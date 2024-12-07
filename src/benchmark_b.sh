#!/bin/bash


PROGRAM="./prog"


if [ ! -f "$PROGRAM" ]; then
    echo "Error: El programa $PROGRAM no existe en el directorio actual."
    exit 1
fi


N=100000000    
REPEATS=12    
MAX_THREADS=8

# iterar el numero de hilos
for THREADS in $(seq 1 $MAX_THREADS); do
    for ((i = 1; i <= REPEATS; i++)); do
        echo "Ejecutando experimento: n=$N, threads=$THREADS (Repetición $i)..."
        $PROGRAM $N 0 $THREADS
    done
done

echo "Todos los experimentos han terminado."
