# Makefile per Mini-Zip
# Utility di Compressione File RLE

# Compilatore
CC = gcc

# Flag di compilazione
CFLAGS = -Wall -Wextra -O2 -std=c99

# Nome dell'eseguibile
TARGET = mini-zip

# File sorgente
SRC = mini-zip.c

# File oggetto
OBJ = $(SRC:.c=.o)

# Regola principale: costruire l'eseguibile
all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

# Regola per il debugging
debug: CFLAGS += -g -DDEBUG
debug: clean $(TARGET)

# Regola per pulire i file compilati
clean:
	del /Q $(TARGET) *.o 2>nul || true

# Regola per eseguire il programma
run: $(TARGET)
	$(TARGET)

# Regola per installare il programma (solo Unix-like)
install: $(TARGET)
	install -m 755 $(TARGET) /usr/local/bin/

# Regola per disinstallare (solo Unix-like)
uninstall:
	rm -f /usr/local/bin/$(TARGET)

# Regola di aiuto
help:
	@echo "Mini-Zip Makefile"
	@echo ""
	@echo "Target disponibili:"
	@echo "  make          - Compila il programma"
	@echo "  make all      - Compila il programma (stesso di sopra)"
	@echo "  make debug    - Compila con simboli di debug"
	@echo "  make clean    - Rimuove i file compilati"
	@echo "  make run      - Compila ed esegue il programma"
	@echo "  make help     - Mostra questo messaggio"

.PHONY: all debug clean run install uninstall help
