# Nombre del ejecutable
TARGET = prog

# Archivos fuente
SRCS = prog.cu

# Compilador
NVCC = nvcc

# Flags para CUDA y OpenMP
NVCC_FLAGS = -Xcompiler -fopenmp -std=c++11 -O3

# Regla por defecto
all: $(TARGET)

# Compilación
$(TARGET): $(SRCS)
	$(NVCC) $(NVCC_FLAGS) -o $@ $^

# Limpieza
clean:
	rm -f $(TARGET)
