"""import pandas as pd
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
plt.title("Benchmark: Speedup std::sort")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# save grafico
plt.savefig("../resultados/benchmark_f.png")
plt.show()
"""

import pandas as pd
import matplotlib.pyplot as plt


csv_path = "../resultados/benchmark_results.csv"


column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)

df.columns = df.columns.str.strip()

# promedio de los tiempos por configuración (agrupando por n y mode)
df_avg = df.groupby(["n", "mode", "threads_or_gridsize"])["time"].mean().reset_index()


n_values = [
    1000, 3000, 5000, 7000, 10000,
    30000, 50000, 70000, 100000,
    300000, 500000, 700000, 1000000,
    3000000, 5000000, 7000000, 10000000,
    30000000, 50000000, 70000000, 100000000,
    300000000, 500000000, 700000000
]


gpu_data_filtered = {}
cpu_data_filtered = {}
stl_sort_data_filtered = {}


for n in n_values:
    # filtro para GPU (mode == 1)
    gpu_data = df_avg[(df_avg["n"] == n) & (df_avg["mode"] == 1)]
    gpu_data_filtered[n] = gpu_data
    
    # filtro para CPU (mode == 0)
    cpu_data = df_avg[(df_avg["n"] == n) & (df_avg["mode"] == 0)]
    cpu_data_filtered[n] = cpu_data
    
    # filtro para std::sort (mode == 2)
    stl_sort_data = df_avg[(df_avg["n"] == n) & (df_avg["mode"] == 2)]
    stl_sort_data_filtered[n] = stl_sort_data

gpu_data = pd.concat(gpu_data_filtered.values())
cpu_data = pd.concat(cpu_data_filtered.values())
stl_sort_data = pd.concat(stl_sort_data_filtered.values())


speedup_cpu = []
speedup_gpu = []
speedup_sort = []

for n_value in n_values:
    # Obtener el tiempo de std::sort para cada n
    stl_sort_row = stl_sort_data[stl_sort_data["n"] == n_value]
    if len(stl_sort_row) > 0:
        time_sort = stl_sort_row["time"].values[0]
    else:
        print(f"Advertencia: No se encontraron datos para std::sort con n = {n_value}")
        continue 

    # Obtener el tiempo de CPU para el mismo n
    cpu_row = cpu_data[cpu_data["n"] == n_value]
    if len(cpu_row) > 0:
        time_cpu = cpu_row["time"].values[0]
    else:
        print(f"Advertencia: No se encontraron datos para CPU con n = {n_value}")
        continue  

    # Obtener el tiempo de GPU para el mismo n
    gpu_row = gpu_data[gpu_data["n"] == n_value]
    if len(gpu_row) > 0:
        time_gpu = gpu_row["time"].values[0]
    else:
        print(f"Advertencia: No se encontraron datos para GPU con n = {n_value}")
        continue  

    speedup_cpu_value = time_sort / time_cpu
    speedup_gpu_value = time_sort / time_gpu
    speedup_sort_value = 1  # El speedup de std::sort con respecto a sí mismo es 1

    speedup_cpu.append([n_value, speedup_cpu_value])
    speedup_gpu.append([n_value, speedup_gpu_value])
    speedup_sort.append([n_value, speedup_sort_value])


df_speedup_cpu = pd.DataFrame(speedup_cpu, columns=["n", "speedup_cpu"])
df_speedup_gpu = pd.DataFrame(speedup_gpu, columns=["n", "speedup_gpu"])
df_speedup_sort = pd.DataFrame(speedup_sort, columns=["n", "speedup_sort"])

# grafico del speedup de los tres algoritmos (CPU, GPU, std::sort)
plt.figure(figsize=(10, 6))
plt.plot(df_speedup_cpu["n"], df_speedup_cpu["speedup_cpu"], label="Speedup CPU (Merge Sort)", marker="o")
plt.plot(df_speedup_gpu["n"], df_speedup_gpu["speedup_gpu"], label="Speedup GPU (Radix Sort)", marker="x")
plt.plot(df_speedup_sort["n"], df_speedup_sort["speedup_sort"], label="Speedup std::sort", marker="s")


plt.xscale("log")  
plt.yscale("log")  
plt.xlabel("Tamaño del arreglo (n)")
plt.ylabel("Speedup")
plt.title("Benchmark: Speedup de los Algoritmos CPU, GPU y std::sort")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)


plt.savefig("../resultados/benchmark_f.png")
plt.show()
