// ============================================
// POMODORO TIMER - JAVASCRIPT ES6+
// ============================================
// Questo script implementa un timer Pomodoro completo con
// le funzionalità moderne di JavaScript ES6+

// ============================================
// CLASSE PRINCIPALE: PomodoroTimer
// ============================================
// ES6: Le classi forniscono un modo più chiaro per creare oggetti
// e gestire la programmazione orientata agli oggetti
class PomodoroTimer {
    // ============================================
    // COSTRUTTORE - Inizializzazione dell'oggetto
    // ============================================
    // ES6: I valori di default dei parametri semplificano il codice
    constructor(workTime = 25, breakTime = 5) {
        // Tempi in minuti
        this.workTime = workTime;
        this.breakTime = breakTime;

        // Stato del timer
        this.timeLeft = workTime * 60;  // Convertito in secondi
        this.isRunning = false;
        this.currentMode = 'work';      // 'work' o 'break'
        this.timerInterval = null;      // Riferimento all'intervallo

        // Statistiche
        this.todaySessions = 0;
        this.sessionHistory = [];

        // ES6: Inizializzazione dei metodi
        this.init();
    }

    // ============================================
    // METODO INIT - Configurazione iniziale
    // ============================================
    init() {
        // Carica le statistiche dal localStorage
        this.loadStats();

        // Ottieni riferimenti agli elementi del DOM
        // ES6: La proprietà DOM elements semplifica l'accesso agli elementi
        this.dom = {
            timeDisplay: document.getElementById('time'),
            modeLabel: document.getElementById('mode-label'),
            startBtn: document.getElementById('start-btn'),
            pauseBtn: document.getElementById('pause-btn'),
            resetBtn: document.getElementById('reset-btn'),
            sessionCount: document.getElementById('session-count'),
            sessionDots: document.getElementById('session-dots'),
            totalSessions: document.getElementById('total-sessions'),
            totalTime: document.getElementById('total-time'),
            bestDay: document.getElementById('best-day'),
            logList: document.getElementById('log-list'),
            clearStatsBtn: document.getElementById('clear-stats-btn'),
            timerDisplay: document.querySelector('.timer-display'),
            modeButtons: document.querySelectorAll('.mode-btn')
        };

        // Aggiorna la UI con i dati caricati
        this.updateDisplay();
        this.updateStats();
        this.renderSessionDots();
        this.renderSessionLog();

        // Registra gli event listeners
        // ES6: Arrow functions per mantenere il contesto 'this'
        this.dom.startBtn.addEventListener('click', () => this.start());
        this.dom.pauseBtn.addEventListener('click', () => this.pause());
        this.dom.resetBtn.addEventListener('click', () => this.reset());
        this.dom.clearStatsBtn.addEventListener('click', () => this.clearStats());

        // Event listeners per i bottoni modalità
        this.dom.modeButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mode = e.target.dataset.mode;
                this.switchMode(mode);
            });
        });

        // Salva automaticamente prima di chiudere la pagina
        window.addEventListener('beforeunload', () => this.saveStats());
    }

    // ============================================
    // METODO START - Avvia il timer
    // ============================================
    start() {
        // ES6: Template literals per stringhe più leggibili
        console.log(`🚀 Timer avviato in modalità ${this.currentMode}`);

        this.isRunning = true;
        this.updateButtons();

        // ES6: setInterval con arrow function
        // L'arrow function mantiene automaticamente il contesto 'this'
        this.timerInterval = setInterval(() => {
            this.tick();
        }, 1000);  // Esegue ogni 1000ms (1 secondo)
    }

    // ============================================
    // METODO PAUSE - Metti in pausa il timer
    // ============================================
    pause() {
        console.log('⏸️ Timer in pausa');
        this.isRunning = false;

        // Ferma l'intervallo
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }

        this.updateButtons();
    }

    // ============================================
    // METODO RESET - Resetta il timer
    // ============================================
    reset() {
        console.log('🔄 Timer resettato');
        this.pause();

        // Resetta il tempo in base alla modalità corrente
        this.timeLeft = this.currentMode === 'work'
            ? this.workTime * 60
            : this.breakTime * 60;

        this.updateDisplay();
    }

    // ============================================
    // METODO TICK - Eseguito ogni secondo
    // ============================================
    tick() {
        // Decrementa il tempo
        this.timeLeft--;

        // Aggiorna il display
        this.updateDisplay();

        // Controlla se il timer è finito
        if (this.timeLeft <= 0) {
            this.completeSession();
        }
    }

    // ============================================
    // METODO COMPLETESESSION - Gestisce il completamento
    // ============================================
    completeSession() {
        // Ferma il timer
        this.pause();

        // Riproduci suono di notifica
        this.playNotificationSound();

        if (this.currentMode === 'work') {
            // Incrementa il contatore delle sessioni
            this.todaySessions++;

            // Aggiungi alla cronologia
            this.addSessionToHistory();

            // Aggiorna la UI
            this.renderSessionDots();
            this.renderSessionLog();
            this.updateStats();

            // Notifica all'utente
            this.showNotification('🎉 Pomodoro completato! Tempo di pausa.');

            // Passa automaticamente alla modalità pausa
            this.switchMode('break');
        } else {
            // Fine della pausa
            this.showNotification('⚡ Pausa terminata! Pronto per lavorare?');
            this.switchMode('work');
        }

        // Salva le statistiche
        this.saveStats();
    }

    // ============================================
    // METODO SWITCHMODE - Cambia modalità lavoro/pausa
    // ============================================
    // ES6: Parametro con valore di default
    switchMode(mode = 'work') {
        // Se il timer è in esecuzione, ferma prima
        if (this.isRunning) {
            this.pause();
        }

        this.currentMode = mode;

        // Imposta il tempo appropriato
        // ES6: Operatore ternario per assegnazione condizionale
        this.timeLeft = mode === 'work'
            ? this.workTime * 60
            : this.breakTime * 60;

        // Aggiorna UI
        this.updateDisplay();
        this.updateModeButtons();
        this.updateTimerDisplayTheme();
    }

    // ============================================
    // METODO UPDATEDISPLAY - Aggiorna il display del tempo
    // ============================================
    updateDisplay() {
        // Converti secondi in minuti e secondi
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;

        // ES6: Template literals con padding
        // .padStart(2, '0') aggiunge uno zero se il numero ha una sola cifra
        const timeString = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        // Aggiorna il DOM
        this.dom.timeDisplay.textContent = timeString;

        // Aggiorna l'etichetta della modalità
        const modeText = this.currentMode === 'work' ? 'Tempo di Lavoro' : 'Tempo di Pausa';
        this.dom.modeLabel.textContent = modeText;

        // Aggiorna il titolo della pagina
        document.title = `${timeString} - ${modeText}`;
    }

    // ============================================
    // METODO UPDATEBUTTONS - Aggiorna stato bottoni
    // ============================================
    updateButtons() {
        // Abilita/disabilita i bottoni in base allo stato
        this.dom.startBtn.disabled = this.isRunning;
        this.dom.pauseBtn.disabled = !this.isRunning;
    }

    // ============================================
    // METODO UPDATEMODEBUTTONS - Aggiorna bottoni modalità
    // ============================================
    updateModeButtons() {
        // Rimuovi la classe active da tutti i bottoni
        this.dom.modeButtons.forEach(btn => {
            btn.classList.remove('active');
        });

        // Aggiungi active al bottone corrispondente alla modalità
        // ES6: Array.from() + find() con arrow function
        const activeButton = Array.from(this.dom.modeButtons)
            .find(btn => btn.dataset.mode === this.currentMode);

        if (activeButton) {
            activeButton.classList.add('active');
        }
    }

    // ============================================
    // METODO UPDATETIMERDISPLAYTHEME - Aggiorna tema display
    // ============================================
    updateTimerDisplayTheme() {
        // Rimuovi o aggiungi la classe break-mode
        if (this.currentMode === 'break') {
            this.dom.timerDisplay.classList.add('break-mode');
        } else {
            this.dom.timerDisplay.classList.remove('break-mode');
        }
    }

    // ============================================
    // METODO RENDERSESSIONDOTS - Renderizza i puntini
    // ============================================
    renderSessionDots() {
        // Svuota il container
        this.dom.sessionDots.innerHTML = '';

        // Aggiungi un puntino per ogni sessione completata
        // ES6: for...of loop (più moderno di for tradizionale)
        for (let i = 0; i < this.todaySessions; i++) {
            const dot = document.createElement('div');
            dot.className = 'session-dot';
            this.dom.sessionDots.appendChild(dot);
        }

        // Aggiorna il contatore numerico
        this.dom.sessionCount.textContent = this.todaySessions;
    }

    // ============================================
    // METODO ADDSESSIONTOHISTORY - Aggiunge sessione alla cronologia
    // ============================================
    addSessionToHistory() {
        // Crea oggetto sessione
        // ES6: Shorthand property (equivalente a { timestamp: timestamp })
        const timestamp = new Date();
        const session = {
            timestamp,
            // ES6: Metodo toLocaleString per formattazione italiana
            formattedTime: timestamp.toLocaleString('it-IT', {
                hour: '2-digit',
                minute: '2-digit'
            }),
            formattedDate: timestamp.toLocaleDateString('it-IT'),
            mode: this.currentMode
        };

        // Aggiungi all'inizio dell'array
        this.sessionHistory.unshift(session);

        // Mantieni solo le ultime 20 sessioni
        // ES6: Array.slice() restituisce una copia dell'array
        if (this.sessionHistory.length > 20) {
            this.sessionHistory = this.sessionHistory.slice(0, 20);
        }
    }

    // ============================================
    // METODO RENDERSESSIONLOG - Renderizza il log
    // ============================================
    renderSessionLog() {
        // Filtra solo le sessioni di oggi
        // ES6: Array.filter() con arrow function
        const today = new Date().toLocaleDateString('it-IT');
        const todaySessions = this.sessionHistory.filter(
            session => session.formattedDate === today
        );

        // Svuota il container
        this.dom.logList.innerHTML = '';

        if (todaySessions.length === 0) {
            // Nessuna sessione oggi
            this.dom.logList.innerHTML =
                '<p class="empty-message">Nessuna sessione completata oggi</p>';
            return;
        }

        // Renderizza ogni sessione
        // ES6: forEach con arrow function
        todaySessions.forEach((session, index) => {
            const item = document.createElement('div');
            item.className = 'log-item';

            // ES6: Template literals per HTML
            item.innerHTML = `
                <span class="time">Pomodoro #${todaySessions.length - index}</span>
                <span class="timestamp">${session.formattedTime}</span>
            `;

            this.dom.logList.appendChild(item);
        });
    }

    // ============================================
    // METODO UPDATESTATS - Aggiorna le statistiche
    // ============================================
    updateStats() {
        // Calcola le statistiche
        const totalSessions = this.sessionHistory.length;
        const totalMinutes = totalSessions * this.workTime;

        // Trova il record giornaliero
        // ES6: Map per raggruppare per data
        const sessionsByDate = {};

        this.sessionHistory.forEach(session => {
            const date = session.formattedDate;
            sessionsByDate[date] = (sessionsByDate[date] || 0) + 1;
        });

        // ES6: Math.max con spread operator (...array)
        const bestDay = Object.values(sessionsByDate).length > 0
            ? Math.max(...Object.values(sessionsByDate))
            : 0;

        // Aggiorna il DOM
        this.dom.totalSessions.textContent = totalSessions;
        this.dom.totalTime.textContent = totalMinutes;
        this.dom.bestDay.textContent = bestDay;
    }

    // ============================================
    // METODO SAVESTATS - Salva in localStorage
    // ============================================
    saveStats() {
        // Crea oggetto dati da salvare
        const data = {
            todaySessions: this.todaySessions,
            sessionHistory: this.sessionHistory,
            lastSaveDate: new Date().toLocaleDateString('it-IT')
        };

        // Converti in JSON e salva
        // ES6: JSON.stringify() per serializzare
        localStorage.setItem('pomodoroStats', JSON.stringify(data));

        console.log('💾 Statistiche salvate');
    }

    // ============================================
    // METODO LOADSTATS - Carica da localStorage
    // ============================================
    loadStats() {
        try {
            // Leggi da localStorage
            const savedData = localStorage.getItem('pomodoroStats');

            if (savedData) {
                // ES6: JSON.parse() per deserializzare
                const data = JSON.parse(savedData);

                // Controlla se i dati sono di oggi
                const today = new Date().toLocaleDateString('it-IT');

                if (data.lastSaveDate === today) {
                    // Ripristina i dati di oggi
                    this.todaySessions = data.todaySessions || 0;
                    this.sessionHistory = data.sessionHistory || [];
                } else {
                    // Nuovo giorno: resetta le sessioni di oggi
                    this.todaySessions = 0;
                    this.sessionHistory = data.sessionHistory || [];
                }
            }
        } catch (error) {
            // ES6: Gestione errori con try-catch
            console.error('Errore nel caricamento delle statistiche:', error);
        }
    }

    // ============================================
    // METODO CLEARSTATS - Cancella tutte le statistiche
    // ============================================
    clearStats() {
        // Conferma con l'utente
        if (!confirm('Sei sicuro di voler cancellare tutte le statistiche?')) {
            return;
        }

        // Resetta i dati
        this.todaySessions = 0;
        this.sessionHistory = [];

        // Cancella da localStorage
        localStorage.removeItem('pomodoroStats');

        // Aggiorna UI
        this.renderSessionDots();
        this.renderSessionLog();
        this.updateStats();

        console.log('🗑️ Statistiche cancellate');
    }

    // ============================================
    // METODO PLAYNOTIFICATIONSOUND - Riproduci suono
    // ============================================
    playNotificationSound() {
        try {
            // Crea un contesto audio
            // ES6: API Web Audio per generare suoni senza file esterni
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();

            // Crea oscillatore per il suono
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            // Configura il suono
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            // Frequenza e tipo di onda
            oscillator.frequency.value = 800;  // Hz
            oscillator.type = 'sine';

            // Volume
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(
                0.01,
                audioContext.currentTime + 0.5
            );

            // Avvia e ferma il suono
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (error) {
            console.error('Errore nella riproduzione del suono:', error);
        }
    }

    // ============================================
    // METODO SHOWNOTIFICATION - Mostra notifica browser
    // ============================================
    showNotification(message) {
        // API Notification del browser
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Pomodoro Timer', {
                body: message,
                icon: '🍅',
                badge: '🍅'
            });
        }

        // Fallback con alert se le notifiche non sono disponibili
        alert(message);
    }
}

// ============================================
// INIZIALIZZAZIONE
// ============================================
// ES6: DOMContentLoaded assicura che il DOM sia pronto
document.addEventListener('DOMContentLoaded', () => {
    // Richiedi permesso per le notifiche
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }

    // Crea istanza del timer
    const timer = new PomodoroTimer();

    // Log di benvenuto
    console.log(`
╔════════════════════════════════════════╗
║     🍅 POMODORO TIMER AVVIATO 🍅       ║
║                                        ║
║  Tecniche JavaScript ES6+ utilizzate:  ║
║  ✅ Classi ES6                         ║
║  ✅ Arrow functions                    ║
║  ✅ Template literals                   ║
║  ✅ Destructuring                       ║
║  ✅ Spread operator                     ║
║  ✅ Array methods (map, filter, etc)    ║
║  ✅ LocalStorage API                    ║
║  ✅ Web Audio API                       ║
║  ✅ DOM manipulation                    ║
╚════════════════════════════════════════╝
    `);
});

// ============================================
// NOTE EDUCATIVE PER STUDENTI
// ============================================
/*
ES6+ FEATURES UTILIZZATE IN QUESTO PROGETTO:

1. CLASSI (ES6 2015)
   - Sintassi più chiara per creare oggetti
   - Constructor per inizializzazione
   - Metodi senza bisogno della parola chiave 'function'

2. ARROW FUNCTIONS (ES6 2015)
   - Sintassi concisa: () => {}
   - Mantengono automaticamente il contesto 'this'
   - Ideali per callback e event listeners

3. TEMPLATE LITERALS (ES6 2015)
   - Stringhe con backtick: `testo ${variabile}`
   - Supporto multi-linea
   - Expression embedding

4. DESTRUCTURING
   - Estrazione proprietà da oggetti
   - Spesso usato con: const { proprietà } = oggetto

5. SPREAD OPERATOR (ES6 2015)
   - ...array espande un array
   - Utile con Math.max(), concatenazione array

6. ARRAY METHODS
   - forEach(): esegue funzione per ogni elemento
   - filter(): crea nuovo array con elementi filtrati
   - map(): trasforma ogni elemento
   - find(): trova primo elemento che soddisfa condizione
   - reduce(): riduce array a singolo valore

7. LET & CONST (ES6 2015)
   - const: per variabili che non cambiano
   - let: per variabili che cambiano
   - Sostituiscono 'var' (scope a blocchi)

8. LOCALSTORAGE API
   - Salvataggio dati nel browser
   - JSON.stringify() per salvare
   - JSON.parse() per caricare

9. WEB AUDIO API
   - Generazione suoni senza file esterni
   - AudioContext per controllo audio

10. MODERN DOM MANIPULATION
    - querySelector(), querySelectorAll()
    - addEventListener()
    - classList per gestione classi CSS

CONSIGLI PER APPROFONDIRE:
- Studio: MDN Web Docs (developer.mozilla.org)
- Pratica: Modifica i tempi, aggiungi funzionalità
- Sperimenta: Prova altre API browser (Geolocation, etc.)
*/
