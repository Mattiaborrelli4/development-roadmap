# Makefile per BigInt Calculator
# Per Linux/macOS con GCC/Clang

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
TARGET = bigint_calc
SOURCES = main.cpp bigint.cpp
OBJECTS = $(SOURCES:.cpp=.o)
HEADERS = bigint.h

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

%.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(OBJECTS) $(TARGET)

help:
	@echo "Comandi disponibili:"
	@echo "  make          - Compila il progetto"
	@echo "  make run      - Compila ed esegue"
	@echo "  make clean    - Rimuove i file compilati"
	@echo "  make help     - Mostra questo messaggio"
