# Makefile per HTTP Server in C
# Supporto multipiattaforma: Windows (MinGW) e Linux (GCC)

# Rileva il sistema operativo
ifeq ($(OS),Windows_NT)
    # Windows
    CC = gcc
    TARGET = server.exe
    CFLAGS = -Wall -Wextra -O2
    LDFLAGS = -lws2_32
    RM = del /Q
    MKDIR = if not exist $(subst /,\,$(1)) mkdir $(subst /,\,$(1))
else
    # Linux/Unix
    CC = gcc
    TARGET = server
    CFLAGS = -Wall -Wextra -O2 -pthread
    LDFLAGS = -pthread
    RM = rm -f
    MKDIR = mkdir -p $(1)
endif

# Directory
SRC_DIR = .
BUILD_DIR = build
PUBLIC_DIR = public

# File sorgente
SRC = server.c
OBJ = $(BUILD_DIR)/server.o

# Regola principale
all: $(BUILD_DIR) $(PUBLIC_DIR) $(TARGET)

$(BUILD_DIR):
	$(call MKDIR,$(BUILD_DIR))

$(PUBLIC_DIR):
	$(call MKDIR,$(PUBLIC_DIR))

# Compilazione
$(OBJ): $(SRC)
	$(CC) $(CFLAGS) -c $< -o $@

# Linking
$(TARGET): $(OBJ)
	$(CC) $(OBJ) $(LDFLAGS) -o $@
	@echo ""
	@echo "=========================================="
	@echo "Compilazione completata!"
	@echo "Eseguibile: $(TARGET)"
	@echo "=========================================="
	@echo ""

# Pulizia
clean:
	$(RM) $(BUILD_DIR)/*.o $(TARGET) 2>nul || true
	@echo "Pulizia completata"

# Esegui
run: $(TARGET)
	./$(TARGET)

# Esegui con porta personalizzata
run-port: $(TARGET)
	@echo "Uso: make run-port PORT=9090"
	./$(TARGET) $(PORT)

# Help
help:
	@echo "Makefile per HTTP Server"
	@echo ""
	@echo "Target disponibili:"
	@echo "  make          - Compila il server"
	@echo "  make all      - Compila il server (stesso di make)"
	@echo "  make clean    - Rimuovi i file compilati"
	@echo "  make run      - Compila e esegui il server"
	@echo "  make run-port - Esegui con porta personalizzata (es: make run-port PORT=9090)"
	@echo "  make help     - Mostra questo messaggio"
	@echo ""
	@echo "Esempi:"
	@echo "  make              - Compila il server"
	@echo "  make run          - Compila e avvia il server"
	@echo "  make run-port PORT=3000 - Avvia il server sulla porta 3000"

.PHONY: all clean run run-port help
