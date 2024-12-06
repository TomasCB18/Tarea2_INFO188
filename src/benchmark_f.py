import pandas as pd
import matplotlib.pyplot as plt

# Ruta del archivo CSV
csv_path = "../resultados/benchmark_results.csv"

# Leer los datos del CSV y asignar nombres a las columnas manualmente
column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)

# Promediar los tiempos por configuración (agrupando por n y mode)
df_avg = df.groupby(["n", "mode"])["time"].mean().reset_index()

# Filtrar los datos para std::sort (mode == 2)
df_sort = df_avg[df_avg["mode"] == 2]  # std::sort (mode == 2)

# Inicializar lista para el speedup vs n
speedup_vs_n = []

# Recorrer los diferentes tamaños de problema n de std::sort
for n_value in df_sort["n"].unique():
    # Filtrar el tiempo de std::sort para cada n
    time_sort = df_sort[df_sort["n"] == n_value]["time"].values[0]  # Tiempo de std::sort
    
    # Calcular el speedup como 1 (sin otra referencia para comparar)
    speedup = 1  # Siempre será 1, ya que no hay otra opción comparativa
    speedup_vs_n.append([n_value, speedup])

# Convertir la lista a un DataFrame para graficar
df_speedup = pd.DataFrame(speedup_vs_n, columns=["n", "speedup"])

# Graficar Speedup vs n
plt.figure(figsize=(10, 6))
plt.plot(df_speedup["n"], df_speedup["speedup"], marker="o", label="Speedup std::sort")
plt.xscale("log")  # Escala logarítmica para el eje X
plt.yscale("log")  # Escala logarítmica para el eje Y
plt.xlabel("Tamaño del arreglo (n)")
plt.ylabel("Speedup")
plt.title("Benchmark: Speedup std::sort (sin comparación)")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Guardar la gráfica
plt.savefig("../resultados/speedup_vs_n_sort_plot.png")
plt.show()
