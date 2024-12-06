import pandas as pd
import matplotlib.pyplot as plt


csv_path = "../resultados/benchmark_results.csv"

column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)

#  solo datos para GPU (mode == 1)
df_gpu = df[df["mode"] == 1]

n_fixed = df_gpu["n"].max()

# filtro de  los datos para ese tamaño de problema
df_fixed_gpu = df_gpu[df_gpu["n"] == n_fixed]

df_fixed_gpu = df_fixed_gpu[(df_fixed_gpu["threads_or_gridsize"] >= 1) & (df_fixed_gpu["threads_or_gridsize"] <= 140)]

# promedio de los tiempos por numero de bloques o threads
df_avg_gpu = df_fixed_gpu.groupby("threads_or_gridsize")["time"].mean().reset_index()

# verificar si hay un registro con threads_or_gridsize == 1
if 1 in df_avg_gpu["threads_or_gridsize"].values:
    # calcular el tiempo con 1 bloque (base para el speedup)
    base_time = df_avg_gpu[df_avg_gpu["threads_or_gridsize"] == 1]["time"].values[0]
else:
    print("No se encontró un registro con threads_or_gridsize == 1. Usando el tiempo con el valor más bajo.")
    base_time = df_avg_gpu["time"].min()

# calcular el speedup
df_avg_gpu["speedup"] = base_time / df_avg_gpu["time"]

# calcular la eficiencia paralela
df_avg_gpu["efficiency"] = df_avg_gpu["speedup"] / df_avg_gpu["threads_or_gridsize"]

# grafico de  Eficiencia Paralela vs numero de Bloques
plt.figure(figsize=(10, 6))
plt.plot(df_avg_gpu["threads_or_gridsize"], df_avg_gpu["efficiency"], marker="o", label="Eficiencia Paralela GPU")
plt.xlabel("Número de Bloques CUDA (threads_or_gridsize)")
plt.ylabel("Eficiencia Paralela")
plt.title(f"Eficiencia Paralela del Algoritmo GPU (n = {n_fixed})")
plt.grid(True, linestyle="--", linewidth=0.5)

# ajustar los ticks del eje X para que comiencen desde 1
plt.xticks(df_avg_gpu["threads_or_gridsize"].astype(int)[::5])

# rotar las etiquetas del eje X para mejorar la legibilidad
plt.xticks(rotation=45)

plt.legend()
plt.savefig("../resultados/benchmark_e.png")
plt.show()
