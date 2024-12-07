#!/bin/bash

# Nombre del programa
PROGRAM="./prog"

# Validar que el programa existe
if [ ! -f "$PROGRAM" ]; then
    echo "Error: El programa $PROGRAM no existe en el directorio actual."
    exit 1
fi


MODE=2       # cambiar al modo segun se quiera usar (0,1 o 2)
THREADS=0    # numero de hilos/gridsize (0 para automático)

# Tamaños de entrada (logarítmico: 10^3, 2*10^3, ..., 10^8)
SIZES=( 
    1000 2000 5000 10000 20000 50000 100000 200000 500000 1000000 
    2000000 5000000 10000000 20000000 50000000 100000000
)


REPEATS=10  # 10 tamaños * 10 repeticiones = 100 experimentos

#EJECUTAR COMO: ./benchmark_af.sh

# Iterar sobre cada tamaño de entrada
for SIZE in "${SIZES[@]}"; do
    for ((i = 1; i <= REPEATS; i++)); do
        echo "Ejecutando experimento: n=$SIZE, modo=$MODE, threads=$THREADS (Repetición $i)..."
        
        # captar tiempo de ejecucion
        START_TIME=$(date +%s.%N)
        $PROGRAM $SIZE $MODE $THREADS
        END_TIME=$(date +%s.%N)
        
        TIME=$(echo "$END_TIME - $START_TIME" | bc)
        
        echo "Tiempo de ejecución para n=$SIZE, modo=$MODE, threads=$THREADS (Repetición $i): $TIME segundos"
    done
done

echo "Todos los experimentos han terminado."
