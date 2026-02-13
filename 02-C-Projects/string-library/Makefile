# ================================================
# MAKEFILE - Libreria Stringhe C
# ================================================
# Facilita la compilazione e il testing del progetto
#
# Uso:
#   make          - Compila tutto
#   make test     - Compila ed esegui i test
#   make clean    - Rimuovi file compilati
#   make lib      - Crea libreria statica
#   make help     - Mostra aiuto
# ================================================

# Compilatore
CC = gcc

# Flag di compilazione
CFLAGS = -Wall -Wextra -std=c99 -O2

# Nome del programma di test
TEST_PROG = test_stringlib

# Nome della libreria statica
LIB_NAME = libstringlib.a

# File sorgente
LIB_SRC = stringlib.c
LIB_HDR = stringlib.h
TEST_SRC = test_stringlib.c

# File oggetto
LIB_OBJ = stringlib.o

# ================================================
# TARGET: all (default)
# ================================================
all: $(TEST_PROG)

	@echo ""
	@echo "=========================================="
	@echo "Compilazione completata con successo!"
	@echo "=========================================="
	@echo ""
	@echo "Per eseguire i test:"
	@echo "  ./"$(TEST_PROG)"          (Linux/Mac)"
	@echo "  "$(TEST_PROG)".exe        (Windows)"
	@echo ""

# ================================================
# TARGET: test - Compila ed esegui
# ================================================
test: $(TEST_PROG)
	@echo ""
	@echo "Esecuzione dei test..."
	@echo ""
	@./$(TEST_PROG)

# ================================================
# TARGET: Compilazione programma di test
# ================================================
$(TEST_PROG): $(TEST_SRC) $(LIB_SRC) $(LIB_HDR)
	@echo "Compilazione di $(TEST_PROG)..."
	$(CC) $(CFLAGS) $(TEST_SRC) $(LIB_SRC) -o $(TEST_PROG)

# ================================================
# TARGET: lib - Crea libreria statica
# ================================================
lib: $(LIB_OBJ)
	@echo "Creazione libreria statica $(LIB_NAME)..."
	ar rcs $(LIB_NAME) $(LIB_OBJ)
	@echo "Libreria creata: $(LIB_NAME)"

# ================================================
# TARGET: File oggetto per la libreria
# ================================================
$(LIB_OBJ): $(LIB_SRC) $(LIB_HDR)
	@echo "Compilazione di $(LIB_SRC)..."
	$(CC) $(CFLAGS) -c $(LIB_SRC) -o $(LIB_OBJ)

# ================================================
# TARGET: clean - Pulisci file compilati
# ================================================
clean:
	@echo "Pulizia file compilati..."
	@rm -f $(TEST_PROG) $(TEST_PROG).exe $(LIB_OBJ) $(LIB_NAME)
	@echo "Pulizia completata."

# ================================================
# TARGET: help - Mostra aiuto
# ================================================
help:
	@echo ""
	@echo "=========================================="
	@echo "  MAKEFILE - Libreria Stringhe C"
	@echo "=========================================="
	@echo ""
	@echo "Target disponibili:"
	@echo ""
	@echo "  make          - Compila il programma di test"
	@echo "  make test     - Compila ed esegui i test"
	@echo "  make lib      - Crea libreria statica"
	@echo "  make clean    - Rimuovi file compilati"
	@echo "  make help     - Mostra questo messaggio"
	@echo ""
	@echo "Esempi:"
	@echo "  make test     (compila + esegui)"
	@echo "  make lib      (crea libstringlib.a)"
	@echo ""
	@echo "Per usare la libreria nel tuo codice:"
	@echo "  #include \"stringlib.h\""
	@echo "  gcc tuofile.c stringlib.c -o tuofile"
	@echo ""

# ================================================
# TARGET: install - Installa la libreria (opzionale)
# ================================================
install: lib
	@echo "Installazione libreria..."
	@mkdir -p ../lib
	@mkdir -p ../include
	@cp $(LIB_NAME) ../lib/
	@cp $(LIB_HDR) ../include/
	@echo "Libreria installata in ../lib e ../include"

# ================================================
# PHONY - Target non file
# ================================================
.PHONY: all test lib clean help install
