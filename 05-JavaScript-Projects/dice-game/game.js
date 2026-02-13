// Classe principale del gioco dei dadi
class DiceGame {
    constructor() {
        // Stato iniziale del gioco
        this.state = {
            scores: [0, 0],
            currentScore: 0,
            activePlayer: 0,
            gamePlaying: true,
            winningScore: 100
        };

        // Selezione elementi DOM
        this.elements = {
            dice: document.getElementById('dice'),
            diceResult: document.getElementById('dice-result'),
            btnNew: document.getElementById('btn-new'),
            btnRoll: document.getElementById('btn-roll'),
            btnHold: document.getElementById('btn-hold'),
            btnPlayAgain: document.getElementById('btn-play-again'),
            score0: document.getElementById('score-0'),
            score1: document.getElementById('score-1'),
            current0: document.getElementById('current-0'),
            current1: document.getElementById('current-1'),
            player0: document.getElementById('player-0'),
            player1: document.getElementById('player-1'),
            indicator0: document.getElementById('indicator-0'),
            indicator1: document.getElementById('indicator-1'),
            overlay: document.getElementById('overlay'),
            winnerText: document.getElementById('winner-text'),
            finalScore: document.getElementById('final-score'),
            gameMessage: document.getElementById('game-message'),
            winningScore: document.getElementById('winning-score')
        };

        // Inizializzazione
        this.init();
    }

    // Inizializza il gioco
    init() {
        this.addEventListeners();
        this.updateMessage('Premi "Lancia il Dado" per iniziare!');
    }

    // Aggiunge gli event listeners
    addEventListeners() {
        this.elements.btnNew.addEventListener('click', () => this.initGame());
        this.elements.btnRoll.addEventListener('click', () => this.rollDice());
        this.elements.btnHold.addEventListener('click', () => this.holdScore());
        this.elements.btnPlayAgain.addEventListener('click', () => {
            this.elements.overlay.classList.remove('active');
            this.initGame();
        });
        this.elements.winningScore.addEventListener('change', (e) => {
            this.state.winningScore = parseInt(e.target.value);
            this.updateMessage(`Punti per vincere impostati a ${this.state.winningScore}`);
        });
    }

    // Inizializza una nuova partita
    initGame() {
        this.state = {
            scores: [0, 0],
            currentScore: 0,
            activePlayer: 0,
            gamePlaying: true,
            winningScore: parseInt(this.elements.winningScore.value)
        };

        // Reset UI
        this.updateScoreDisplay();
        this.updateCurrentScoreDisplay();
        this.updateActivePlayerUI();
        this.resetDice();
        this.updateButtons(true);
        this.updateMessage('Premi "Lancia il Dado" per iniziare!');
    }

    // Lancia il dado
    rollDice() {
        if (!this.state.gamePlaying) return;

        // Disabilita i pulsanti durante l'animazione
        this.updateButtons(false);

        // Genera numero casuale per il dado
        const diceValue = Math.floor(Math.random() * 6) + 1;

        // Mostra animazione del dado
        this.animateDice(diceValue);
    }

    // Anima il dado e gestisce il risultato
    animateDice(diceValue) {
        const dice = this.elements.dice;
        dice.classList.add('rolling');

        // Mostra animazione di rotazione
        setTimeout(() => {
            dice.classList.remove('rolling');
            this.showDiceFace(diceValue);
            this.elements.diceResult.textContent = diceValue;

            // Gestisci il risultato
            this.handleDiceRoll(diceValue);
        }, 600);
    }

    // Mostra la faccia del dado
    showDiceFace(faceNumber) {
        // Nascondi tutte le facce
        const faces = this.elements.dice.querySelectorAll('.dice-face');
        faces.forEach(face => face.classList.remove('active'));

        // Mostra la faccia corretta
        const targetFace = this.elements.dice.querySelector(
            `.dice-face[data-face="${faceNumber}"]`
        );
        if (targetFace) {
            targetFace.classList.add('active');
        }
    }

    // Gestisce il risultato del lancio del dado
    handleDiceRoll(diceValue) {
        if (diceValue === 1) {
            // Se esce 1, perde il punteggio corrente e il turno passa
            this.state.currentScore = 0;
            this.updateCurrentScoreDisplay();

            // Aggiungi effetto visivo
            this.elements[`player${this.state.activePlayer}`].classList.add('lost-turn');
            setTimeout(() => {
                this.elements[`player${this.state.activePlayer}`].classList.remove('lost-turn');
            }, 500);

            this.updateMessage(
                `È uscito 1! ${this.getPlayerName(this.state.activePlayer)} perde il punteggio corrente.`
            );

            setTimeout(() => this.nextPlayer(), 1000);
        } else {
            // Aggiungi il valore al punteggio corrente
            this.state.currentScore += diceValue;
            this.updateCurrentScoreDisplay();
            this.updateMessage(
                `${this.getPlayerName(this.state.activePlayer)} ha fatto ${diceValue}! Punteggio corrente: ${this.state.currentScore}`
            );
        }

        // Riabilita i pulsanti
        this.updateButtons(true);
    }

    // Tieni il punteggio
    holdScore() {
        if (!this.state.gamePlaying || this.state.currentScore === 0) {
            if (this.state.currentScore === 0) {
                this.updateMessage('Lancia prima il dado per accumulare punti!');
            }
            return;
        }

        // Aggiungi il punteggio corrente al totale
        this.state.scores[this.state.activePlayer] += this.state.currentScore;
        this.state.currentScore = 0;

        // Aggiorna UI con animazione
        this.updateScoreDisplay();
        this.updateCurrentScoreDisplay();

        // Aggiungi effetto visivo al punteggio aggiornato
        const scoreElement = this.elements[`score${this.state.activePlayer}`];
        scoreElement.classList.add('updated');
        setTimeout(() => scoreElement.classList.remove('updated'), 500);

        // Controlla se il giocatore ha vinto
        if (this.checkWin()) {
            this.declareWinner();
        } else {
            this.updateMessage(
                `${this.getPlayerName(this.state.activePlayer)} tiene ${this.state.scores[this.state.activePlayer]} punti!`
            );
            setTimeout(() => this.nextPlayer(), 1000);
        }
    }

    // Passa al prossimo giocatore
    nextPlayer() {
        this.state.currentScore = 0;
        this.state.activePlayer = this.state.activePlayer === 0 ? 1 : 0;

        this.updateCurrentScoreDisplay();
        this.updateActivePlayerUI();
        this.resetDice();
        this.updateMessage(
            `Turno di ${this.getPlayerName(this.state.activePlayer)}! Lancia il dado.`
        );
    }

    // Controlla se il giocatore corrente ha vinto
    checkWin() {
        return this.state.scores[this.state.activePlayer] >= this.state.winningScore;
    }

    // Dichiara il vincitore
    declareWinner() {
        this.state.gamePlaying = false;
        this.updateButtons(false);

        const winnerName = this.getPlayerName(this.state.activePlayer);
        const finalScore = this.state.scores[this.state.activePlayer];

        this.elements.winnerText.textContent = `${winnerName} vince!`;
        this.elements.finalScore.textContent = finalScore;
        this.elements.overlay.classList.add('active');

        this.updateMessage(`🎉 ${winnerName} ha vinto con ${finalScore} punti!`);
    }

    // Aggiorna il display dei punteggi totali
    updateScoreDisplay() {
        this.elements.score0.textContent = this.state.scores[0];
        this.elements.score1.textContent = this.state.scores[1];
    }

    // Aggiorna il display dei punteggi correnti
    updateCurrentScoreDisplay() {
        this.elements.current0.textContent = this.state.currentScore;
        this.elements.current1.textContent = this.state.currentScore;
    }

    // Aggiorna l'UI del giocatore attivo
    updateActivePlayerUI() {
        // Rimuovi classe active da tutti i pannelli
        this.elements.player0.classList.remove('active');
        this.elements.player1.classList.remove('active');
        this.elements.indicator0.classList.remove('active');
        this.elements.indicator1.classList.remove('active');

        // Aggiungi classe active al giocatore corrente
        const activePanel = this.elements[`player${this.state.activePlayer}`];
        const activeIndicator = this.elements[`indicator${this.state.activePlayer}`];

        activePanel.classList.add('active');
        activeIndicator.classList.add('active');
    }

    // Reset del dado
    resetDice() {
        this.elements.diceResult.textContent = '-';
        const faces = this.elements.dice.querySelectorAll('.dice-face');
        faces.forEach(face => face.classList.remove('active'));

        // Mostra la prima faccia come default
        const defaultFace = this.elements.dice.querySelector('.dice-face[data-face="1"]');
        if (defaultFace) {
            defaultFace.classList.add('active');
        }
    }

    // Aggiorna lo stato dei pulsanti
    updateButtons(enabled) {
        this.elements.btnRoll.disabled = !enabled;
        this.elements.btnHold.disabled = !enabled;
        this.elements.btnNew.disabled = !enabled;
    }

    // Aggiorna il messaggio di gioco
    updateMessage(message) {
        this.elements.gameMessage.textContent = message;
    }

    // Ottieni il nome del giocatore
    getPlayerName(playerIndex) {
        return `Giocatore ${playerIndex + 1}`;
    }
}

// Utility functions per operazioni comuni
const GameUtils = {
    // Genera numero casuale tra min e max (inclusivo)
    randomBetween: (min, max) => {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },

    // Formatta il punteggio
    formatScore: (score) => {
        return score.toLocaleString('it-IT');
    },

    // Calcola la media dei punteggi
    calculateAverage: (scores) => {
        if (scores.length === 0) return 0;
        const sum = scores.reduce((acc, score) => acc + score, 0);
        return Math.round(sum / scores.length);
    },

    // Trova il punteggio più alto
    findHighScore: (scores) => {
        return Math.max(...scores);
    },

    // Valuta se vale la pena tenere il punteggio
    shouldHold: (currentScore, totalScore, winningScore, risk = 0.16) => {
        // risk è la probabilità di perdere tutto (1/6 = 0.16)
        const potentialGain = currentScore;
        const potentialLoss = currentScore;
        const distanceToWin = winningScore - totalScore;

        // Se sei vicino alla vittoria, tieni il punteggio
        if (distanceToWin <= 20) return true;

        // Se hai accumulato molti punti, valuta di tenere
        if (currentScore >= 15) return true;

        // Altrimenti, continua a giocare
        return false;
    }
};

// Storage per statistiche di gioco (LocalStorage)
class GameStats {
    constructor() {
        this.storageKey = 'diceGameStats';
        this.stats = this.loadStats();
    }

    // Carica le statistiche dal localStorage
    loadStats() {
        const saved = localStorage.getItem(this.storageKey);
        return saved ? JSON.parse(saved) : this.getDefaultStats();
    }

    // Statistiche di default
    getDefaultStats() {
        return {
            gamesPlayed: 0,
            player1Wins: 0,
            player2Wins: 0,
            highestScore: 0,
            lastPlayed: null
        };
    }

    // Salva le statistiche
    saveStats() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.stats));
    }

    // Registra una partita giocata
    recordGame(winner, finalScore) {
        this.stats.gamesPlayed++;
        this.stats.lastPlayed = new Date().toISOString();

        if (winner === 0) {
            this.stats.player1Wins++;
        } else {
            this.stats.player2Wins++;
        }

        if (finalScore > this.stats.highestScore) {
            this.stats.highestScore = finalScore;
        }

        this.saveStats();
    }

    // Ottieni le statistiche
    getStats() {
        return { ...this.stats };
    }

    // Reset delle statistiche
    resetStats() {
        this.stats = this.getDefaultStats();
        this.saveStats();
    }

    // Calcola le percentuali di vittoria
    getWinPercentages() {
        if (this.stats.gamesPlayed === 0) {
            return { player1: 0, player2: 0 };
        }

        return {
            player1: Math.round((this.stats.player1Wins / this.stats.gamesPlayed) * 100),
            player2: Math.round((this.stats.player2Wins / this.stats.gamesPlayed) * 100)
        };
    }
}

// Inizializza il gioco quando il DOM è pronto
document.addEventListener('DOMContentLoaded', () => {
    // Crea istanza del gioco
    const game = new DiceGame();

    // Crea istanza per le statistiche
    const stats = new GameStats();

    // Log di inizializzazione
    console.log('🎲 Gioco dei Dadi inizializzato!');
    console.log('Statistiche:', stats.getStats());

    // Esponi le istanze globalmente per debugging
    window.diceGame = game;
    window.gameStats = stats;

    // Aggiungi shortcut da tastiera
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
            e.preventDefault();
            if (game.state.gamePlaying) {
                game.rollDice();
            }
        } else if (e.code === 'Enter') {
            e.preventDefault();
            if (game.state.gamePlaying) {
                game.holdScore();
            }
        } else if (e.code === 'KeyN' && e.ctrlKey) {
            e.preventDefault();
            game.initGame();
        }
    });

    // Mostra i controlli da tastiera in console
    console.log('🎮 Controlli da tastiera:');
    console.log('  - Spazio: Lancia il dado');
    console.log('  - Enter: Tieni il punteggio');
    console.log('  - Ctrl + N: Nuova partita');
});

// Export per moduli ES6 (se usato in un ambiente module)
export { DiceGame, GameUtils, GameStats };
