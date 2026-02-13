# Makefile per Dynamic Array Project
# Educational Project - Array Dinamico in C

# Compilatore
CC = gcc

# Flag di compilazione
CFLAGS = -Wall -Wextra -std=c99 -pedantic

# Flag per il debugging
# Se vuoi usare valgrind, non usare -O
CFLAGS_DEBUG = -g -O0 -Wall -Wextra -std=c99

# Flag per il profiling (performance)
CFLAGS_PROFILE = -pg -O2 -Wall -Wextra -std=c99

# Nome dell'eseguibile
TARGET = dynamic_array_test

# File sorgenti
SOURCES = main.c dynamic_array.c

# File oggetto
OBJECTS = $(SOURCES:.c=.o)

# File header
HEADERS = dynamic_array.h

# ============================================================
# REGOLE PRINCIPALI
# ============================================================

# Target di default
all: $(TARGET)

# Linking
$(TARGET): $(OBJECTS)
	@echo "Linking di $@..."
	$(CC) $(CFLAGS) -o $@ $(OBJECTS)
	@echo "Build completato con successo!"
	@echo "Esegui con: ./$@"
	@echo ""

# Compilazione file oggetto
%.o: %.c $(HEADERS)
	@echo "Compilazione di $<..."
	$(CC) $(CFLAGS) -c $< -o $@

# Build debug (per valgrind/gdb)
debug: clean
	@echo "Build in modalità DEBUG..."
	$(CC) $(CFLAGS_DEBUG) -c dynamic_array.c -o dynamic_array.o
	$(CC) $(CFLAGS_DEBUG) -c main.c -o main.o
	$(CC) $(CFLAGS_DEBUG) -o $(TARGET) $(OBJECTS)
	@echo "Build debug completato!"
	@echo "Puoi usare: valgrind --leak-check=full ./$@"
	@echo ""

# Build con profiling
profile: clean
	@echo "Build in modalità PROFILING..."
	$(CC) $(CFLAGS_PROFILE) -c dynamic_array.c -o dynamic_array.o
	$(CC) $(CFLAGS_PROFILE) -c main.c -o main.o
	$(CC) $(CFLAGS_PROFILE) -o $(TARGET) $(OBJECTS)
	@echo "Build profiling completato!"
	@echo "Esegui: ./$@"
	@echo "Poi: gprof $(TARGET) gmon.out > analysis.txt"
	@echo ""

# Esecuzione del programma
run: $(TARGET)
	@echo "Esecuzione del programma..."
	@echo "=============================================="
	./$(TARGET)

# Esecuzione con valgrind (check memory leaks)
valgrind: $(TARGET)
	@echo "Esecuzione con Valgrind per memory leak check..."
	@echo "=============================================="
	valgrind --leak-check=full \
	         --show-leak-kinds=all \
	         --track-origins=yes \
	         --verbose \
	         --log-file=valgrind-out.txt \
	         ./$(TARGET)
	@echo ""
	@echo "Risultato Valgrind salvato in valgrind-out.txt"
	@echo "Controlla 'definitely lost' - dovrebbe essere 0 bytes!"

# Esecuzione con gdb
gdb: $(TARGET)
	@echo "Avvio GDB..."
	gdb ./$(TARGET)

# Pulizia file oggetto e eseguibili
clean:
	@echo "Pulizia..."
	rm -f $(OBJECTS) $(TARGET) gmon.out
	@echo "Pulizia completata!"

# Pulizia completa (inclusi file di debug)
cleanall: clean
	@echo "Pulizia completa..."
	rm -f valgrind-out.txt analysis.txt
	@echo "Tutto pulito!"

# ============================================================
# UTILITÀ
# ============================================================

# Mostra le informazioni di build
info:
	@echo "Informazioni Build:"
	@echo "  Compilatore: $(CC)"
	@echo "  Flag: $(CFLAGS)"
	@echo "  Sorgenti: $(SOURCES)"
	@echo "  Target: $(TARGET)"
	@echo ""
	@echo "Target disponibili:"
	@echo "  make          - Build normale"
	@echo "  make debug    - Build con simboli debug"
	@echo "  make profile  - Build con profiling"
	@echo "  make run      - Compila ed esegui"
	@echo "  make valgrind - Esegui con valgrind"
	@echo "  make gdb      - Esegui con gdb"
	@echo "  make clean    - Rimuovi file oggetto"
	@echo "  make info     - Mostra questo messaggio"

# Help
help: info

# Phony targets (non corrispondono a file reali)
.PHONY: all debug profile run valgrind gdb clean cleanall info help
