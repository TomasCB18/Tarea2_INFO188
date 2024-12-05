import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta al archivo CSV
csv_file = "../resultados/benchmark_results.csv"

# Verificar si el archivo existe
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"No se encontró el archivo: {csv_file}. Asegúrate de ejecutar el código CUDA primero.")

# Cargar los datos del archivo CSV
data = pd.read_csv(csv_file, names=["n", "mode", "threads_or_blocks", "time"])

# Gráficos
def plot_time_vs_n(data):
    plt.figure(figsize=(10, 6))
    for mode, label in [(0, "CPU"), (1, "GPU")]:
        subset = data[data["mode"] == mode]
        plt.plot(subset["n"], subset["time"], label=f"{label} Time")
    plt.xlabel("Tamaño del arreglo (n)")
    plt.ylabel("Tiempo de ejecución (segundos)")
    plt.title("Tiempo de ejecución vs Tamaño del arreglo")
    plt.legend()
    plt.grid()
    plt.savefig("../resultados/tiempo_vs_n.png")
    plt.show()

def plot_speedup_cpu(data):
    cpu_data = data[data["mode"] == 0]
    single_thread_time = cpu_data[cpu_data["threads_or_blocks"] == 1]["time"].values[0]
    cpu_data["speedup"] = single_thread_time / cpu_data["time"]

    plt.figure(figsize=(10, 6))
    plt.plot(cpu_data["threads_or_blocks"], cpu_data["speedup"], marker="o", label="CPU Speedup")
    plt.xlabel("Número de hilos")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Número de hilos (CPU)")
    plt.grid()
    plt.legend()
    plt.savefig("../resultados/speedup_cpu.png")
    plt.show()

def plot_efficiency_cpu(data):
    cpu_data = data[data["mode"] == 0]
    single_thread_time = cpu_data[cpu_data["threads_or_blocks"] == 1]["time"].values[0]
    cpu_data["speedup"] = single_thread_time / cpu_data["time"]
    cpu_data["efficiency"] = cpu_data["speedup"] / cpu_data["threads_or_blocks"]

    plt.figure(figsize=(10, 6))
    plt.plot(cpu_data["threads_or_blocks"], cpu_data["efficiency"], marker="o", label="CPU Efficiency")
    plt.xlabel("Número de hilos")
    plt.ylabel("Eficiencia paralela")
    plt.title("Eficiencia paralela vs Número de hilos (CPU)")
    plt.grid()
    plt.legend()
    plt.savefig("../resultados/eficiencia_cpu.png")
    plt.show()

def plot_speedup_gpu(data):
    gpu_data = data[data["mode"] == 1]
    single_block_time = gpu_data[gpu_data["threads_or_blocks"] == 1]["time"].values[0]
    gpu_data["speedup"] = single_block_time / gpu_data["time"]

    plt.figure(figsize=(10, 6))
    plt.plot(gpu_data["threads_or_blocks"], gpu_data["speedup"], marker="o", label="GPU Speedup")
    plt.xlabel("Número de bloques")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Número de bloques (GPU)")
    plt.grid()
    plt.legend()
    plt.savefig("../resultados/speedup_gpu.png")
    plt.show()

def plot_efficiency_gpu(data):
    gpu_data = data[data["mode"] == 1]
    single_block_time = gpu_data[gpu_data["threads_or_blocks"] == 1]["time"].values[0]
    gpu_data["speedup"] = single_block_time / gpu_data["time"]
    gpu_data["efficiency"] = gpu_data["speedup"] / gpu_data["threads_or_blocks"]

    plt.figure(figsize=(10, 6))
    plt.plot(gpu_data["threads_or_blocks"], gpu_data["efficiency"], marker="o", label="GPU Efficiency")
    plt.xlabel("Número de bloques")
    plt.ylabel("Eficiencia paralela")
    plt.title("Eficiencia paralela vs Número de bloques (GPU)")
    plt.grid()
    plt.legend()
    plt.savefig("../resultados/eficiencia_gpu.png")
    plt.show()

def plot_speedup_vs_n(data):
    cpu_data = data[data["mode"] == 0]
    gpu_data = data[data["mode"] == 1]

    std_sort_time = cpu_data[cpu_data["threads_or_blocks"] == 1]["time"].values[0]

    cpu_speedup = std_sort_time / cpu_data["time"]
    gpu_speedup = std_sort_time / gpu_data["time"]

    plt.figure(figsize=(10, 6))
    plt.plot(cpu_data["n"], cpu_speedup, label="CPU Speedup vs n")
    plt.plot(gpu_data["n"], gpu_speedup, label="GPU Speedup vs n")
    plt.xlabel("Tamaño del arreglo (n)")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Tamaño del arreglo")
    plt.legend()
    plt.grid()
    plt.savefig("../resultados/speedup_vs_n.png")
    plt.show()

# Ejecutar los gráficos
plot_time_vs_n(data)
plot_speedup_cpu(data)
plot_efficiency_cpu(data)
plot_speedup_gpu(data)
plot_efficiency_gpu(data)
plot_speedup_vs_n(data)
