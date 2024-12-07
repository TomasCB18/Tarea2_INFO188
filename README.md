# Tarea2_INFO188
2024, INFO188 Tarea 2: Batalla de sorting paralelo

# Integrantes

Renato Atencio
Tomás Contreras
Fabrizio Fresard
Handel Venegas

# Descripción del Proyecto

Este proyecto implementa un benchmark para comparar el rendimiento de distintos algoritmos de ordenamiento en CPU y GPU. Los algoritmos soportados son:

    MergeSort Paralelo en CPU utilizando OpenMP.
    Radix Sort en GPU utilizando CUDA.
    std::sort en CPU.

La finalidad es evaluar el rendimiento de estos algoritmos en diferentes configuraciones y tamaños de datos.

Para obtener los resultados, se genera un benchmark_results.csv donde se guardan los resultados de la siguiente manera:
tamaño del array, modo (GPU,CPU o sort), Threads o gridsize, tiempo de ejecucion.

Para obtener los graficos de cada benchmark, se ejecuta celda por celda el script jupyter graficos.ipynb:


# Compilación

El proyecto utiliza un archivo Makefile para facilitar la compilación. Comando para compilar:

make

# Ejecución

El programa se ejecuta con el siguiente formato:

./prog <n> <mode> <threads_or_gridsize>

Parámetros:
<n>: Tamaño del arreglo a ordenar.
<mode>: Modo de ejecución:
        0: MergeSort Paralelo en CPU.
        1: Radix Sort en GPU.
        2: std::sort en CPU.
<threads_or_gridsize>:
        Número de hilos para CPU (modo 0).
        Tamaño de la grilla para GPU (modo 1).

# Modo de ejecucion segun el benchmark

# benchmark a
Para el primer benchmark **Tiempo (y) vs n (x)**, al ir cambiando el tamaño del array **n** de manera dinamica (debe ser el mismo valor base de n con los mismos patrones de incrementos para ver resultados comparables), tanto los threads en CPU, como gridsize en GPU, se mantienen
fijos de manera estatica en el programa, por lo que la ejecucion para este benchmark es la siguiente:

./prog <n> 0 0  --> para la CPU
./prog <n> 1 0  --> para la GPU

**Nota**
Por defecto, para este benchmark se usan 8 hilos de CPU y un gridsize para la GPU de 256 (coincide con el blocksize que tambien es fijo de 256)

# benchmark b
Para este segundo benchmark que es solo en CPU **Speedup y vs num-threads (x)**, el tamaño **n** del array es fijo y tiene que ser la entrada mas grande 
de todos los benchmark (ya que se pide  un **n** suficientemente alto), aca lo que varia es el numero de threads a usar (idealmente el tope es 8), al ejecucion es la siguiente:
./prog <n_max> 0 <k>

donde <n_max> es el tamaño max del array y <k> es la cantidad dinamica de threads a usar 

# benchmark c
Este benchmark no se ejecuta, ya que depende del benchmark b, para ver sus resultados basta con ejecutar el script de jupyter.

# benchmark d
Este benchmark que es para GPU **Speedup y vs num-bloques (x)** para ejecutarse se hace mediante un comando en bash (el script se llama benchmark.sh), ya que son 140 iteraciones. Este benchmark tambien se iteria sobre un tamaño de array maximo. 
La ejecucion de este benchmark es el siguiente:

./benchmark.sh 1000000000 1 

**Nota**
Se omite el gridsize ya que este se encuentra en las iteraciones

# benchmark e
Este benchmark no se ejecuta (al igual que el c) ya que depende del benchmark d, para ver los reusltados basta con ejecutar el script en jupyter.

# benchmark f
Para este benchmark **Speedup vs n** se ejecuta solo el algoritmo de sort, que se comparara con los resultados del benchmark 'a', por eso es ideal
que la entrada <n> para este algoritmo siga el mismo patron de incremento que el benchmark 'a'. La ejecucion de este programa es el siguiente:
./prog <n> 2 <k>
donde <n> es el tamaño del array y <k> un valor numerico cualquiera, ya que no influye en el sort (no se utiliza).

# Consideraciones  

1- Para los benchmark b y d se uso un tamaño 10^9 del array, ya que es el maximo posible, al sobrepasarse da error, como por ejemplo este:
    terminate called after throwing an instance of 'std::bad_array_new_length'
        what():  std::bad_array_new_length
    Aborted
2- Para el resto de benchmark (a,c y e) se usaron valores con los siguiente patrones: 10^3,(10^3)*3 , (10^3)*5, (10^3)*7...(10^8),(10^8)*3,(10^8)*5,(10^8)*7 , ya que son valores
que donde no hay saltos excesivos en las curvas, al sobrepasarse de esos valores suelen ocurrir saltos que deforman los graficos.