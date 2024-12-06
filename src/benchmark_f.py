import pandas as pd
import matplotlib.pyplot as plt


csv_path = "../resultados/benchmark_results.csv"


column_names = ["n", "mode", "threads_or_gridsize", "time"]
df = pd.read_csv(csv_path, header=None, names=column_names)


df.columns = df.columns.str.strip()

# promedio de los tiempos por configuración (agrupando por n y mode)
df_avg = df.groupby(["n", "mode", "threads_or_gridsize"])["time"].mean().reset_index()

# filtro para GPU, CPU y std::sort (tamaños de n menores a 1,000,000,000)
gpu_data = df_avg[(df_avg["n"] < 1000000000) & (df_avg["mode"] == 1)]
cpu_data = df_avg[(df_avg["n"] < 1000000000) & (df_avg["mode"] == 0)]
stl_sort_data = df_avg[(df_avg["n"] < 1000000000) & (df_avg["mode"] == 2)]

# listas para almacenar el speedup de CPU y GPU con respecto a std::sort
speedup_cpu = []
speedup_gpu = []
speedup_sort = []

# iterar los diferentes tamaños de n en los DataFrames filtrados
for n_value in gpu_data["n"].unique():  # se usan los valores únicos de 'n' de los datos de GPU (todos deben tener el mismo rango)
    # tiempo de std::sort para cada n
    stl_sort_row = stl_sort_data[stl_sort_data["n"] == n_value]
    if len(stl_sort_row) > 0:
        time_sort = stl_sort_row["time"].values[0]
    else:
        print(f"Advertencia: No se encontraron datos para std::sort con n = {n_value}")
        continue 

    #tiempo de CPU para el mismo n
    cpu_row = cpu_data[cpu_data["n"] == n_value]
    if len(cpu_row) > 0:
        time_cpu = cpu_row["time"].values[0]
    else:
        print(f"Advertencia: No se encontraron datos para CPU con n = {n_value}")
        continue  

    # tiempo de GPU para el mismo n
    gpu_row = gpu_data[gpu_data["n"] == n_value]
    if len(gpu_row) > 0:
        time_gpu = gpu_row["time"].values[0]
    else:
        print(f"Advertencia: No se encontraron datos para GPU con n = {n_value}")
        continue  

    # speedup para CPU y GPU con respecto a std::sort
    speedup_cpu_value = time_sort / time_cpu
    speedup_gpu_value = time_sort / time_gpu
    speedup_sort_value = 1  # El speedup de std::sort con respecto a sí mismo es 1

    # Almacenar los resultados de speedup
    speedup_cpu.append([n_value, speedup_cpu_value])
    speedup_gpu.append([n_value, speedup_gpu_value])
    speedup_sort.append([n_value, speedup_sort_value])

# pasar las listas a DataFrames para graficar
df_speedup_cpu = pd.DataFrame(speedup_cpu, columns=["n", "speedup_cpu"])
df_speedup_gpu = pd.DataFrame(speedup_gpu, columns=["n", "speedup_gpu"])
df_speedup_sort = pd.DataFrame(speedup_sort, columns=["n", "speedup_sort"])


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

# Guardar la gráfica
plt.savefig("../resultados/benchmark_f.png")
plt.show()
