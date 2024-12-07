#!/bin/bash

# Verificar que se hayan pasado los parámetros necesarios
if [ $# -lt 2 ]; then
    echo "Usage: $0 <n> <mode>"
    exit 1
fi


n=$1       # Tamaño del arreglo 
mode=$2    # Modo GPU ( 0 para CPU, 1 para GPU)

# crear CSV si no existe
output_file="../resultados/benchmark_results.csv"
if [ ! -f "$output_file" ]; then
    echo "n,mode,gridsize,time" > "$output_file"
fi

# Loop para ejecutar el programa con gridsize de 1 a 140
for gridsize in {1..140}; do
    echo "Ejecutando con gridsize=$gridsize..."
    ./prog $n $mode $gridsize
done

#este script es para el benchmark e), no se compila, simplemente se hace ./benchmark.sh 1000000000 1 (se empieza del 1)
#dejar todo esto como esta , solo cambiar el largo del array 