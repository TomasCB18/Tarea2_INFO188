#include <iostream>
#include <vector>
#include <cstdlib>
#include <random>
#include <omp.h>
#include <cuda_runtime.h>
#include <algorithm>
#include <ctime>
#include <fstream>
#include <sys/stat.h>
#include <sys/types.h>

using namespace std;

// fun para inicializar un arreglo con valores aleatorios
void initializeArray(int *arr, int n) {
    mt19937 rng(static_cast<unsigned int>(time(0)));
    uniform_int_distribution<int> dist(0, 999999);
    for (int i = 0; i < n; ++i) {
        arr[i] = dist(rng);
    }
}

// merge-Sort paralelo para CPU
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

    int i = left, j = mid, k = left;
    while (i < mid && j < right) {
        if (arr[i] < arr[j]) temp[k++] = arr[i++];
        else temp[k++] = arr[j++];
    }
    while (i < mid) temp[k++] = arr[i++];
    while (j < right) temp[k++] = arr[j++];
    for (i = left; i < right; ++i) arr[i] = temp[i];
}

// kernel para calcular la máscara de bits en Radix Sort
__global__ void computeMaskKernel(int *d_input, int *d_mask, int bit, int n) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx < n) {
        d_mask[idx] = (d_input[idx] >> bit) & 1;
    }
}

// kernel para calcular posiciones exclusivas de los 0s
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

// kernel para realizar el reordenamiento (scatter)
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

// fun Radix Sort en GPU
void radixSortGPU(int *arr, int n, int gridSize) {
    int *d_input, *d_output, *d_mask, *d_scan;
    cudaMalloc(&d_input, n * sizeof(int));
    cudaMalloc(&d_output, n * sizeof(int));
    cudaMalloc(&d_mask, n * sizeof(int));
    cudaMalloc(&d_scan, n * sizeof(int));

    cudaMemcpy(d_input, arr, n * sizeof(int), cudaMemcpyHostToDevice);

    dim3 blockSize(256);
    //dim3 gridSize((n + blockSize.x - 1) / blockSize.x); esta formula se uso para el benchmark (el primero) directo entre gpu vs cpu

    for (int bit = 0; bit < 32; ++bit) {
        computeMaskKernel<<<gridSize, blockSize>>>(d_input, d_mask, bit, n);
        cudaDeviceSynchronize();

        computeExclusiveScan<<<gridSize, blockSize, blockSize.x * sizeof(int)>>>(d_mask, d_scan, n);
        cudaDeviceSynchronize();

        int totalZeros;
        cudaMemcpy(&totalZeros, &d_scan[n - 1], sizeof(int), cudaMemcpyDeviceToHost);
        totalZeros += 1 - ((arr[n - 1] >> bit) & 1);

        scatterKernel<<<gridSize, blockSize>>>(d_input, d_output, d_mask, d_scan, n, totalZeros);
        cudaDeviceSynchronize();

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
        cerr << "Usage: ./prog <n> <mode> <threads_or_gridsize>" << endl;
        return 1;
    }

    int n = atoi(argv[1]);
    int mode = atoi(argv[2]);
    int threads_or_gridsize = atoi(argv[3]);

    int *arr = new int[n];
    int *temp = new int[n];
    //printf("Inicializando arreglo..."); fflush(stdout);
    initializeArray(arr, n);
    //printf("Arreglo inicializado\n");

    double startTime, endTime;

    const string csvFile = "../resultados/benchmark_results.csv";
    mkdir("../resultados", 0777);

    ofstream outFile(csvFile, ios::app);
    if (!outFile.is_open()) {
        cerr << "Error al abrir el archivo CSV para escribir: " << csvFile << endl;
        delete[] arr;
        delete[] temp;
        return 1;
    }
    //printf("Ordenando arreglo..."); fflush(stdout);
    if (mode == 0) { // CPU Mode
        omp_set_num_threads(threads_or_gridsize);
        startTime = omp_get_wtime();
        parallelMergeSort(arr, temp, 0, n, threads_or_gridsize);
        endTime = omp_get_wtime();
       // printf("Arreglo ordenado\n");
        printf("Tiempo MergeSort en CPU: %f segundos\n", (endTime - startTime)); fflush(stdout);
    } else if (mode == 1) { // GPU Mode
        startTime = omp_get_wtime();
        radixSortGPU(arr, n, threads_or_gridsize);
        endTime = omp_get_wtime();
       // printf("Arreglo ordenado\n");
        printf("Tiempo RadixSort en GPU: %f segundos\n", (endTime - startTime)); fflush(stdout);
    } else {
        cerr << "Invalid mode. Use 0 for CPU and 1 for GPU." << endl;
        delete[] arr;
        delete[] temp;
        return 1;
    }

    outFile << n << "," << mode << "," << threads_or_gridsize << "," << (endTime - startTime) << "\n";
    outFile.close();

    delete[] arr;
    delete[] temp;
    return 0;
}