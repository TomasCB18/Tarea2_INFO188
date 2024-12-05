"""import pandas as pd
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
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos desde el archivo CSV sin encabezados
df = pd.read_csv("../resultados/benchmark_results.csv", header=None)

# Nombrar las columnas para mayor claridad
df.columns = ["n", "modo", "nt", "tiempo"]

# Función para calcular el speedup
def calcular_speedup(tiempo_1, tiempo_n):
    return tiempo_1 / tiempo_n

# Función para calcular la eficiencia paralela
def calcular_eficiencia_paralela(speedup, num_threads):
    return speedup / num_threads

# Función para generar los gráficos
def generar_graficos(df):
    # Gráfico a: Tiempo vs n
    df_cpu = df[df["modo"] == 0]  # Filtrar solo CPU
    df_gpu = df[df["modo"] == 1]  # Filtrar solo GPU
    
    plt.figure(figsize=(10, 6))
    for n in sorted(df_cpu["n"].unique()):
        df_cpu_n = df_cpu[df_cpu["n"] == n]
        tiempo_promedio_cpu = df_cpu_n["tiempo"].mean()
        plt.plot(n, tiempo_promedio_cpu, 'bo')  # Punto azul para CPU
    
    for n in sorted(df_gpu["n"].unique()):
        df_gpu_n = df_gpu[df_gpu["n"] == n]
        tiempo_promedio_gpu = df_gpu_n["tiempo"].mean()
        plt.plot(n, tiempo_promedio_gpu, 'ro')  # Punto rojo para GPU
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("n")
    plt.ylabel("Tiempo (s)")
    plt.title("Tiempo vs n (CPU vs GPU)")
    plt.legend(["CPU", "GPU"])
    plt.grid(True)
    plt.show()

    # Gráfico b: Speedup vs num-threads (solo CPU)
    df_cpu_high_n = df_cpu[df_cpu["n"] > 10000000]  # Filtrar valores altos de n
    speedups = []
    num_threads = sorted(df_cpu_high_n["nt"].unique())
    
    for nt in num_threads:
        df_nt = df_cpu_high_n[df_cpu_high_n["nt"] == nt]
        tiempo_1_thread = df_cpu_high_n[df_cpu_high_n["nt"] == 1]["tiempo"].mean()
        tiempo_nt = df_nt["tiempo"].mean()
        speedup = calcular_speedup(tiempo_1_thread, tiempo_nt)
        speedups.append(speedup)

    plt.figure(figsize=(10, 6))
    plt.plot(num_threads, speedups, 'bo-')
    plt.xlabel("Número de hilos (threads)")
    plt.ylabel("Speedup")
    plt.title("Speedup vs num-threads (CPU)")
    plt.grid(True)
    plt.show()

    # Gráfico c: Eficiencia paralela vs num-threads (solo CPU)
    eficiencias = [calcular_eficiencia_paralela(speedup, nt) for speedup, nt in zip(speedups, num_threads)]

    plt.figure(figsize=(10, 6))
    plt.plot(num_threads, eficiencias, 'ro-')
    plt.xlabel("Número de hilos (threads)")
    plt.ylabel("Eficiencia paralela")
    plt.title("Eficiencia paralela vs num-threads (CPU)")
    plt.grid(True)
    plt.show()

    # Gráfico d: Speedup vs num-bloques (solo GPU)
    df_gpu_high_n = df_gpu[df_gpu["n"] > 10000000]  # Filtrar valores altos de n
    speedups_gpu = []
    num_bloques = sorted(df_gpu_high_n["nt"].unique())
    
    for bloques in num_bloques:
        df_bloques = df_gpu_high_n[df_gpu_high_n["nt"] == bloques]
        tiempo_1_bloque = df_gpu_high_n[df_gpu_high_n["nt"] == 1]["tiempo"].mean()
        tiempo_bloques = df_bloques["tiempo"].mean()
        speedup_gpu = calcular_speedup(tiempo_1_bloque, tiempo_bloques)
        speedups_gpu.append(speedup_gpu)

    plt.figure(figsize=(10, 6))
    plt.plot(num_bloques, speedups_gpu, 'bo-')
    plt.xlabel("Número de bloques CUDA")
    plt.ylabel("Speedup")
    plt.title("Speedup vs num-bloques (GPU)")
    plt.grid(True)
    plt.show()

    # Gráfico e: Eficiencia paralela vs num-bloques (solo GPU)
    eficiencias_gpu = [calcular_eficiencia_paralela(speedup_gpu, bloques) for speedup_gpu, bloques in zip(speedups_gpu, num_bloques)]

    plt.figure(figsize=(10, 6))
    plt.plot(num_bloques, eficiencias_gpu, 'ro-')
    plt.xlabel("Número de bloques CUDA")
    plt.ylabel("Eficiencia paralela")
    plt.title("Eficiencia paralela vs num-bloques (GPU)")
    plt.grid(True)
    plt.show()

    # Gráfico f: Speedup vs n
    speedups_std = []
    for n in sorted(df["n"].unique()):
        df_n = df[df["n"] == n]
        tiempo_std_sort = df_n[df_n["modo"] == 2]["tiempo"].mean()  # Asumimos modo 2 es el std::sort
        tiempo_cpu = df_n[df_n["modo"] == 0]["tiempo"].mean()
        speedup_std = calcular_speedup(tiempo_std_sort, tiempo_cpu)
        speedups_std.append(speedup_std)

    plt.figure(figsize=(10, 6))
    plt.plot(sorted(df["n"].unique()), speedups_std, 'go-')
    plt.xlabel("n")
    plt.ylabel("Speedup")
    plt.title("Speedup vs n (comparado con std::sort)")
    plt.grid(True)
    plt.show()

# Llamar a la función para generar los gráficos
generar_graficos(df)
