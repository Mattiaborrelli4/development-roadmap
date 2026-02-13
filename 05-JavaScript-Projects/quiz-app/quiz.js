// ===== Quiz Application - Main Logic =====

class QuizApp {
    constructor() {
        // Stato del gioco
        this.state = {
            currentScreen: 'start',
            selectedCategory: null,
            selectedDifficulty: null,
            questions: [],
            currentQuestionIndex: 0,
            score: 0,
            correctAnswers: 0,
            incorrectAnswers: 0,
            answers: [],
            timer: null,
            timeRemaining: 15,
            totalTime: 0,
            isAnswered: false,
            highScores: []
        };

        // Configurazione
        this.config = {
            questionsPerQuiz: 10,
            timePerQuestion: 15,
            pointsPerCorrectAnswer: 10,
            pointsPerTimeBonus: 1
        };

        // Elementi DOM
        this.elements = {};

        // Inizializzazione
        this.init();
    }

    // Inizializza l'applicazione
    init() {
        this.cacheElements();
        this.loadHighScores();
        this.bindEvents();
        this.renderCategories();
        this.renderHighScoresPreview();
    }

    // Cache degli elementi DOM
    cacheElements() {
        // Schermi
        this.elements.screens = {
            start: document.getElementById('start-screen'),
            quiz: document.getElementById('quiz-screen'),
            results: document.getElementById('results-screen'),
            highScores: document.getElementById('high-scores-screen')
        };

        // Start Screen
        this.elements.categoriesGrid = document.getElementById('categories-grid');
        this.elements.difficultyButtons = document.querySelectorAll('.difficulty-btn');
        this.elements.startQuizBtn = document.getElementById('start-quiz-btn');
        this.elements.highScoresList = document.getElementById('high-scores-list');

        // Quiz Screen
        this.elements.progressFill = document.getElementById('progress-fill');
        this.elements.questionCounter = document.getElementById('question-counter');
        this.elements.categoryDisplay = document.getElementById('category-display');
        this.elements.currentScore = document.getElementById('current-score');
        this.elements.timerFill = document.getElementById('timer-fill');
        this.elements.timerDisplay = document.getElementById('timer-display');
        this.elements.questionText = document.getElementById('question-text');
        this.elements.answersContainer = document.getElementById('answers-container');
        this.elements.nextQuestionBtn = document.getElementById('next-question-btn');

        // Results Screen
        this.elements.finalScore = document.getElementById('final-score');
        this.elements.correctCount = document.getElementById('correct-count');
        this.elements.incorrectCount = document.getElementById('incorrect-count');
        this.elements.percentage = document.getElementById('percentage');
        this.elements.totalTime = document.getElementById('total-time');
        this.elements.performanceMessage = document.getElementById('performance-message');
        this.elements.answersReviewList = document.getElementById('answers-review-list');
        this.elements.highScoreForm = document.getElementById('high-score-form');
        this.elements.playerName = document.getElementById('player-name');
        this.elements.saveScoreBtn = document.getElementById('save-score-btn');
        this.elements.playAgainBtn = document.getElementById('play-again-btn');
        this.elements.homeBtn = document.getElementById('home-btn');

        // High Scores Screen
        this.elements.highScoresTable = document.getElementById('high-scores-table');
        this.elements.filterButtons = document.querySelectorAll('.filter-btn');
        this.elements.closeHighScoresBtn = document.getElementById('close-high-scores-btn');
        this.elements.clearScoresBtn = document.getElementById('clear-scores-btn');
    }

    // Binding degli event listeners
    bindEvents() {
        // Start Screen
        this.elements.startQuizBtn.addEventListener('click', () => this.startQuiz());

        // Quiz Screen
        this.elements.nextQuestionBtn.addEventListener('click', () => this.nextQuestion());

        // Results Screen
        this.elements.saveScoreBtn.addEventListener('click', () => this.saveHighScore());
        this.elements.playAgainBtn.addEventListener('click', () => this.restartQuiz());
        this.elements.homeBtn.addEventListener('click', () => this.goToHome());

        // High Scores Screen
        this.elements.filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.filterHighScores(e));
        });
        this.elements.closeHighScoresBtn.addEventListener('click', () => this.goToHome());
        this.elements.clearScoresBtn.addEventListener('click', () => this.clearHighScores());
    }

    // Renderizza le categorie
    renderCategories() {
        this.elements.categoriesGrid.innerHTML = categories.map(category => `
            <div class="category-card" data-category="${category.id}">
                <i class="${category.icon}" style="color: ${category.color}"></i>
                <h3>${category.name}</h3>
                <p>${category.description}</p>
            </div>
        `).join('');

        // Aggiungi event listeners
        this.elements.categoriesGrid.querySelectorAll('.category-card').forEach(card => {
            card.addEventListener('click', () => this.selectCategory(card.dataset.category));
        });
    }

    // Seleziona una categoria
    selectCategory(categoryId) {
        this.state.selectedCategory = categoryId;

        // Aggiorna UI
        this.elements.categoriesGrid.querySelectorAll('.category-card').forEach(card => {
            card.classList.toggle('selected', card.dataset.category === categoryId);
        });

        this.updateStartButton();
    }

    // Seleziona la difficoltà
    selectDifficulty(difficulty) {
        this.state.selectedDifficulty = difficulty;

        // Aggiorna UI
        this.elements.difficultyButtons.forEach(btn => {
            btn.classList.toggle('selected', btn.dataset.difficulty === difficulty);
        });

        this.updateStartButton();
    }

    // Aggiorna lo stato del pulsante start
    updateStartButton() {
        const canStart = this.state.selectedCategory && this.state.selectedDifficulty;
        this.elements.startQuizBtn.disabled = !canStart;
    }

    // Avvia il quiz
    startQuiz() {
        // Recupera le domande
        const questions = getQuestions(
            this.state.selectedCategory,
            this.state.selectedDifficulty,
            this.config.questionsPerQuiz
        );

        // Mischia le risposte per ogni domanda
        this.state.questions = questions.map(q => shuffleAnswers(q));

        // Reset dello stato
        this.state.currentQuestionIndex = 0;
        this.state.score = 0;
        this.state.correctAnswers = 0;
        this.state.incorrectAnswers = 0;
        this.state.answers = [];
        this.state.totalTime = 0;

        // Cambia schermata
        this.showScreen('quiz');
        this.displayQuestion();
    }

    // Mostra una schermata
    showScreen(screenName) {
        Object.values(this.elements.screens).forEach(screen => {
            screen.classList.remove('active');
        });
        this.elements.screens[screenName].classList.add('active');
        this.state.currentScreen = screenName;
    }

    // Visualizza la domanda corrente
    displayQuestion() {
        const question = this.state.questions[this.state.currentQuestionIndex];

        // Reset stato
        this.state.isAnswered = false;
        this.state.timeRemaining = this.config.timePerQuestion;

        // Aggiorna progress
        const progress = ((this.state.currentQuestionIndex + 1) / this.state.questions.length) * 100;
        this.elements.progressFill.style.width = `${progress}%`;
        this.elements.questionCounter.textContent = `Domanda ${this.state.currentQuestionIndex + 1}/${this.state.questions.length}`;

        // Aggiorna categoria e punteggio
        const category = categories.find(c => c.id === this.state.selectedCategory);
        this.elements.categoryDisplay.textContent = category?.name || '';
        this.elements.currentScore.textContent = this.state.score;

        // Visualizza la domanda
        this.elements.questionText.textContent = question.question;

        // Visualizza le risposte
        this.elements.answersContainer.innerHTML = question.shuffledAnswers.map((answer, index) => `
            <button class="answer-btn" data-index="${index}">
                <span class="answer-letter">${String.fromCharCode(65 + index)}</span>
                ${answer.text}
                <span class="feedback-icon">
                    <i class="fas ${answer.isCorrect ? 'fa-check' : 'fa-times'}"></i>
                </span>
            </button>
        `).join('');

        // Aggiungi event listeners
        this.elements.answersContainer.querySelectorAll('.answer-btn').forEach(btn => {
            btn.addEventListener('click', () => this.selectAnswer(parseInt(btn.dataset.index)));
        });

        // Nascondi pulsante next
        this.elements.nextQuestionBtn.style.display = 'none';

        // Avvia il timer
        this.startTimer();
    }

    // Avvia il timer
    startTimer() {
        clearInterval(this.state.timer);
        this.updateTimerDisplay();

        this.state.timer = setInterval(() => {
            this.state.timeRemaining--;
            this.state.totalTime++;
            this.updateTimerDisplay();

            if (this.state.timeRemaining <= 0) {
                this.timeUp();
            }
        }, 1000);
    }

    // Aggiorna il display del timer
    updateTimerDisplay() {
        const percentage = (this.state.timeRemaining / this.config.timePerQuestion) * 100;
        this.elements.timerFill.style.width = `${percentage}%`;
        this.elements.timerDisplay.textContent = this.state.timeRemaining;

        // Aggiorna classi per warning
        this.elements.timerDisplay.classList.remove('warning', 'danger');
        if (this.state.timeRemaining <= 5) {
            this.elements.timerDisplay.classList.add('danger');
        } else if (this.state.timeRemaining <= 10) {
            this.elements.timerDisplay.classList.add('warning');
        }
    }

    // Tempo scaduto
    timeUp() {
        clearInterval(this.state.timer);
        this.state.isAnswered = true;

        // Segna come risposta errata
        const question = this.state.questions[this.state.currentQuestionIndex];
        this.state.incorrectAnswers++;

        // Salva la risposta
        this.state.answers.push({
            question: question.question,
            userAnswer: null,
            correctAnswer: question.shuffledAnswers[question.correctIndex].text,
            isCorrect: false,
            timeRemaining: 0
        });

        // Mostra la risposta corretta
        this.showCorrectAnswer();
        this.disableAnswers();
        this.showNextButton();
    }

    // Seleziona una risposta
    selectAnswer(answerIndex) {
        if (this.state.isAnswered) return;

        clearInterval(this.state.timer);
        this.state.isAnswered = true;

        const question = this.state.questions[this.state.currentQuestionIndex];
        const isCorrect = answerIndex === question.correctIndex;
        const selectedBtn = this.elements.answersContainer.querySelectorAll('.answer-btn')[answerIndex];

        // Aggiorna statistiche
        if (isCorrect) {
            this.state.correctAnswers++;
            // Calcola punteggio base + bonus tempo
            const timeBonus = this.state.timeRemaining * this.config.pointsPerTimeBonus;
            const points = this.config.pointsPerCorrectAnswer + timeBonus;
            this.state.score += points;
            this.elements.currentScore.textContent = this.state.score;
        } else {
            this.state.incorrectAnswers++;
        }

        // Salva la risposta
        this.state.answers.push({
            question: question.question,
            userAnswer: question.shuffledAnswers[answerIndex].text,
            correctAnswer: question.shuffledAnswers[question.correctIndex].text,
            isCorrect,
            timeRemaining: this.state.timeRemaining
        });

        // Aggiorna UI
        if (isCorrect) {
            selectedBtn.classList.add('correct');
        } else {
            selectedBtn.classList.add('incorrect', 'shake');
            // Mostra la risposta corretta
            this.showCorrectAnswer();
        }

        selectedBtn.classList.add('show-feedback');
        this.disableAnswers();
        this.showNextButton();
    }

    // Mostra la risposta corretta
    showCorrectAnswer() {
        const question = this.state.questions[this.state.currentQuestionIndex];
        const correctBtn = this.elements.answersContainer.querySelectorAll('.answer-btn')[question.correctIndex];
        correctBtn.classList.add('correct', 'show-feedback');
    }

    // Disabilita tutti i pulsanti risposta
    disableAnswers() {
        this.elements.answersContainer.querySelectorAll('.answer-btn').forEach(btn => {
            btn.disabled = true;
        });
    }

    // Mostra il pulsante next
    showNextButton() {
        this.elements.nextQuestionBtn.style.display = 'inline-flex';
        this.elements.nextQuestionBtn.focus();
    }

    // Prossima domanda
    nextQuestion() {
        this.state.currentQuestionIndex++;

        if (this.state.currentQuestionIndex >= this.state.questions.length) {
            this.endQuiz();
        } else {
            this.displayQuestion();
        }
    }

    // Termina il quiz
    endQuiz() {
        clearInterval(this.state.timer);
        this.showScreen('results');
        this.displayResults();
    }

    // Visualizza i risultati
    displayResults() {
        const totalQuestions = this.state.questions.length;
        const percentage = Math.round((this.state.correctAnswers / totalQuestions) * 100);

        // Punteggio finale
        this.elements.finalScore.textContent = this.state.score;

        // Dettagli
        this.elements.correctCount.textContent = this.state.correctAnswers;
        this.elements.incorrectCount.textContent = this.state.incorrectAnswers;
        this.elements.percentage.textContent = `${percentage}%`;
        this.elements.totalTime.textContent = `${this.state.totalTime}s`;

        // Messaggio di performance
        let message = '';
        if (percentage >= 90) {
            message = '🏆 Eccellente! Sei un vero esperto!';
        } else if (percentage >= 70) {
            message = '👏 Ottimo lavoro! Continua così!';
        } else if (percentage >= 50) {
            message = '👍 Buon risultato! Puoi migliorare ancora!';
        } else {
            message = '📚 Non arrenderti! Continua a studiare!';
        }
        this.elements.performanceMessage.textContent = message;

        // Rivedi le risposte
        this.renderAnswersReview();

        // Controlla se è un nuovo high score
        this.checkHighScore();
    }

    // Renderizza la revisione delle risposte
    renderAnswersReview() {
        this.elements.answersReviewList.innerHTML = this.state.answers.map((answer, index) => `
            <div class="review-item ${answer.isCorrect ? 'correct' : 'incorrect'}">
                <div class="review-question">${index + 1}. ${answer.question}</div>
                ${answer.userAnswer ? `
                    <div class="review-answer user">
                        <i class="fas ${answer.isCorrect ? 'fa-check-circle' : 'fa-times-circle'}"></i>
                        La tua risposta: ${answer.userAnswer}
                    </div>
                ` : `
                    <div class="review-answer user">
                        <i class="fas fa-clock"></i>
                        Tempo scaduto
                    </div>
                `}
                ${!answer.isCorrect ? `
                    <div class="review-answer correct">
                        <i class="fas fa-check-circle"></i>
                        Risposta corretta: ${answer.correctAnswer}
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    // Controlla se è un nuovo high score
    checkHighScore() {
        const categoryHighScores = this.state.highScores.filter(
            score => score.category === this.state.selectedCategory
        );

        const isHighScore = categoryHighScores.length < 10 ||
            this.state.score > Math.min(...categoryHighScores.map(s => s.score));

        this.elements.highScoreForm.style.display = isHighScore ? 'block' : 'none';
    }

    // Salva il high score
    saveHighScore() {
        const playerName = this.elements.playerName.value.trim() || 'Anonimo';

        const highScore = {
            name: playerName,
            score: this.state.score,
            category: this.state.selectedCategory,
            difficulty: this.state.selectedDifficulty,
            correct: this.state.correctAnswers,
            total: this.state.questions.length,
            date: new Date().toISOString()
        };

        this.state.highScores.push(highScore);
        this.saveHighScoresToStorage();
        this.elements.highScoreForm.style.display = 'none';

        // Mostra conferma
        alert('🎉 Punteggio salvato con successo!');
    }

    // Carica i high scores dal localStorage
    loadHighScores() {
        const saved = localStorage.getItem('quizHighScores');
        this.state.highScores = saved ? JSON.parse(saved) : [];
    }

    // Salva i high scores nel localStorage
    saveHighScoresToStorage() {
        localStorage.setItem('quizHighScores', JSON.stringify(this.state.highScores));
    }

    // Renderizza l'anteprima dei high scores
    renderHighScoresPreview() {
        const topScores = this.state.highScores
            .sort((a, b) => b.score - a.score)
            .slice(0, 5);

        this.elements.highScoresList.innerHTML = topScores.length > 0 ? topScores.map((score, index) => {
            const rankClass = index === 0 ? 'gold' : index === 1 ? 'silver' : index === 2 ? 'bronze' : '';
            const category = categories.find(c => c.id === score.category);
            return `
                <div class="high-score-item">
                    <span class="high-score-rank ${rankClass}">${index + 1}</span>
                    <div class="high-score-info">
                        <div class="high-score-name">${score.name}</div>
                        <div class="high-score-details">${category?.name || 'Generale'} - ${score.difficulty}</div>
                    </div>
                    <span class="high-score-points">${score.score} pts</span>
                </div>
            `;
        }).join('') : '<p style="text-align: center; color: var(--text-secondary);">Nessun punteggio registrato</p>';
    }

    // Filtra i high scores
    filterHighScores(event) {
        const filter = event.target.dataset.filter;

        // Aggiorna UI
        this.elements.filterButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });

        // Filtra scores
        const filteredScores = filter === 'all'
            ? this.state.highScores
            : this.state.highScores.filter(score => score.category === filter);

        this.renderHighScoresTable(filteredScores);
    }

    // Renderizza la tabella dei high scores
    renderHighScoresTable(scores) {
        const sortedScores = [...scores].sort((a, b) => b.score - a.score);

        this.elements.highScoresTable.innerHTML = sortedScores.length > 0 ? sortedScores.map((score, index) => {
            const rankClass = index === 0 ? 'gold' : index === 1 ? 'silver' : index === 2 ? 'bronze' : '';
            const category = categories.find(c => c.id === score.category);
            const date = new Date(score.date).toLocaleDateString('it-IT');
            return `
                <div class="high-score-item">
                    <span class="high-score-rank ${rankClass}">${index + 1}</span>
                    <div class="high-score-info">
                        <div class="high-score-name">${score.name}</div>
                        <div class="high-score-details">
                            ${category?.name || 'Generale'} - ${score.difficulty} | ${score.correct}/${score.total} corrette | ${date}
                        </div>
                    </div>
                    <span class="high-score-points">${score.score} pts</span>
                </div>
            `;
        }).join('') : '<p style="text-align: center; color: var(--text-secondary);">Nessun punteggio trovato</p>';
    }

    // Cancella tutti i high scores
    clearHighScores() {
        if (confirm('Sei sicuro di voler cancellare tutti i punteggi? Questa azione non può essere annullata.')) {
            this.state.highScores = [];
            this.saveHighScoresToStorage();
            this.renderHighScoresTable([]);
            this.renderHighScoresPreview();
            alert('Tutti i punteggi sono stati cancellati.');
        }
    }

    // Riavvia il quiz
    restartQuiz() {
        this.showScreen('start');
        this.state.selectedCategory = null;
        this.state.selectedDifficulty = null;
        this.elements.categoriesGrid.querySelectorAll('.category-card').forEach(card => {
            card.classList.remove('selected');
        });
        this.elements.difficultyButtons.forEach(btn => {
            btn.classList.remove('selected');
        });
        this.elements.playerName.value = '';
        this.updateStartButton();
    }

    // Torna alla home
    goToHome() {
        this.showScreen('start');
        this.renderHighScoresPreview();
    }
}

// Event listener per i pulsanti di difficoltà
document.addEventListener('DOMContentLoaded', () => {
    // Inizializza l'app
    const app = new QuizApp();

    // Aggiungi event listeners per i pulsanti difficoltà
    document.querySelectorAll('.difficulty-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            app.selectDifficulty(btn.dataset.difficulty);
        });
    });

    // Apri high scores screen (click sul titolo)
    document.querySelector('.high-scores-preview h3').style.cursor = 'pointer';
    document.querySelector('.high-scores-preview h3').addEventListener('click', () => {
        app.showScreen('highScores');
        app.filterHighScores({ target: { dataset: { filter: 'all' } } });
    });

    // Mostra l'app
    console.log('🎯 Quiz App caricata con successo!');
});
