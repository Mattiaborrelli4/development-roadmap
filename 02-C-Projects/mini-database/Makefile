# Makefile per Mini Database Engine

CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2
TARGET = minidb
SOURCES = main.c database.c
HEADERS = database.h
OBJECTS = $(SOURCES:.c=.o)
DB_FILE = database.db

# Regola principale
all: $(TARGET)

# Linking
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJECTS)
	@echo ""
	@echo "=========================================="
	@echo "  Compilazione completata!"
	@echo "  Esegui con: ./$(TARGET)"
	@echo "=========================================="
	@echo ""

# Compilazione
%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

# Esecuzione
run: $(TARGET)
	./$(TARGET)

# Pulizia
clean:
	rm -f $(OBJECTS) $(TARGET) $(DB_FILE)
	@echo "Pulizia completata"

# Pulizia file oggetto
clean-obj:
	rm -f $(OBJECTS)
	@echo "File oggetto rimossi"

# Reset database
reset-db:
	rm -f $(DB_FILE)
	@echo "Database resettato"

# Help
help:
	@echo "=========================================="
	@echo "  Mini Database Engine - Makefile"
	@echo "=========================================="
	@echo ""
	@echo "Comandi disponibili:"
	@echo "  make          - Compila il progetto"
	@echo "  make run      - Compila ed esegui"
	@echo "  make clean    - Rimuove tutti i file generati"
	@echo "  make reset-db - Rimuove solo il file database"
	@echo "  make help     - Mostra questo messaggio"
	@echo ""

.PHONY: all run clean clean-obj reset-db help
