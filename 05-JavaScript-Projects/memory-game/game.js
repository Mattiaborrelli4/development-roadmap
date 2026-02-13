/**
 * ========================================
 * GIOCO DI MEMORIA
 * ========================================
 * Un gioco di carte memoria in JavaScript puro
 * con animazioni 3D, sistema di punteggio
 * e livelli di difficoltà
 */

class MemoryGame {
    /**
     * Inizializza il gioco di memoria
     * @param {string} boardId - ID dell'elemento contenitore del gioco
     */
    constructor(boardId) {
        this.board = document.getElementById(boardId);
        this.cards = [];
        this.flippedCards = [];
        this.matchedPairs = 0;
        this.moves = 0;
        this.timer = null;
        this.seconds = 0;
        this.gameStarted = false;
        this.isLocked = false;
        this.difficulty = 'easy';

        // Simboli per le carte (emoji)
        this.symbols = [
            '🍎', '🍊', '🍋', '🍇', '🍓', '🍒',
            '🥝', '🍑', '🥭', '🍍', '🥥', '🍌',
            '🫐', '🍈', '🍉', '🫒', '🥑', '🍆'
        ];

        // Elementi DOM
        this.movesElement = document.getElementById('moves');
        this.timerElement = document.getElementById('timer');
        this.pairsElement = document.getElementById('pairs');
        this.difficultySelect = document.getElementById('difficulty');
        this.restartBtn = document.getElementById('restartBtn');
        this.winModal = document.getElementById('winModal');
        this.playAgainBtn = document.getElementById('playAgainBtn');

        // Elementi finali modale
        this.finalMovesElement = document.getElementById('finalMoves');
        this.finalTimeElement = document.getElementById('finalTime');
        this.finalDifficultyElement = document.getElementById('finalDifficulty');

        this.init();
    }

    /**
     * Inizializza il gioco
     */
    init() {
        // Aggiungi event listeners
        this.difficultySelect.addEventListener('change', (e) => {
            this.difficulty = e.target.value;
            this.restartGame();
        });

        this.restartBtn.addEventListener('click', () => this.restartGame());
        this.playAgainBtn.addEventListener('click', () => {
            this.winModal.classList.add('hidden');
            this.restartGame();
        });

        // Avvia il gioco
        this.startGame();
    }

    /**
     * Avvia una nuova partita
     */
    startGame() {
        // Resetta lo stato del gioco
        this.resetState();

        // Determina il numero di coppie in base alla difficoltà
        const totalPairs = this.difficulty === 'easy' ? 8 : 18;
        this.totalPairs = totalPairs;

        // Aggiorna il display delle coppie
        this.pairsElement.textContent = `0 / ${totalPairs}`;

        // Seleziona i simboli per questo gioco
        const selectedSymbols = this.symbols.slice(0, totalPairs);

        // Crea le coppie di carte
        const cardPairs = [...selectedSymbols, ...selectedSymbols];

        // Mischia le carte
        this.shuffleCards(cardPairs);

        // Crea il board di gioco
        this.createBoard(cardPairs);
    }

    /**
     * Resetta lo stato del gioco
     */
    resetState() {
        // Ferma il timer
        this.stopTimer();

        // Resetta le variabili
        this.cards = [];
        this.flippedCards = [];
        this.matchedPairs = 0;
        this.moves = 0;
        this.seconds = 0;
        this.gameStarted = false;
        this.isLocked = false;

        // Resetta il display
        this.movesElement.textContent = '0';
        this.timerElement.textContent = '00:00';

        // Rimuovi la classe di difficoltà dal board
        this.board.classList.remove('easy', 'hard');
        this.board.classList.add(this.difficulty);

        // Svuota il board
        this.board.innerHTML = '';
    }

    /**
     * Mischia le carte usando l'algoritmo Fisher-Yates
     * @param {Array} cards - Array delle carte da mischiare
     */
    shuffleCards(cards) {
        for (let i = cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cards[i], cards[j]] = [cards[j], cards[i]];
        }
        return cards;
    }

    /**
     * Crea il board di gioco con le carte
     * @param {Array} cards - Array delle carte
     */
    createBoard(cards) {
        cards.forEach((symbol, index) => {
            const card = this.createCard(symbol, index);
            this.board.appendChild(card);
            this.cards.push(card);
        });
    }

    /**
     * Crea un elemento carta
     * @param {string} symbol - Simbolo della carta
     * @param {number} index - Indice della carta
     * @returns {HTMLElement} Elemento carta
     */
    createCard(symbol, index) {
        const card = document.createElement('div');
        card.classList.add('card');
        card.dataset.index = index;
        card.dataset.symbol = symbol;

        // Crea le facce della carta
        const frontFace = document.createElement('div');
        frontFace.classList.add('card-face', 'card-front');

        const backFace = document.createElement('div');
        backFace.classList.add('card-face', 'card-back');
        backFace.textContent = symbol;

        // Aggiungi le facce alla carta
        card.appendChild(frontFace);
        card.appendChild(backFace);

        // Aggiungi event listener
        card.addEventListener('click', () => this.flipCard(card));

        return card;
    }

    /**
     * Gestisce il click su una carta
     * @param {HTMLElement} card - Elemento carta cliccato
     */
    flipCard(card) {
        // Verifica se il gioco è bloccato o la carta è già girata
        if (
            this.isLocked ||
            card.classList.contains('flipped') ||
            card.classList.contains('matched')
        ) {
            return;
        }

        // Avvia il timer al primo click
        if (!this.gameStarted) {
            this.startTimer();
            this.gameStarted = true;
        }

        // Girala carta
        card.classList.add('flipped');
        this.flippedCards.push(card);

        // Se due carte sono girate, verifica la corrispondenza
        if (this.flippedCards.length === 2) {
            this.incrementMoves();
            this.checkMatch();
        }
    }

    /**
     * Verifica se le due carte girate corrispondono
     */
    checkMatch() {
        this.isLocked = true;

        const [card1, card2] = this.flippedCards;
        const match = card1.dataset.symbol === card2.dataset.symbol;

        if (match) {
            this.handleMatch(card1, card2);
        } else {
            this.handleMismatch(card1, card2);
        }
    }

    /**
     * Gestisce una corrispondenza trovata
     * @param {HTMLElement} card1 - Prima carta
     * @param {HTMLElement} card2 - Seconda carta
     */
    handleMatch(card1, card2) {
        // Aggiungi la classe matched
        setTimeout(() => {
            card1.classList.add('matched');
            card2.classList.add('matched');
            this.matchedPairs++;

            // Aggiorna il display delle coppie
            this.pairsElement.textContent = `${this.matchedPairs} / ${this.totalPairs}`;

            // Resetta le carte girate
            this.flippedCards = [];
            this.isLocked = false;

            // Verifica se il gioco è completato
            if (this.matchedPairs === this.totalPairs) {
                this.handleWin();
            }
        }, 500);
    }

    /**
     * Gestisce una mancata corrispondenza
     * @param {HTMLElement} card1 - Prima carta
     * @param {HTMLElement} card2 - Seconda carta
     */
    handleMismatch(card1, card2) {
        // Aspetta e rigira le carte
        setTimeout(() => {
            card1.classList.remove('flipped');
            card2.classList.remove('flipped');
            this.flippedCards = [];
            this.isLocked = false;
        }, 1000);
    }

    /**
     * Incrementa il contatore delle mosse
     */
    incrementMoves() {
        this.moves++;
        this.movesElement.textContent = this.moves;
    }

    /**
     * Avvia il timer
     */
    startTimer() {
        this.timer = setInterval(() => {
            this.seconds++;
            this.updateTimerDisplay();
        }, 1000);
    }

    /**
     * Ferma il timer
     */
    stopTimer() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    /**
     * Aggiorna il display del timer
     */
    updateTimerDisplay() {
        const minutes = Math.floor(this.seconds / 60);
        const seconds = this.seconds % 60;
        this.timerElement.textContent = `${this.formatTime(minutes)}:${this.formatTime(seconds)}`;
    }

    /**
     * Formatta il tempo
     * @param {number} time - Tempo da formattare
     * @returns {string} Tempo formattato
     */
    formatTime(time) {
        return time < 10 ? `0${time}` : time;
    }

    /**
     * Gestisce la vittoria del gioco
     */
    handleWin() {
        this.stopTimer();

        // Aggiorna le statistiche finali
        this.finalMovesElement.textContent = this.moves;
        this.finalTimeElement.textContent = this.timerElement.textContent;
        this.finalDifficultyElement.textContent =
            this.difficulty === 'easy' ? 'Facile (4x4)' : 'Difficile (6x6)';

        // Mostra il modale dopo un breve ritardo
        setTimeout(() => {
            this.winModal.classList.remove('hidden');
        }, 500);
    }

    /**
     * Riavvia il gioco
     */
    restartGame() {
        this.winModal.classList.add('hidden');
        this.startGame();
    }
}

/**
 * ========================================
 * INIZIALIZZAZIONE
 * ========================================
 * Avvia il gioco quando il DOM è caricato
 */
document.addEventListener('DOMContentLoaded', () => {
    const game = new MemoryGame('gameBoard');
});
