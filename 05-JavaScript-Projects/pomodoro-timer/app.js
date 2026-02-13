// ===================================
// CONFIGURAZIONE
// ===================================
const CONFIG = {
    workDuration: 25 * 60,      // 25 minuti in secondi
    breakDuration: 5 * 60,      // 5 minuti in secondi
    notificationSound: 1000,    // Durata suono notifica in ms
    storageKey: 'pomodoroTimer' // Chiave LocalStorage
};

// ===================================
// STATO DELL'APPLICAZIONE
// ===================================
const state = {
    timeLeft: CONFIG.workDuration,
    isRunning: false,
    isWorkSession: true,
    completedPomodoros: 0,
    currentSession: 1,
    timerInterval: null,
    totalTime: CONFIG.workDuration
};

// ===================================
// ELEMENTI DOM
// ===================================
const elements = {
    timeDisplay: document.getElementById('timeDisplay'),
    sessionLabel: document.getElementById('sessionLabel'),
    startBtn: document.getElementById('startBtn'),
    pauseBtn: document.getElementById('pauseBtn'),
    resetBtn: document.getElementById('resetBtn'),
    workBtn: document.getElementById('workBtn'),
    breakBtn: document.getElementById('breakBtn'),
    themeToggle: document.getElementById('themeToggle'),
    completedPomodoros: document.getElementById('completedPomodoros'),
    currentSession: document.getElementById('currentSession'),
    progressFill: document.getElementById('progressFill'),
    timerDisplay: document.querySelector('.timer-display'),
    themeIcon: document.querySelector('.theme-icon')
};

// ===================================
// GESTIONE AUDIO
// ===================================
class AudioManager {
    constructor() {
        this.audioContext = null;
    }

    init() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    playNotification() {
        this.init();

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        // Configura il tono
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';

        // Configura il volume
        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(
            0.01,
            this.audioContext.currentTime + CONFIG.notificationSound / 1000
        );

        // Riproduci il suono
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + CONFIG.notificationSound / 1000);

        // Secondo tono per effetto campana
        setTimeout(() => {
            const osc2 = this.audioContext.createOscillator();
            const gain2 = this.audioContext.createGain();
            osc2.connect(gain2);
            gain2.connect(this.audioContext.destination);
            osc2.frequency.value = 600;
            osc2.type = 'sine';
            gain2.gain.setValueAtTime(0.3, this.audioContext.currentTime);
            gain2.gain.exponentialRampToValueAtTime(
                0.01,
                this.audioContext.currentTime + 0.5
            );
            osc2.start(this.audioContext.currentTime);
            osc2.stop(this.audioContext.currentTime + 0.5);
        }, 200);
    }
}

const audioManager = new AudioManager();

// ===================================
// GESTIONE LOCALSTORAGE
// ===================================
const storage = {
    save() {
        const data = {
            completedPomodoros: state.completedPomodoros,
            currentSession: state.currentSession,
            theme: document.documentElement.getAttribute('data-theme')
        };
        localStorage.setItem(CONFIG.storageKey, JSON.stringify(data));
    },

    load() {
        const saved = localStorage.getItem(CONFIG.storageKey);
        if (saved) {
            const data = JSON.parse(saved);
            state.completedPomodoros = data.completedPomodoros || 0;
            state.currentSession = data.currentSession || 1;
            if (data.theme) {
                document.documentElement.setAttribute('data-theme', data.theme);
                updateThemeIcon(data.theme);
            }
            updateStats();
        }
    }
};

// ===================================
// FUNZIONI DI UTILITY
// ===================================
const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

const updateDisplay = () => {
    elements.timeDisplay.textContent = formatTime(state.timeLeft);
    elements.sessionLabel.textContent = state.isWorkSession
        ? 'Tempo di Lavoro'
        : 'Tempo di Pausa';

    // Aggiorna la barra di progresso
    const progress = (state.timeLeft / state.totalTime) * 100;
    elements.progressFill.style.width = `${progress}%`;
};

const updateStats = () => {
    elements.completedPomodoros.textContent = state.completedPomodoros;
    elements.currentSession.textContent = state.currentSession;
};

const updateThemeIcon = (theme) => {
    elements.themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
};

// ===================================
// GESTIONE DEL TIMER
// ===================================
const startTimer = () => {
    if (state.isRunning) return;

    state.isRunning = true;
    elements.timerDisplay.classList.add('running');
    elements.timerDisplay.classList.remove('finished');
    updateButtons();

    state.timerInterval = setInterval(() => {
        state.timeLeft--;
        updateDisplay();

        if (state.timeLeft <= 0) {
            completeSession();
        }
    }, 1000);
};

const pauseTimer = () => {
    if (!state.isRunning) return;

    state.isRunning = false;
    elements.timerDisplay.classList.remove('running');
    clearInterval(state.timerInterval);
    updateButtons();
};

const resetTimer = () => {
    pauseTimer();
    state.timeLeft = state.isWorkSession ? CONFIG.workDuration : CONFIG.breakDuration;
    state.totalTime = state.timeLeft;
    elements.timerDisplay.classList.remove('finished');
    updateDisplay();
    updateButtons();
};

const switchSession = (isWork) => {
    state.isWorkSession = isWork;
    state.timeLeft = isWork ? CONFIG.workDuration : CONFIG.breakDuration;
    state.totalTime = state.timeLeft;

    // Aggiorna UI
    if (isWork) {
        elements.workBtn.classList.add('active');
        elements.breakBtn.classList.remove('active');
        elements.timerDisplay.classList.remove('break-mode');
    } else {
        elements.breakBtn.classList.add('active');
        elements.workBtn.classList.remove('active');
        elements.timerDisplay.classList.add('break-mode');
    }

    resetTimer();
};

const completeSession = () => {
    pauseTimer();
    elements.timerDisplay.classList.add('finished');
    audioManager.playNotification();

    if (state.isWorkSession) {
        // Completa sessione di lavoro
        state.completedPomodoros++;
        state.currentSession++;
        updateStats();
        storage.save();

        // Notifica e passa alla pausa
        if (Notification.permission === 'granted') {
            new Notification('Pomodoro Completato!', {
                body: 'Ottimo lavoro! È ora di fare una pausa.',
                icon: '🍅'
            });
        }

        setTimeout(() => {
            switchSession(false);
            startTimer();
        }, 2000);
    } else {
        // Completa sessione di pausa
        if (Notification.permission === 'granted') {
            new Notification('Pausa Terminata!', {
                body: 'Torna al lavoro! Nuovo Pomodoro.',
                icon: '💪'
            });
        }

        setTimeout(() => {
            switchSession(true);
            startTimer();
        }, 2000);
    }
};

// ===================================
// GESTIONE DEI PULSANTI
// ===================================
const updateButtons = () => {
    elements.startBtn.disabled = state.isRunning;
    elements.pauseBtn.disabled = !state.isRunning;
};

// ===================================
// GESTIONE DEL TEMA
// ===================================
const toggleTheme = () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    updateThemeIcon(newTheme);
    storage.save();
};

// ===================================
// RICHIESTA PERMESSO NOTIFICHE
// ===================================
const requestNotificationPermission = () => {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
};

// ===================================
// EVENT LISTENERS
// ===================================
const initEventListeners = () => {
    elements.startBtn.addEventListener('click', startTimer);
    elements.pauseBtn.addEventListener('click', pauseTimer);
    elements.resetBtn.addEventListener('click', resetTimer);
    elements.workBtn.addEventListener('click', () => switchSession(true));
    elements.breakBtn.addEventListener('click', () => switchSession(false));
    elements.themeToggle.addEventListener('click', toggleTheme);

    // Scorciatoie da tastiera
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && e.target.tagName !== 'BUTTON') {
            e.preventDefault();
            if (state.isRunning) {
                pauseTimer();
            } else {
                startTimer();
            }
        }
        if (e.code === 'KeyR' && e.target.tagName !== 'INPUT') {
            e.preventDefault();
            resetTimer();
        }
    });
};

// ===================================
// INIZIALIZZAZIONE
// ===================================
const init = () => {
    storage.load();
    updateDisplay();
    updateStats();
    updateButtons();
    initEventListeners();
    requestNotificationPermission();

    // Imposta lo stato iniziale
    if (state.isWorkSession) {
        elements.workBtn.classList.add('active');
    } else {
        elements.breakBtn.classList.add('active');
        elements.timerDisplay.classList.add('break-mode');
    }

    console.log('🍅 Pomodoro Timer inizializzato!');
    console.log('Premi Space per avviare/pausare, R per reset');
};

// Avvia l'applicazione
document.addEventListener('DOMContentLoaded', init);
