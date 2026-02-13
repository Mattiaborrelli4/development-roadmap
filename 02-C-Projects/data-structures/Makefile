# Makefile per Data Structures Library
# Autore: Matti
# Anno: 2026

# Compilatore
CC = gcc

# Flag di compilazione
CFLAGS = -Wall -Wextra -std=c99

# File sorgenti
SOURCES = main.c list.c stack.c queue.c hashtable.c

# File oggetto
OBJECTS = $(SOURCES:.c=.o)

# Eseguibile
TARGET = datastructures

# Regola principale: compila tutto
all: $(TARGET)

# Linking
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o $(TARGET)
	@echo "\n=========================================="
	@echo "  Compilazione completata con successo!"
	@echo "  Esegui con: ./$(TARGET)"
	@echo "==========================================\n"

# Compilazione dei file .c in .o
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Esegue il programma
run: $(TARGET)
	./$(TARGET)

# Pulisce i file oggetto e l'eseguibile
clean:
	rm -f $(OBJECTS) $(TARGET)
	@echo "Pulizia completata!"

# Pulisce e ricompila tutto
rebuild: clean all

# Help
help:
	@echo "=========================================="
	@echo "  Data Structures Library - Makefile"
	@echo "=========================================="
	@echo ""
	@echo "Comandi disponibili:"
	@echo "  make          - Compila il progetto"
	@echo "  make all      - Compila il progetto"
	@echo "  make run      - Compila e esegue"
	@echo "  make clean    - Rimuove file oggetto ed eseguibile"
	@echo "  make rebuild  - Pulisce e ricompila tutto"
	@echo "  make help     - Mostra questo messaggio"
	@echo ""
	@echo "File nel progetto:"
	@echo "  list.c/h      - Linked List implementation"
	@echo "  stack.c/h     - Stack implementation"
	@echo "  queue.c/h     - Queue implementation"
	@echo "  hashtable.c/h - Hash Table implementation"
	@echo "  main.c        - Test program"
	@echo ""

# Phony targets
.PHONY: all run clean rebuild help
