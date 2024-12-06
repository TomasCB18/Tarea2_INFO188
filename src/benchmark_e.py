import pandas as pd
import matplotlib.pyplot as plt

# Ruta del archivo CSV
csv_path = "../resultados/benchmark_results.csv"

# Leer los datos del CSV
column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)

# Filtrar solo datos para GPU (mode == 1)
df_gpu = df[df["mode"] == 1]

# Tomar un valor alto de 'n' (puedes cambiar este valor si prefieres otro tamaño de problema)
n_fixed = df_gpu["n"].max()

# Filtrar los datos para ese tamaño de problema
df_fixed_gpu = df_gpu[df_gpu["n"] == n_fixed]

# Promediar los tiempos por número de bloques o threads
df_avg_gpu = df_fixed_gpu.groupby("threads_or_gridsize")["time"].mean().reset_index()

# Verificar si hay un registro con threads_or_gridsize == 1
if 1 in df_avg_gpu["threads_or_gridsize"].values:
    # Calcular el tiempo con 1 bloque (base para el speedup)
    base_time = df_avg_gpu[df_avg_gpu["threads_or_gridsize"] == 1]["time"].values[0]
else:
    print("No se encontró un registro con threads_or_gridsize == 1. Usando el tiempo con el valor más bajo.")
    # Si no se encuentra el valor 1, podemos usar el valor más cercano a 1 (el más bajo disponible)
    base_time = df_avg_gpu["time"].min()

# Calcular el speedup
df_avg_gpu["speedup"] = base_time / df_avg_gpu["time"]

# Calcular la eficiencia paralela
df_avg_gpu["efficiency"] = df_avg_gpu["speedup"] / df_avg_gpu["threads_or_gridsize"]

# Graficar Eficiencia Paralela vs Número de Bloques
plt.figure(figsize=(10, 6))
plt.plot(df_avg_gpu["threads_or_gridsize"], df_avg_gpu["efficiency"], marker="o", label="Eficiencia Paralela GPU")
plt.xlabel("Número de Bloques CUDA (threads_or_gridsize)")
plt.ylabel("Eficiencia Paralela")
plt.title(f"Eficiencia Paralela del Algoritmo GPU (n = {n_fixed})")
plt.grid(True, linestyle="--", linewidth=0.5)

# Ajustar los ticks del eje X para que comiencen desde 1
plt.xticks(df_avg_gpu["threads_or_gridsize"].astype(int)[::5])

# Rotar las etiquetas del eje X para mejorar la legibilidad
plt.xticks(rotation=45)

plt.legend()
plt.savefig("../resultados/efficiency_plot_gpu.png")
plt.show()
