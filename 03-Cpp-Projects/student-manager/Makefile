# Makefile per Student Management System
# Compilatore: g++

# Nome dell'eseguibile
TARGET = student_manager

# File sorgente
SOURCES = main.cpp student.cpp

# File object
OBJECTS = $(SOURCES:.cpp=.o)

# File header
HEADERS = student.h

# Compilatore
CXX = g++

# Flag di compilazione
CXXFLAGS = -Wall -Wextra -std=c++11

# Regola principale: compila tutto
all: $(TARGET)

# Linkaggio
$(TARGET): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $(TARGET)
	@echo ""
	@echo "=========================================="
	@echo "  Compilazione completata con successo!"
	@echo "  Eseguibile: $(TARGET).exe"
	@echo "  Per eseguire: .\$(TARGET).exe"
	@echo "=========================================="
	@echo ""

# Compilazione dei file sorgente
%.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Esecuzione del programma
run: $(TARGET)
	@echo "Avvio del programma..."
	./$(TARGET).exe

# Pulizia dei file compilati
clean:
	@echo "Pulizia in corso..."
	del /Q *.o 2>nul
	del /Q $(TARGET).exe 2>nul
	@echo "Pulizia completata!"

# Pulizia completa (incluso file di dati)
cleanall: clean
	@echo "Pulizia completa in corso..."
	del /Q students.txt 2>nul
	del /Q test_students.txt 2>nul
	@echo "Pulizia completa completata!"

# Test rapido
test: $(TARGET)
	@echo "Creazione file di test..."
	@echo 1,Mario,Rossi,20,Informatica,28.5 > test_students.txt
	@echo 2,Laura,Bianchi,21,Matematica,29.0 >> test_students.txt
	@echo 3,Giuseppe,Verdi,22,Fisica,27.5 >> test_students.txt
	@echo ""
	@echo "File test_students.txt creato!"
	@echo "Avvio del programma con dati di test..."
	@echo ""
	./$(TARGET).exe

# Help
help:
	@echo "=========================================="
	@echo "  Makefile - Student Management System"
	@echo "=========================================="
	@echo ""
	@echo "Comandi disponibili:"
	@echo "  make        - Compila il programma"
	@echo "  make all    - Compila il programma (steso di make)"
	@echo "  make run    - Compila ed esegue"
	@echo "  make test   - Crea file di test ed esegue"
	@echo "  make clean  - Rimuove i file compilati"
	@echo "  make cleanall- Rimuove tutto (inclusi dati)"
	@echo "  make help   - Mostra questo aiuto"
	@echo ""

.PHONY: all run clean cleanall test help
