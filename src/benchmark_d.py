import pandas as pd
import matplotlib.pyplot as plt


csv_path = "../resultados/benchmark_results.csv"


column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)

# filtrar solo datos para GPU (mode == 1)
df_gpu = df[df["mode"] == 1]

# filtro de un valor alto de 'n'
n_fixed = df_gpu["n"].max()

# filtrar los datos para ese tamaño de problema
df_fixed_gpu = df_gpu[df_gpu["n"] == n_fixed]

df_fixed_gpu = df_fixed_gpu[(df_fixed_gpu["threads_or_gridsize"] >= 1) & (df_fixed_gpu["threads_or_gridsize"] <= 140)]

# promedio los tiempos por numerode bloques o threads
df_avg_gpu = df_fixed_gpu.groupby("threads_or_gridsize")["time"].mean().reset_index()

# revisar si hay un registro con threads_or_gridsize == 1
if 1 in df_avg_gpu["threads_or_gridsize"].values:
    # calcular el tiempo con 1 bloque (base para el speedup)
    base_time = df_avg_gpu[df_avg_gpu["threads_or_gridsize"] == 1]["time"].values[0]
else:
    print("No se encontro un registro con threads_or_gridsize == 1. Usando el tiempo con el valor mas bajo.")
    # si  el valor 1 no esta, se usa el valor mascercano a 1 (el mas bajo disponible)
    base_time = df_avg_gpu["time"].min()

# calcular el speedup
df_avg_gpu["speedup"] = base_time / df_avg_gpu["time"]

# Graficar Speedup vs numerp de Bloques
plt.figure(figsize=(10, 6))
plt.plot(df_avg_gpu["threads_or_gridsize"], df_avg_gpu["speedup"], marker="o", label="Speedup GPU")
plt.xlabel("Número de Bloques CUDA (threads_or_gridsize)")
plt.ylabel("Speedup")
plt.title(f"Speedup del Algoritmo GPU (n = {n_fixed})")
plt.grid(True, linestyle="--", linewidth=0.5)

# ajustar los ticks del eje X
plt.xticks(df_avg_gpu["threads_or_gridsize"].astype(int)[::5])  # mostrar cada 5 valor del eje X 

# rotar las etiquetas del eje X para mejorar la legibilidad
plt.xticks(rotation=45)

plt.legend()
plt.savefig("../resultados/speedup_plot_gpu.png")
plt.show()
