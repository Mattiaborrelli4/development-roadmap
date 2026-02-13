# Makefile per Custom STL Containers
# C++17 Project con MyVector, MyLinkedList e Algorithms

# Compilatori
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic -O2

# Target
TARGET = custom_stl

# File sorgente
SOURCES = main.cpp

# File oggetto
OBJECTS = $(SOURCES:.cpp=.o)

# Header files (dipendenze)
HEADERS = vector.h vector.tpp list.h list.tpp algorithms.h

# Regola di default
all: $(TARGET)

# Linking
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)
	@echo ""
	@echo "Compilazione completata! Esegui con: ./$(TARGET)"
	@echo ""

# Compilazione
%.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Esecuzione
run: $(TARGET)
	./$(TARGET)

# Debug build
debug: CXXFLAGS += -g -fsanitize=address -fsanitize=undefined
debug: clean $(TARGET)
	@echo "Debug build creato con sanitizers"

# Clean
clean:
	rm -f $(OBJECTS) $(TARGET)
	@echo "Clean completato"

# Phony targets
.PHONY: all run debug clean

# Dipendenze
main.o: main.cpp vector.h list.h algorithms.h
