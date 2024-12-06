import pandas as pd
import matplotlib.pyplot as plt


csv_path = "../resultados/benchmark_results.csv"

# read  datos del csv  y asignar nombres a las columnas manualmente
column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)

# promedio de  los tiempos por configuración (agrupando por n y mode)
df_avg = df.groupby(["n", "mode"])["time"].mean().reset_index()

# filtro datos para CPU (mode = 0) con threads_or_gridsize == 8 y GPU (mode = 1) con threads_or_gridsize == 0
cpu_data = df_avg[(df_avg["mode"] == 0) & (df_avg["threads_or_gridsize"] == 8)]
gpu_data = df_avg[(df_avg["mode"] == 1) & (df_avg["threads_or_gridsize"] == 0)]

# grafico tiemmpo vs n
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
