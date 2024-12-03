#include <iostream>
#include <vector>
#include <cstdlib>
#include <random> 
#include <omp.h>
#include <cuda_runtime.h>
#include <algorithm> 
#include <ctime>

using namespace std;

// Función para inicializar un arreglo con valores aleatorios
void initializeArray(int *arr, int n) {
    // Crear un generador de números aleatorios con la semilla basada en el tiempo actual
    std::mt19937 rng(static_cast<unsigned int>(std::time(0)));
    
    // Distribución uniforme en el rango [0, 1000000)
    std::uniform_int_distribution<int> dist(0, 999999);  
    
    for (int i = 0; i < n; ++i) {
        arr[i] = dist(rng);  // Genera un número aleatorio uniforme
    }
}
// Merge Sort paralelo para CPU
void parallelMergeSort(int *arr, int *temp, int left, int right, int threads) {
    if (threads <= 1 || right - left <= 1) {
        sort(arr + left, arr + right);
        return;
    }
    int mid = (left + right) / 2;

#pragma omp parallel sections
    {
#pragma omp section
        parallelMergeSort(arr, temp, left, mid, threads / 2);
#pragma omp section
        parallelMergeSort(arr, temp, mid, right, threads / 2);
    }

    // Merge
    int i = left, j = mid, k = left;
    while (i < mid && j < right) {
        if (arr[i] < arr[j]) temp[k++] = arr[i++];
        else temp[k++] = arr[j++];
    }
    while (i < mid) temp[k++] = arr[i++];
    while (j < right) temp[k++] = arr[j++];
    for (i = left; i < right; ++i) arr[i] = temp[i];
}

// Kernel para calcular la máscara de bits en Radix Sort
__global__ void computeMaskKernel(int *d_input, int *d_mask, int bit, int n) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx < n) {
        d_mask[idx] = (d_input[idx] >> bit) & 1;
    }
}

// Kernel para calcular posiciones exclusivas de los 0s
__global__ void computeExclusiveScan(int *d_mask, int *d_scan, int n) {
    extern __shared__ int temp[];
    int idx = threadIdx.x;
    int i = blockIdx.x * blockDim.x + idx;

    if (i < n) {
        temp[idx] = d_mask[i];
    } else {
        temp[idx] = 0;
    }
    __syncthreads();

    // Exclusive scan (Blelloch)
    for (int offset = 1; offset < blockDim.x; offset *= 2) {
        int val = idx >= offset ? temp[idx - offset] : 0;
        __syncthreads();
        temp[idx] += val;
        __syncthreads();
    }

    if (i < n) {
        d_scan[i] = temp[idx];
    }
}

// Kernel para realizar el reordenamiento (scatter)
__global__ void scatterKernel(int *d_input, int *d_output, int *d_mask, int *d_scan, int n, int totalZeros) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx < n) {
        int pos;
        if (d_mask[idx] == 0) {
            pos = d_scan[idx];
        } else {
            pos = totalZeros + idx - d_scan[idx];
        }
        d_output[pos] = d_input[idx];
    }
}

// Función Radix Sort en GPU
void radixSortGPU(int *arr, int n) {
    int *d_input, *d_output, *d_mask, *d_scan;
    cudaMalloc(&d_input, n * sizeof(int));
    cudaMalloc(&d_output, n * sizeof(int));
    cudaMalloc(&d_mask, n * sizeof(int));
    cudaMalloc(&d_scan, n * sizeof(int));

    cudaMemcpy(d_input, arr, n * sizeof(int), cudaMemcpyHostToDevice);

    dim3 blockSize(256);
    dim3 gridSize((n + blockSize.x - 1) / blockSize.x);

    for (int bit = 0; bit < 32; ++bit) {
        // Compute mask for the current bit
        computeMaskKernel<<<gridSize, blockSize>>>(d_input, d_mask, bit, n);
        cudaDeviceSynchronize();

        // Compute exclusive scan
        computeExclusiveScan<<<gridSize, blockSize, blockSize.x * sizeof(int)>>>(d_mask, d_scan, n);
        cudaDeviceSynchronize();

        // Compute totalZeros (last element of the scan array)
        int totalZeros;
        cudaMemcpy(&totalZeros, &d_scan[n - 1], sizeof(int), cudaMemcpyDeviceToHost);
        totalZeros += 1 - ((arr[n - 1] >> bit) & 1);

        // Scatter elements based on bit
        scatterKernel<<<gridSize, blockSize>>>(d_input, d_output, d_mask, d_scan, n, totalZeros);
        cudaDeviceSynchronize();

        // Swap input and output arrays
        swap(d_input, d_output);
    }

    cudaMemcpy(arr, d_input, n * sizeof(int), cudaMemcpyDeviceToHost);

    cudaFree(d_input);
    cudaFree(d_output);
    cudaFree(d_mask);
    cudaFree(d_scan);
}

int main(int argc, char **argv) {
    if (argc != 4) {
        cerr << "Usage: ./prog <n> <mode> <nt>" << endl;
        return 1;
    }

    int n = atoi(argv[1]);
    int mode = atoi(argv[2]);
    int threads = atoi(argv[3]);

    int *arr = new int[n];
    int *temp = new int[n];
    initializeArray(arr, n);

    double startTime, endTime;

    if (mode == 0) { // CPU Mode
        int *arrCopy = new int[n];
        copy(arr, arr + n, arrCopy);

        omp_set_num_threads(threads);
        startTime = omp_get_wtime();
        parallelMergeSort(arrCopy, temp, 0, n, threads);
        endTime = omp_get_wtime();
        cout << "CPU Merge Sort Time: " << (endTime - startTime) << " seconds" << endl;

        delete[] arrCopy;
    }

    else if (mode == 1) { // GPU Mode
        int *arrCopy = new int[n];
        copy(arr, arr + n, arrCopy);

        startTime = omp_get_wtime();
        radixSortGPU(arrCopy, n);
        endTime = omp_get_wtime();
        cout << "GPU Radix Sort Time: " << (endTime - startTime) << " seconds" << endl;

        delete[] arrCopy;
    }
    else {
        cerr << "Invalid mode. Use 0 for CPU and 1 for GPU." << endl;
        delete[] arr;
        delete[] temp;
        return 1;
    }

        delete[] arr;
        delete[] temp;
        return 0;
    }
