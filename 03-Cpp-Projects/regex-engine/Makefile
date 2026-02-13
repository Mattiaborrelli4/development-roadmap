# Makefile per Regex Engine
# Supporto per Linux e macOS

# Compilatore
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
LDFLAGS =

# Nome eseguibile
TARGET = regex

# Directory
SRC_DIR = .
BUILD_DIR = build

# File sorgenti
SOURCES = regex.cpp nfa.cpp dfa.cpp main.cpp

# File oggetto
OBJECTS = $(addprefix $(BUILD_DIR)/,$(SOURCES:.cpp=.o))

# Dipendenze
DEPENDS = $(addprefix $(BUILD_DIR)/,$(SOURCES:.cpp=.d))

# Colori per output
COLOR_RESET = \033[0m
COLOR_BOLD = \033[1m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_BLUE = \033[34m

# Regola principale
all: $(TARGET)
	@echo "$(COLOR_BOLD)$(COLOR_GREEN)✓ Build completata!$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)Eseguibile: ./$(TARGET)$(COLOR_RESET)"
	@echo ""

# Linking
$(TARGET): $(OBJECTS)
	@echo "$(COLOR_BOLD)Linking $(TARGET)...$(COLOR_RESET)"
	$(CXX) $(LDFLAGS) $^ -o $(TARGET)

# Compilazione
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BUILD_DIR)
	@echo "$(COLOR_YELLOW)Compiling $<...$(COLOR_RESET)"
	$(CXX) $(CXXFLAGS) -MMD -MP -c $< -o $@

# Includi dipendenze
-include $(DEPENDS)

# Esegui test
test: $(TARGET)
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)Esecuzione test...$(COLOR_RESET)"
	@echo ""
	./$(TARGET) test

# Modalità interattiva
run: $(TARGET)
	./$(TARGET) interactive

# Clean
clean:
	@echo "$(COLOR_BOLD)Pulizia file...$(COLOR_RESET)"
	rm -rf $(BUILD_DIR)
	rm -f $(TARGET)
	@echo "$(COLOR_GREEN)✓ Clean completato$(COLOR_RESET)"

# Help
help:
	@echo "$(COLOR_BOLD)════════════════════════════════════════$(COLOR_RESET)"
	@echo "$(COLOR_BOLD)  Regex Engine - Makefile$(COLOR_RESET)"
	@echo "$(COLOR_BOLD)════════════════════════════════════════$(COLOR_RESET)"
	@echo ""
	@echo "Target disponibili:"
	@echo "  $(COLOR_GREEN)make$(COLOR_RESET)          - Compila il progetto"
	@echo "  $(COLOR_GREEN)make test$(COLOR_RESET)     - Compila e esegui i test"
	@echo "  $(COLOR_GREEN)make run$(COLOR_RESET)      - Compila e avvia modalità interattiva"
	@echo "  $(COLOR_GREEN)make clean$(COLOR_RESET)    - Rimuovi file compilati"
	@echo "  $(COLOR_GREEN)make help$(COLOR_RESET)     - Mostra questo help"
	@echo ""
	@echo "Pattern supportati:"
	@echo "  .  - Qualsiasi carattere"
	@echo "  *  - Zero o più"
	@echo "  +  - Uno o più"
	@echo "  ?  - Zero o uno"
	@echo "  ^  - Inizio stringa"
	@echo "  $  - Fine stringa"
	@echo ""
	@echo "Esempi:"
	@echo "  ./regex test"
	@echo "  ./regex interactive"
	@echo ""

# Phony targets
.PHONY: all test run clean help
