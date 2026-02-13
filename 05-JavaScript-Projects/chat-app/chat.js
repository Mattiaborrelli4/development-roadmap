/**
 * Chat Application - Sistema di Messaggistica in Tempo Reale (Simulato)
 *
 * Caratteristiche:
 * - Messaggistica in tempo reale (simulata)
 * - Più stanze di chat
 * - Cronologia messaggi persistente
 * - Utenti online simulati
 * - Gestione username
 * - Timestamp dei messaggi
 * - Indicatore di digitazione
 */

class ChatApplication {
    constructor() {
        this.currentUser = null;
        this.currentRoom = 'generale';
        this.messages = {};
        this.onlineUsers = [];
        this.simulationInterval = null;
        this.typingTimeout = null;

        // Inizializza le stanze
        this.rooms = ['generale', 'tecnologia', 'musica', 'giochi', 'off-topic'];
        this.rooms.forEach(room => {
            this.messages[room] = this.loadMessagesFromStorage(room);
        });

        // Lista di utenti simulati
        this.simulatedUsers = [
            { name: 'Mario', avatar: 'M', color: '#e74c3c' },
            { name: 'Luca', avatar: 'L', color: '#3498db' },
            { name: 'Giulia', avatar: 'G', color: '#9b59b6' },
            { name: 'Anna', avatar: 'A', color: '#e91e63' },
            { name: 'Marco', avatar: 'M', color: '#00bcd4' },
            { name: 'Sofia', avatar: 'S', color: '#4caf50' },
            { name: 'Paolo', avatar: 'P', color: '#ff9800' },
            { name: 'Elena', avatar: 'E', color: '#673ab7' }
        ];

        this.bindEvents();
        this.checkExistingSession();
    }

    /**
     * Verifica se esiste una sessione salvata
     */
    checkExistingSession() {
        const savedUser = localStorage.getItem('chatUsername');
        if (savedUser) {
            this.currentUser = savedUser;
            this.showChat();
        }
    }

    /**
     * Bind degli eventi DOM
     */
    bindEvents() {
        // Login form
        const loginForm = document.getElementById('loginForm');
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // Message form
        const messageForm = document.getElementById('messageForm');
        messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Room selection
        const roomItems = document.querySelectorAll('.room-item');
        roomItems.forEach(item => {
            item.addEventListener('click', () => {
                const room = item.dataset.room;
                this.switchRoom(room);
            });
        });

        // Logout button
        const logoutBtn = document.getElementById('logoutBtn');
        logoutBtn.addEventListener('click', () => this.handleLogout());

        // Clear history
        const clearHistory = document.getElementById('clearHistory');
        clearHistory.addEventListener('click', () => this.clearRoomHistory());

        // Typing indicator
        const messageInput = document.getElementById('messageInput');
        messageInput.addEventListener('input', () => this.handleTyping());
    }

    /**
     * Gestione del login
     */
    handleLogin() {
        const usernameInput = document.getElementById('usernameInput');
        const username = usernameInput.value.trim();

        if (username.length < 2) {
            alert('Lo username deve avere almeno 2 caratteri!');
            return;
        }

        this.currentUser = username;
        localStorage.setItem('chatUsername', username);
        this.showChat();
    }

    /**
     * Mostra l'interfaccia di chat
     */
    showChat() {
        document.getElementById('loginModal').style.display = 'none';
        document.getElementById('chatContainer').classList.remove('hidden');

        // Aggiorna l'interfaccia utente
        document.getElementById('currentUsername').textContent = this.currentUser;
        document.getElementById('userAvatar').textContent = this.currentUser.charAt(0).toUpperCase();

        // Inizializza la lista utenti online
        this.initializeOnlineUsers();

        // Carica i messaggi della stanza corrente
        this.displayMessages();

        // Avvia la simulazione
        this.startSimulation();
    }

    /**
     * Gestisce il logout
     */
    handleLogout() {
        if (confirm('Sei sicuro di voler uscire?')) {
            this.stopSimulation();
            localStorage.removeItem('chatUsername');
            this.currentUser = null;
            document.getElementById('chatContainer').classList.add('hidden');
            document.getElementById('loginModal').style.display = 'flex';
            document.getElementById('usernameInput').value = '';
        }
    }

    /**
     * Inizializza la lista utenti online
     */
    initializeOnlineUsers() {
        // Aggiungi l'utente corrente
        this.onlineUsers = [
            { name: this.currentUser, avatar: this.currentUser.charAt(0).toUpperCase(), isCurrentUser: true }
        ];

        // Aggiunge 3-6 utenti simulati casuali
        const shuffled = [...this.simulatedUsers].sort(() => 0.5 - Math.random());
        const selectedUsers = shuffled.slice(0, Math.floor(Math.random() * 4) + 3);

        this.onlineUsers.push(...selectedUsers.map(user => ({
            name: user.name,
            avatar: user.avatar,
            color: user.color,
            isCurrentUser: false
        })));

        this.renderOnlineUsers();
    }

    /**
     * Renderizza la lista utenti online
     */
    renderOnlineUsers() {
        const usersList = document.getElementById('onlineUsers');
        usersList.innerHTML = this.onlineUsers.map(user => `
            <li>
                <div class="user-avatar" style="${user.color ? 'background:' + user.color : ''}">
                    ${user.avatar}
                </div>
                <span class="user-name">${user.name}${user.isCurrentUser ? ' (Tu)' : ''}</span>
            </li>
        `).join('');
    }

    /**
     * Cambia stanza
     */
    switchRoom(roomName) {
        if (this.currentRoom === roomName) return;

        this.currentRoom = roomName;

        // Aggiorna UI
        document.querySelectorAll('.room-item').forEach(item => {
            item.classList.remove('active');
            if (item.dataset.room === roomName) {
                item.classList.add('active');
            }
        });

        document.getElementById('currentRoom').textContent = roomName;
        document.getElementById('welcomeRoom').textContent = `#${roomName}`;

        // Nascondi badge
        const badge = document.getElementById(`badge-${roomName}`);
        if (badge) {
            badge.classList.remove('show');
        }

        // Carica messaggi della nuova stanza
        this.displayMessages();
    }

    /**
     * Invia un messaggio
     */
    sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const text = messageInput.value.trim();

        if (!text) return;

        const message = {
            id: Date.now(),
            username: this.currentUser,
            avatar: this.currentUser.charAt(0).toUpperCase(),
            text: text,
            timestamp: new Date().toISOString(),
            room: this.currentRoom,
            isOwn: true
        };

        // Aggiungi alla lista messaggi
        if (!this.messages[this.currentRoom]) {
            this.messages[this.currentRoom] = [];
        }
        this.messages[this.currentRoom].push(message);

        // Salva nel localStorage
        this.saveMessagesToStorage(this.currentRoom);

        // Renderizza
        this.renderMessage(message);

        // Pulisci input
        messageInput.value = '';
        messageInput.focus();

        // Scroll to bottom
        this.scrollToBottom();
    }

    /**
     * Visualizza tutti i messaggi della stanza corrente
     */
    displayMessages() {
        const container = document.getElementById('messagesContainer');
        const roomMessages = this.messages[this.currentRoom] || [];

        if (roomMessages.length === 0) {
            container.innerHTML = `
                <div class="welcome-message">
                    <h3>Benvenuto nella stanza <span>#${this.currentRoom}</span>!</h3>
                    <p>Questa è un'applicazione di chat simulata con persistenza locale.</p>
                    <p>I messaggi vengono salvati nel tuo browser e restano disponibili anche dopo la chiusura.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = roomMessages.map(msg => this.createMessageHTML(msg)).join('');
        this.scrollToBottom();
    }

    /**
     * Renderizza un singolo messaggio
     */
    renderMessage(message) {
        const container = document.getElementById('messagesContainer');

        // Rimuovi il messaggio di benvenuto se presente
        const welcomeMsg = container.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }

        const messageHTML = this.createMessageHTML(message);
        container.insertAdjacentHTML('beforeend', messageHTML);
    }

    /**
     * Crea l'HTML di un messaggio
     */
    createMessageHTML(message) {
        const date = new Date(message.timestamp);
        const timeStr = date.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
        const dateStr = date.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric' });

        return `
            <div class="message ${message.isOwn ? 'own' : ''}" data-id="${message.id}">
                <div class="message-avatar" style="${message.color ? 'background:' + message.color : ''}">
                    ${message.avatar}
                </div>
                <div class="message-content">
                    <div class="message-header">
                        <span class="message-username">${message.username}</span>
                        <span class="message-timestamp" title="${dateStr} ${timeStr}">${timeStr}</span>
                    </div>
                    <div class="message-text">${this.escapeHTML(message.text)}</div>
                </div>
            </div>
        `;
    }

    /**
     * Escape HTML per prevenire XSS
     */
    escapeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    /**
     * Gestisce l'indicatore di digitazione
     */
    handleTyping() {
        // Reset timer
        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
        }

        // Simula altri utenti che scrivono
        if (Math.random() > 0.7) {
            this.showTypingIndicator();
        }

        this.typingTimeout = setTimeout(() => {
            this.hideTypingIndicator();
        }, 1000);
    }

    /**
     * Mostra l'indicatore di digitazione
     */
    showTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        indicator.classList.add('show');
        setTimeout(() => {
            indicator.classList.remove('show');
        }, 3000);
    }

    /**
     * Nasconde l'indicatore di digitazione
     */
    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        indicator.classList.remove('show');
    }

    /**
     * Scrolla in fondo alla chat
     */
    scrollToBottom() {
        const container = document.getElementById('messagesContainer');
        container.scrollTop = container.scrollHeight;
    }

    /**
     * Salva i messaggi nel localStorage
     */
    saveMessagesToStorage(room) {
        try {
            const key = `chat_messages_${room}`;
            localStorage.setItem(key, JSON.stringify(this.messages[room]));
        } catch (e) {
            console.error('Errore nel salvare i messaggi:', e);
        }
    }

    /**
     * Carica i messaggi dal localStorage
     */
    loadMessagesFromStorage(room) {
        try {
            const key = `chat_messages_${room}`;
            const stored = localStorage.getItem(key);
            return stored ? JSON.parse(stored) : [];
        } catch (e) {
            console.error('Errore nel caricare i messaggi:', e);
            return [];
        }
    }

    /**
     * Cancella la cronologia della stanza corrente
     */
    clearRoomHistory() {
        if (confirm(`Sei sicuro di voler cancellare tutti i messaggi dalla stanza #${this.currentRoom}?`)) {
            this.messages[this.currentRoom] = [];
            localStorage.removeItem(`chat_messages_${this.currentRoom}`);
            this.displayMessages();
        }
    }

    /**
     * Avvia la simulazione di messaggi in tempo reale
     */
    startSimulation() {
        // Simula un nuovo messaggio ogni 15-30 secondi
        this.simulationInterval = setInterval(() => {
            if (Math.random() > 0.3) {
                this.simulateIncomingMessage();
            }
        }, 15000);

        // Simula cambiamenti nella lista utenti online ogni 45-60 secondi
        setInterval(() => {
            this.simulateUserActivity();
        }, 45000);
    }

    /**
     * Ferma la simulazione
     */
    stopSimulation() {
        if (this.simulationInterval) {
            clearInterval(this.simulationInterval);
            this.simulationInterval = null;
        }
    }

    /**
     * Simula un messaggio in arrivo
     */
    simulateIncomingMessage() {
        // Scegli un utente casuale (non l'utente corrente)
        const otherUsers = this.onlineUsers.filter(u => !u.isCurrentUser);
        if (otherUsers.length === 0) return;

        const randomUser = otherUsers[Math.floor(Math.random() * otherUsers.length)];

        // Scegli una stanza casuale con probabilità più alta per la stanza corrente
        let randomRoom;
        if (Math.random() > 0.4) {
            randomRoom = this.currentRoom;
        } else {
            randomRoom = this.rooms[Math.floor(Math.random() * this.rooms.length)];
        }

        // Messaggi di esempio basati sulla stanza
        const sampleMessages = {
            'generale': [
                'Ciao a tutti! 👋',
                'Qualcuno ha visto l\'ultimo film uscito?',
                'Che bella giornata oggi!',
                'Qualcuno vuole fare una partita?',
                'Ragazzi, avete sentito la notizia?',
                'Oggi è tutto tranquillo...',
                'Chi è online adesso?'
            ],
            'tecnologia': [
                'Avete provato il nuovo framework JavaScript?',
                'Qualcuno usa VS Code? È fantastico!',
                'Sto imparando React, è incredibile!',
                'Python o JavaScript? Voi cosa scegliete?',
                'Ho appena aggiornato il mio PC!',
                'Qualcuno sa come risolvere questo bug?',
                'La programmazione è arte! 🎨'
            ],
            'musica': [
                'Avete sentito l\'ultimo album?',
                'Che canzone state ascoltando?',
                'Consigli musicali per il weekend?',
                'Il concerto di ieri era pazzesco! 🎵',
                'Spotify o Apple Music?',
                'Sto imparando a suonare la chitarra',
                'Playlist consigliata per studiare?'
            ],
            'giochi': [
                'Qualcuno gioca a Valorant?',
                'Partita stasera?',
                'Ho appena finito Elden Ring!',
                'Console o PC? 🎮',
                'Che gioco state giocando?',
                'Livello massimo raggiunto!',
                'Qualcuno vuole fare squadra?'
            ],
            'off-topic': [
                'Qualcuno ha visto le stasera?',
                'Ricordo quando eravamo giovani...',
                'Ricetta preferita di tutti?',
                'Che tempo fa oggi?',
                'Avete visto il video virale?',
                'Discussione filosofica: perché siamo qui?',
                'Random fact: lo sapevate che...?'
            ]
        };

        const messages = sampleMessages[randomRoom] || sampleMessages['generale'];
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];

        const message = {
            id: Date.now(),
            username: randomUser.name,
            avatar: randomUser.avatar,
            text: randomMessage,
            timestamp: new Date().toISOString(),
            room: randomRoom,
            isOwn: false,
            color: randomUser.color
        };

        // Aggiungi alla stanza appropriata
        if (!this.messages[randomRoom]) {
            this.messages[randomRoom] = [];
        }
        this.messages[randomRoom].push(message);

        // Salva
        this.saveMessagesToStorage(randomRoom);

        // Se è la stanza corrente, renderizza
        if (randomRoom === this.currentRoom) {
            this.renderMessage(message);
            this.scrollToBottom();

            // Mostra notifica visiva
            this.showTypingIndicator();
            setTimeout(() => this.hideTypingIndicator(), 1500);
        } else {
            // Aggiorna badge
            const badge = document.getElementById(`badge-${randomRoom}`);
            if (badge) {
                const currentCount = parseInt(badge.textContent) || 0;
                badge.textContent = currentCount + 1;
                badge.classList.add('show');
            }
        }
    }

    /**
     * Simula attività degli utenti (login/logout)
     */
    simulateUserActivity() {
        const action = Math.random() > 0.5 ? 'join' : 'leave';

        if (action === 'join' && this.onlineUsers.length < 10) {
            // Aggiungi un nuovo utente
            const availableUsers = this.simulatedUsers.filter(
                u => !this.onlineUsers.some(ou => ou.name === u.name)
            );

            if (availableUsers.length > 0) {
                const newUser = availableUsers[Math.floor(Math.random() * availableUsers.length)];
                this.onlineUsers.push({
                    name: newUser.name,
                    avatar: newUser.avatar,
                    color: newUser.color,
                    isCurrentUser: false
                });
                this.renderOnlineUsers();
            }
        } else if (action === 'leave' && this.onlineUsers.length > 2) {
            // Rimuovi un utente (non l'utente corrente)
            const otherUsers = this.onlineUsers.filter(u => !u.isCurrentUser);
            if (otherUsers.length > 0) {
                const userToRemove = otherUsers[Math.floor(Math.random() * otherUsers.length)];
                this.onlineUsers = this.onlineUsers.filter(u => u.name !== userToRemove.name);
                this.renderOnlineUsers();
            }
        }
    }
}

// Inizializza l'applicazione quando il DOM è caricato
document.addEventListener('DOMContentLoaded', () => {
    new ChatApplication();
});
