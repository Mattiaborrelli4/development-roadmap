# Mini Vim - Makefile

# Compilatore
CC = gcc

# Flag di compilazione
CFLAGS = -Wall -Wextra -std=c99 -pedantic

# Nome dell'eseguibile
TARGET = mini-vim

# File sorgenti
SOURCES = editor.c buffer.c

# File oggetto
OBJECTS = $(SOURCES:.c=.o)

# Piattaforma detection
ifeq ($(OS),Windows_NT)
    # Windows
    RM = del /Q
    EXE_EXT = .exe
    PLATFORM_FLAGS =
else
    # Unix-like (Linux, macOS)
    RM = rm -f
    EXE_EXT =
    PLATFORM_FLAGS = -lncurses
endif

# Regola di default
all: $(TARGET)$(EXE_EXT)

# Linking
$(TARGET)$(EXE_EXT): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(TARGET)$(EXE_EXT) $(PLATFORM_FLAGS)
	@echo ""
	@echo "Build completato! Eseguibile: $(TARGET)$(EXE_EXT)"
	@echo ""

# Compilazione
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Pulizia
clean:
	$(RM) $(OBJECTS) $(TARGET)$(EXE_EXT)
	@echo "Pulizia completata."

# Esecuzione
run: $(TARGET)$(EXE_EXT)
	./$(TARGET)$(EXE_EXT)

# Debug
debug: CFLAGS += -g -DDEBUG
debug: clean $(TARGET)$(EXE_EXT)

# Install (opzionale)
install: $(TARGET)$(EXE_EXT)
	@echo "Installazione di $(TARGET)..."
ifeq ($(OS),Windows_NT)
	@copy $(TARGET)$(EXE_EXT) C:\Windows\System32\
else
	@sudo cp $(TARGET) /usr/local/bin/
endif
	@echo "Installazione completata."

# Disinstalla
uninstall:
	@echo "Rimozione di $(TARGET)..."
ifeq ($(OS),Windows_NT)
	@del C:\Windows\System32\$(TARGET)$(EXE_EXT)
else
	@sudo rm -f /usr/local/bin/$(TARGET)
endif
	@echo "Rimozione completata."

# Help
help:
	@echo "Mini Vim - Makefile"
	@echo ""
	@echo "Target disponibili:"
	@echo "  make          - Compila il progetto"
	@echo "  make clean    - Rimuove i file oggetto e l'eseguibile"
	@echo "  make run      - Compila ed esegui"
	@echo "  make debug    - Compila con simboli di debug"
	@echo "  make install  - Installa mini-vim nel sistema"
	@echo "  make uninstall - Rimuove mini-vim dal sistema"
	@echo "  make help     - Mostra questo messaggio"

.PHONY: all clean run debug install uninstall help
