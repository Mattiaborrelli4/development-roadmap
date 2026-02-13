// ==================== Configuration ====================
const CONFIG = {
    API_URL: 'https://api.exchangerate-api.com/v4/latest/',
    STORAGE_KEY: 'currency_converter_history',
    MAX_HISTORY: 10
};

// ==================== DOM Elements ====================
const elements = {
    amountInput: document.getElementById('amount'),
    fromCurrency: document.getElementById('from-currency'),
    toCurrency: document.getElementById('to-currency'),
    convertButton: document.getElementById('convert-button'),
    swapButton: document.getElementById('swap-button'),
    resultSection: document.getElementById('result-section'),
    resultAmount: document.getElementById('result-amount'),
    resultDetails: document.getElementById('result-details'),
    ratesInfo: document.getElementById('rates-info'),
    lastUpdate: document.getElementById('last-update'),
    alert: document.getElementById('alert'),
    historyList: document.getElementById('history-list'),
    clearHistoryButton: document.getElementById('clear-history'),
    amountError: document.getElementById('amount-error')
};

// ==================== State ====================
let cachedRates = null;
let lastFetchTime = null;

// ==================== Currency Symbols ====================
const currencySymbols = {
    USD: '$',
    EUR: '€',
    GBP: '£',
    JPY: '¥',
    CHF: 'CHF',
    CAD: 'C$',
    AUD: 'A$'
};

// ==================== Utility Functions ====================

/**
 * Formatta un numero con il simbolo di valuta
 */
const formatCurrency = (amount, currency) => {
    const symbol = currencySymbols[currency] || currency;
    return `${symbol} ${parseFloat(amount).toLocaleString('it-IT', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })}`;
};

/**
 * Formatta la data e ora corrente
 */
const formatDateTime = () => {
    const now = new Date();
    return now.toLocaleString('it-IT', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

/**
 * Mostra un messaggio di alert
 */
const showAlert = (message, type = 'info') => {
    elements.alert.textContent = message;
    elements.alert.className = `alert ${type} active`;

    setTimeout(() => {
        elements.alert.classList.remove('active');
    }, 5000);
};

/**
 * Nasconde la sezione risultato
 */
const hideResult = () => {
    elements.resultSection.classList.remove('active');
};

/**
 * Mostra la sezione risultato
 */
const showResult = () => {
    elements.resultSection.classList.add('active');
};

// ==================== API Functions ====================

/**
 * Recupera i tassi di cambio dall'API
 */
const fetchExchangeRates = async (baseCurrency) => {
    try {
        const response = await fetch(`${CONFIG.API_URL}${baseCurrency}`);

        if (!response.ok) {
            throw new Error(`Errore HTTP: ${response.status}`);
        }

        const data = await response.json();

        if (!data.rates) {
            throw new Error('Formato risposta API non valido');
        }

        cachedRates = data.rates;
        lastFetchTime = new Date();

        return data.rates;
    } catch (error) {
        console.error('Errore nel recupero dei tassi:', error);
        throw error;
    }
};

/**
 * Converte un importo tra due valute
 */
const convertCurrency = async (amount, from, to) => {
    if (from === to) {
        return amount;
    }

    try {
        const rates = await fetchExchangeRates(from);
        const convertedAmount = amount * rates[to];

        // Aggiorna l'informazione sull'ultimo aggiornamento
        elements.lastUpdate.textContent = formatDateTime();

        return convertedAmount;
    } catch (error) {
        throw new Error('Impossibile recuperare i tassi di cambio. Controlla la tua connessione.');
    }
};

// ==================== Validation ====================

/**
 * Valida l'input dell'importo
 */
const validateAmount = (amount) => {
    if (!amount || amount <= 0) {
        elements.amountError.textContent = 'Inserisci un importo valido maggiore di zero';
        return false;
    }

    if (amount > 1000000000) {
        elements.amountError.textContent = 'L\'importo è troppo elevato';
        return false;
    }

    elements.amountError.textContent = '';
    return true;
};

/**
 * Resetta la validazione
 */
const resetValidation = () => {
    elements.amountError.textContent = '';
};

// ==================== History Functions ====================

/**
 * Carica la cronologia dal localStorage
 */
const loadHistory = () => {
    try {
        const historyJSON = localStorage.getItem(CONFIG.STORAGE_KEY);
        return historyJSON ? JSON.parse(historyJSON) : [];
    } catch (error) {
        console.error('Errore nel caricamento della cronologia:', error);
        return [];
    }
};

/**
 * Salva la cronologia nel localStorage
 */
const saveHistory = (history) => {
    try {
        localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(history));
    } catch (error) {
        console.error('Errore nel salvataggio della cronologia:', error);
    }
};

/**
 * Aggiunge una conversione alla cronologia
 */
const addToHistory = (conversion) => {
    const history = loadHistory();

    const historyItem = {
        id: Date.now(),
        ...conversion,
        timestamp: new Date().toISOString()
    };

    // Aggiungi all'inizio dell'array
    history.unshift(historyItem);

    // Mantieni solo gli ultimi MAX_HISTORY elementi
    const trimmedHistory = history.slice(0, CONFIG.MAX_HISTORY);

    saveHistory(trimmedHistory);
    renderHistory();
};

/**
 * Rimuove un elemento dalla cronologia
 */
const removeFromHistory = (id) => {
    const history = loadHistory();
    const filteredHistory = history.filter(item => item.id !== id);
    saveHistory(filteredHistory);
    renderHistory();
};

/**
 * Cancella tutta la cronologia
 */
const clearHistory = () => {
    if (confirm('Sei sicuro di voler cancellare tutta la cronologia?')) {
        localStorage.removeItem(CONFIG.STORAGE_KEY);
        renderHistory();
        showAlert('Cronologia cancellata', 'success');
    }
};

/**
 * Renderizza la cronologia
 */
const renderHistory = () => {
    const history = loadHistory();

    if (history.length === 0) {
        elements.historyList.innerHTML = '<p class="empty-history">Nessuna conversione salvata</p>';
        return;
    }

    const historyHTML = history.map(item => `
        <div class="history-item">
            <div class="history-item-content">
                <div class="history-item-amount">
                    ${formatCurrency(item.amount, item.from)} → ${formatCurrency(item.result, item.to)}
                </div>
                <div class="history-item-details">
                    Tasso: 1 ${item.from} = ${(item.rate).toFixed(4)} ${item.to}
                </div>
            </div>
            <div class="history-item-date">
                ${new Date(item.timestamp).toLocaleString('it-IT', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                })}
                <button class="history-item-delete" onclick="removeFromHistory(${item.id})" title="Rimuovi">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `).join('');

    elements.historyList.innerHTML = historyHTML;
};

// ==================== Event Handlers ====================

/**
 * Gestisce il clic sul pulsante Converti
 */
const handleConvert = async () => {
    const amount = parseFloat(elements.amountInput.value);
    const from = elements.fromCurrency.value;
    const to = elements.toCurrency.value;

    // Validazione
    if (!validateAmount(amount)) {
        hideResult();
        return;
    }

    // Disabilita il pulsante e mostra loading
    elements.convertButton.disabled = true;
    elements.convertButton.classList.add('loading');
    hideResult();

    try {
        // Esegui la conversione
        const result = await convertCurrency(amount, from, to);

        // Calcola il tasso di cambio
        const rate = cachedRates ? cachedRates[to] : result / amount;

        // Mostra il risultato
        elements.resultAmount.textContent = formatCurrency(result, to);
        elements.resultDetails.textContent = `${formatCurrency(amount, from)} = ${formatCurrency(result, to)}`;
        showResult();

        // Aggiungi alla cronologia
        addToHistory({
            amount,
            from,
            to,
            result,
            rate
        });

        // Mostra messaggio di successo
        showAlert('Conversione completata!', 'success');

    } catch (error) {
        showAlert(error.message, 'error');
        console.error('Errore di conversione:', error);
    } finally {
        // Riabilita il pulsante e rimuovi loading
        elements.convertButton.disabled = false;
        elements.convertButton.classList.remove('loading');
    }
};

/**
 * Gestisce il clic sul pulsante Swap
 */
const handleSwap = () => {
    const fromValue = elements.fromCurrency.value;
    const toValue = elements.toCurrency.value;

    elements.fromCurrency.value = toValue;
    elements.toCurrency.value = fromValue;

    // Aggiungi animazione
    elements.swapButton.classList.add('spinning');
    setTimeout(() => {
        elements.swapButton.classList.remove('spinning');
    }, 600);

    // Se c'è un risultato, riesegui la conversione
    if (elements.resultSection.classList.contains('active')) {
        handleConvert();
    }
};

/**
 * Gestisce il cambio delle valute
 */
const handleCurrencyChange = () => {
    resetValidation();
    hideResult();
};

// ==================== Initialization ====================

/**
 * Inizializza l'applicazione
 */
const init = () => {
    // Event Listeners
    elements.convertButton.addEventListener('click', handleConvert);
    elements.swapButton.addEventListener('click', handleSwap);
    elements.clearHistoryButton.addEventListener('click', clearHistory);

    // Event listener per l'input
    elements.amountInput.addEventListener('input', () => {
        resetValidation();
        if (elements.resultSection.classList.contains('active')) {
            hideResult();
        }
    });

    // Event listener per i select
    elements.fromCurrency.addEventListener('change', handleCurrencyChange);
    elements.toCurrency.addEventListener('change', handleCurrencyChange);

    // Event listener per Enter nell'input
    elements.amountInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleConvert();
        }
    });

    // Carica la cronologia salvata
    renderHistory();

    // Imposta il focus sull'input
    elements.amountInput.focus();

    console.log('Convertitore di valuta inizializzato');
};

// ==================== Start Application ====================
document.addEventListener('DOMContentLoaded', init);
