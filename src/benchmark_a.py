import pandas as pd
import matplotlib.pyplot as plt

csv_path = "../resultados/benchmark_results.csv"


column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)


df.columns = df.columns.str.strip()

# promedio de los tiempos por configuración (agrupando por n y mode)
df_avg = df.groupby(["n", "mode", "threads_or_gridsize"])["time"].mean().reset_index()


# valores de la entrada n 
n_values = [
    1000, 3000, 5000, 7000, 10000,
    30000, 50000, 70000, 100000,
    300000, 500000, 700000, 1000000,
    3000000, 5000000, 7000000, 10000000,
    30000000, 50000000, 70000000, 100000000,
    300000000, 500000000, 700000000
]


# diccionario para almacenar los resultados filtrados por cada valor de n
gpu_data_filtered = {}
cpu_data_filtered = {}

# iterar los valores de n
for n in n_values:
    # calcular threads_or_gridsize para cada valor de n, ya que para el primer experimento, se hace sin asignar threads de manera manual
    gridsize = (n + 255) // 256
    threads = min(12, (n + 999) // 1000)  # formula para CPU
    
    # filtro en el df para obtener solo los registros de GPU y el threads_or_gridsize calculado
    gpu_data = df_avg[(df_avg["n"] == n) & (df_avg["mode"] == 1) & (df_avg["threads_or_gridsize"] == gridsize)]
    # guardar resultado en el diccionario
    gpu_data_filtered[n] = gpu_data


    cpu_data = df_avg[(df_avg["n"] == n) & (df_avg["mode"] == 0) & (df_avg["threads_or_gridsize"] == threads)]
    cpu_data_filtered[n] = cpu_data


# concatenar los datos filtrados para gpu y cpu en un solo DataFrame
gpu_data = pd.concat(gpu_data_filtered.values())
cpu_data = pd.concat(cpu_data_filtered.values())

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
