# ============================================================================
# Makefile per Snake Game - Linux/macOS
# ============================================================================
# Questo Makefile facilita la compilazione e gestione del progetto
# Uso: make, make run, make clean, make help
# ============================================================================

# Variabili di configurazione
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic
TARGET = snake
SOURCE = ConsoleGame.cpp
OBJECTS = $(SOURCE:.cpp=.o)

# Colori per output
COLOR_RESET = \033[0m
COLOR_BOLD = \033[1m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_BLUE = \033[34m

# Phony targets (non creano file)
.PHONY: all run clean help debug release

# Target principale
all: $(TARGET)
	@echo "$(COLOR_GREEN)✓ Compilazione completata!$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)Esegui con: ./$(TARGET)$(COLOR_RESET)"

# Linking
$(TARGET): $(OBJECTS)
	@echo "$(COLOR_YELLOW)Linking in corso...$(COLOR_RESET)"
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)
	@echo "$(COLOR_GREEN)✓ Linking completato$(COLOR_RESET)"

# Compilazione
%.o: %.cpp
	@echo "$(COLOR_YELLOW)Compilazione di $<...$(COLOR_RESET)"
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Esecuzione
run: $(TARGET)
	@echo "$(COLOR_BLUE)Avvio del gioco...$(COLOR_RESET)"
	./$(TARGET)

# Debug build
debug: CXXFLAGS += -g -O0 -DDEBUG
debug: clean $(TARGET)
	@echo "$(COLOR_GREEN)✓ Build debug completata$(COLOR_RESET)"

# Release build
release: CXXFLAGS += -O3 -DNDEBUG
release: clean $(TARGET)
	@echo "$(COLOR_GREEN)✓ Build release completata$(COLOR_RESET)"

# Pulizia
clean:
	@echo "$(COLOR_YELLOW)Pulizia in corso...$(COLOR_RESET)"
	rm -f $(OBJECTS) $(TARGET)
	@echo "$(COLOR_GREEN)✓ Pulizia completata$(COLOR_RESET)"

# Help
help:
	@echo "$(COLOR_BOLD)Snake Game - Makefile$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BOLD)Comandi disponibili:$(COLOR_RESET)"
	@echo "  $(COLOR_GREEN)make$(COLOR_RESET)          - Compila il progetto"
	@echo "  $(COLOR_GREEN)make run$(COLOR_RESET)       - Compila ed esegui il gioco"
	@echo "  $(COLOR_GREEN)make debug$(COLOR_RESET)     - Compila con simboli di debug"
	@echo "  $(COLOR_GREEN)make release$(COLOR_RESET)   - Compila con ottimizzazioni"
	@echo "  $(COLOR_GREEN)make clean$(COLOR_RESET)     - Rimuove i file compilati"
	@echo "  $(COLOR_GREEN)make help$(COLOR_RESET)      - Mostra questo messaggio"
	@echo ""
	@echo "$(COLOR_BOLD)Esempi:$(COLOR_RESET)"
	@echo "  make           # Compila"
	@echo "  make run       # Compila e gioca"
	@echo "  make clean all # Ricompila tutto"
	@echo ""

# Dipendenze automatiche
-include $(OBJECTS:.o=.d)

# Genera dipendenze
%.d: %.cpp
	@$(CXX) $(CXXFLAGS) -MM -MT '$*.o $*.d' $< > $@

# Informazioni
info:
	@echo "$(COLOR_BOLD)Informazioni di compilazione:$(COLOR_RESET)"
	@echo "  Compilatore: $(CXX)"
	@echo "  Flag: $(CXXFLAGS)"
	@echo "  Target: $(TARGET)"
	@echo "  Sorgenti: $(SOURCE)"
	@echo ""
