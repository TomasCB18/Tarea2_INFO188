import pandas as pd
import matplotlib.pyplot as plt

# Ruta del archivo CSV
csv_path = "../resultados/benchmark_results.csv"

# Leer los datos del CSV y asignar nombres a las columnas manualmente
column_names = ["n", "mode", "threads_or_blocks", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)

# Promediar los tiempos por configuración (agrupando por n y mode)
df_avg = df.groupby(["n", "mode"])["time"].mean().reset_index()

# Filtrar datos para CPU (mode = 0) y GPU (mode = 1)
cpu_data = df_avg[df_avg["mode"] == 0]
gpu_data = df_avg[df_avg["mode"] == 1]

# Graficar Tiempo vs n
plt.figure(figsize=(10, 6))
plt.plot(cpu_data["n"], cpu_data["time"], label="CPU (Merge Sort)", marker="o")
plt.plot(gpu_data["n"], gpu_data["time"], label="GPU (Radix Sort)", marker="x")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Tamaño del arreglo (n)")
plt.ylabel("Tiempo (segundos)")
plt.title("Benchmark: Tiempo vs Tamaño del Arreglo (n)")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.savefig("../resultados/benchmark_plot.png")
plt.show()
