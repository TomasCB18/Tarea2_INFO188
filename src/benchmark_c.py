import pandas as pd
import matplotlib.pyplot as plt


csv_path = "../resultados/benchmark_results.csv"


column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)

# filtrar datos para CPU (mode = 0) y un tamaño de problema fijo (e.g., n = 100000000)
n_fixed = df["n"].max() 
df_fixed = df[(df["mode"] == 0) & (df["n"] == n_fixed)]

# promedio de  tiempos por numero de hilos
df_avg = df_fixed.groupby("threads_or_gridsize")["time"].mean().reset_index()

# caclular el tiempo con 1 hilo (base para el speedup)
base_time = df_avg[df_avg["threads_or_gridsize"] == 1]["time"].values[0]

# calcular el speedup
df_avg["speedup"] = base_time / df_avg["time"]

# calcular la eficiencia paralela
df_avg["efficiency"] = df_avg["speedup"] / df_avg["threads_or_gridsize"]

# grafico Eficiencia vs numero de hilos
plt.figure(figsize=(10, 6))
plt.plot(df_avg["threads_or_gridsize"], df_avg["efficiency"], marker="o", label="Eficiencia paralela")
plt.xlabel("numero de Hilos")
plt.ylabel("Eficiencia Paralela")
plt.title(f"Eficiencia Paralela del Algoritmo CPU (n = {n_fixed})")
plt.grid(True, linestyle="--", linewidth=0.5)
plt.xticks(range(1, df_avg["threads_or_gridsize"].max() + 1))
plt.legend()
plt.savefig("../resultados/efficiency_plot.png")
plt.show()
