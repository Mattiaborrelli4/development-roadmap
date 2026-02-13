# Makefile per Mini Shell
# Compatibile con Linux/Unix e Windows (con MinGW)

# Compilatore
CC = gcc

# Flag di compilazione
CFLAGS = -Wall -Wextra -std=c99 -pedantic
LDFLAGS =

# Nome dell'eseguibile
TARGET = mini-shell

# File sorgente
SRC = shell.c
HDR = shell.h
OBJ = $(SRC:.c=.o)

# Sistema operativo detection
ifeq ($(OS),Windows_NT)
    # Windows
    RM = del /Q
    TARGET_EXT = .exe
else
    # Linux/Unix
    RM = rm -f
    TARGET_EXT =
endif

TARGET_FULL = $(TARGET)$(TARGET_EXT)

# Regola principale
all: $(TARGET_FULL)

# Linking
$(TARGET_FULL): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET_FULL) $(LDFLAGS)
	@echo "Compilazione completata: $(TARGET_FULL)"

# Compilazione
%.o: %.c $(HDR)
	$(CC) $(CFLAGS) -c $< -o $@

# Esecuzione
run: $(TARGET_FULL)
	./$(TARGET_FULL)

# Pulizia
clean:
	$(RM) $(OBJ) $(TARGET_FULL) *.stackdump 2>NUL || true

# Installazione (opzionale)
install: $(TARGET_FULL)
	@echo "Installazione di $(TARGET_FULL) in /usr/local/bin"
	@sudo cp $(TARGET_FULL) /usr/local/bin/mini-shell

# Disinstallazione
uninstall:
	@echo "Rimozione di mini-shell da /usr/local/bin"
	@sudo rm -f /usr/local/bin/mini-shell

# Help
help:
	@echo "Mini Shell - Makefile"
	@echo ""
	@echo "Targets disponibili:"
	@echo "  make          - Compila il progetto"
	@echo "  make all      - Compila il progetto (stesso di sopra)"
	@echo "  make run      - Compila ed esegue la shell"
	@echo "  make clean    - Rimuove i file oggetto e l'eseguibile"
	@echo "  make install  - Installa la shell in /usr/local/bin (richiede sudo)"
	@echo "  make uninstall- Rimuove la shell da /usr/local/bin (richiede sudo)"
	@echo "  make help     - Mostra questo messaggio"

.PHONY: all run clean install uninstall help
