TARGET = prog


SRCS = prog.cu


NVCC = nvcc


NVCC_FLAGS = -Xcompiler -fopenmp -std=c++11 -O3


all: $(TARGET)


$(TARGET): $(SRCS)
	$(NVCC) $(NVCC_FLAGS) -o $@ $^


clean:
	rm -f $(TARGET)
