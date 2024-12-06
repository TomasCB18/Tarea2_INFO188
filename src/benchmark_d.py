import pandas as pd
import matplotlib.pyplot as plt


csv_path = "../resultados/benchmark_results.csv"


column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)


df_gpu = df[df["mode"] == 1]


n_fixed = df_gpu["n"].max()


df_fixed_gpu = df_gpu[df_gpu["n"] == n_fixed]

df_fixed_gpu = df_fixed_gpu[(df_fixed_gpu["threads_or_gridsize"] >= 1) & (df_fixed_gpu["threads_or_gridsize"] <= 140)]

# promedio los tiempos por número de bloques o threads
df_avg_gpu = df_fixed_gpu.groupby("threads_or_gridsize")["time"].mean().reset_index()

# Rver si hay un registro con threads_or_gridsize == 1
if 1 in df_avg_gpu["threads_or_gridsize"].values:
    # calcular el tiempo con 1 bloque (base para el speedup)
    base_time = df_avg_gpu[df_avg_gpu["threads_or_gridsize"] == 1]["time"].values[0]
else:
    print("No se encontró un registro con threads_or_gridsize == 1. Usando el tiempo con el valor más bajo.")
    # si 1 no está, se usa el valor mas cercano a 1 (el menor disponible)
    base_time = df_avg_gpu["time"].min()

# calcular speedup
df_avg_gpu["speedup"] = base_time / df_avg_gpu["time"]

# suavizar el speedup usando una media movil (ventana de 5)
df_avg_gpu['smoothed_speedup'] = df_avg_gpu['speedup'].rolling(window=5, min_periods=1).mean()

# speedup vs nimero de Bloques
plt.figure(figsize=(10, 6))
plt.plot(df_avg_gpu["threads_or_gridsize"], df_avg_gpu["smoothed_speedup"], marker="o", markersize=5, color='b', label="Speedup GPU Suavizado")
#plt.axhline(y=1, color='r', linestyle='--', label="Speedup Ideal")  # Línea de referencia para el speedup ideal
plt.xlabel("Número de Bloques CUDA (threads_or_gridsize)")
plt.ylabel("Speedup")
plt.title(f"Speedup del Algoritmo GPU (n = {n_fixed})")
plt.grid(True, linestyle="--", linewidth=0.5)


plt.xticks(df_avg_gpu["threads_or_gridsize"].astype(int)[::5])

plt.xticks(rotation=45)

plt.legend()
plt.savefig("../resultados/speedup_plot_gpu_clean.png")
plt.show()
