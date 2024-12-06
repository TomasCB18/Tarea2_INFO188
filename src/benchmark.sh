#!/bin/bash

# Verificar que se hayan pasado los parámetros necesarios
if [ $# -lt 2 ]; then
    echo "Usage: $0 <n> <mode>"
    exit 1
fi

# Asignar los valores de los parámetros
n=$1       # Tamaño del arreglo (primer parámetro)
mode=$2    # Modo GPU (segundo parámetro: 0 para CPU, 1 para GPU)

# Crear el archivo CSV si no existe
output_file="../resultados/benchmark_results.csv"
if [ ! -f "$output_file" ]; then
    echo "n,mode,gridsize,time" > "$output_file"
fi

# Loop para ejecutar el programa con gridsize de 1 a 140
for gridsize in {1..140}; do
    echo "Ejecutando con gridsize=$gridsize..."
    ./prog $n $mode $gridsize
done
