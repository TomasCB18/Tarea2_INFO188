import pandas as pd
import matplotlib.pyplot as plt


csv_path = "../resultados/benchmark_results.csv"


column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)

# promedio de los tiempos por configuración (agrupando por n y mode)
df_avg = df.groupby(["n", "mode"])["time"].mean().reset_index()

# filtro de los datos para std::sort (mode == 2)
df_sort = df_avg[df_avg["mode"] == 2]  

# lista para el speedup vs n
speedup_vs_n = []

# recorrer los diferentes tamaños de problema n de std::sort
for n_value in df_sort["n"].unique():
    # filtrado de el tiempo de std::sort para cada n
    time_sort = df_sort[df_sort["n"] == n_value]["time"].values[0]  # tiempo de std::sort
    
    # calcular el speedup como 1 (sin otra referencia para comparar)
    speedup = 1  # siempre será 1, ya que no hay otra opción comparativa
    speedup_vs_n.append([n_value, speedup])

# convertir la lista a un DataFrame para graficar
df_speedup = pd.DataFrame(speedup_vs_n, columns=["n", "speedup"])

# grafica de  Speedup vs n
plt.figure(figsize=(10, 6))
plt.plot(df_speedup["n"], df_speedup["speedup"], marker="o", label="Speedup std::sort")
plt.xscale("log")  # escala logarítmica para el eje X y para y
plt.yscale("log")  
plt.xlabel("Tamaño del arreglo (n)")
plt.ylabel("Speedup")
plt.title("Benchmark: Speedup std::sort (sin comparación)")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# save grafico
plt.savefig("../resultados/speedup_vs_n_sort_plot.png")
plt.show()
