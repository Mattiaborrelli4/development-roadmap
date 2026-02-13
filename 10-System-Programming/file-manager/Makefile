# =============================================
# Makefile per File Manager
# =============================================

# Compilatore
CC = gcc

# Flag di compilazione
CFLAGS = -Wall -Wextra -std=c99 -pedantic

# Nome dell'eseguibile
TARGET = file_manager

# File sorgenti
SOURCES = file_manager.c

# File oggetto
OBJECTS = $(SOURCES:.c=.o)

# Regola principale: compila tutto
all: $(TARGET)

# Linking
$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(TARGET)
	@echo ""
	@echo "=========================================="
	@echo "✓ Compilazione completata con successo!"
	@echo "✓ Eseguibile creato: $(TARGET)"
	@echo "=========================================="
	@echo ""
	@echo "Per eseguire il programma:"
	@echo "  ./$(TARGET)"
	@echo ""

# Compilazione
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Esecuzione
run: $(TARGET)
	./$(TARGET)

# Pulizia
clean:
	rm -f $(OBJECTS) $(TARGET)
	@echo "✓ File oggetto ed eseguibili rimossi"

# Installazione (opzionale)
install: $(TARGET)
	@echo "Installa $(TARGET) in /usr/local/bin (richiede sudo)"
	@sudo cp $(TARGET) /usr/local/bin/

# Disinstallazione
uninstall:
	@echo "Rimuove $(TARGET) da /usr/local/bin (richiede sudo)"
	@sudo rm -f /usr/local/bin/$(TARGET)

# Help
help:
	@echo "Target disponibili:"
	@echo "  all        - Compila il progetto (default)"
	@echo "  run        - Compila ed esegue il programma"
	@echo "  clean      - Rimuove i file compilati"
	@echo "  install    - Installa il programma in /usr/local/bin"
	@echo "  uninstall  - Rimuove il programma da /usr/local/bin"
	@echo "  help       - Mostra questo messaggio"

.PHONY: all run clean install uninstall help
