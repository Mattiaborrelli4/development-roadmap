// ========== CALCULATOR CLASS ==========
class Calculator {
    constructor(previousOperandTextElement, currentOperandTextElement) {
        this.previousOperandTextElement = previousOperandTextElement;
        this.currentOperandTextElement = currentOperandTextElement;
        this.clear();
    }

    clear() {
        this.currentOperand = '0';
        this.previousOperand = '';
        this.operation = undefined;
        this.shouldResetScreen = false;
    }

    delete() {
        if (this.shouldResetScreen) {
            this.currentOperand = '0';
            this.shouldResetScreen = false;
            return;
        }

        if (this.currentOperand === '0') return;

        this.currentOperand = this.currentOperand.toString().slice(0, -1);

        if (this.currentOperand === '' || this.currentOperand === '-') {
            this.currentOperand = '0';
        }
    }

    appendNumber(number) {
        if (this.shouldResetScreen) {
            this.currentOperand = '';
            this.shouldResetScreen = false;
        }

        // Prevent multiple leading zeros
        if (this.currentOperand === '0' && number === '0') return;

        // Replace single zero with number
        if (this.currentOperand === '0' && number !== '.') {
            this.currentOperand = number;
            return;
        }

        // Prevent multiple decimal points
        if (number === '.' && this.currentOperand.includes('.')) return;

        this.currentOperand = this.currentOperand.toString() + number.toString();
    }

    chooseOperation(operation) {
        if (this.currentOperand === '') return;

        if (this.previousOperand !== '') {
            this.compute();
        }

        this.operation = operation;
        this.previousOperand = this.currentOperand;
        this.shouldResetScreen = true;
    }

    compute() {
        let computation;
        const prev = parseFloat(this.previousOperand);
        const current = parseFloat(this.currentOperand);

        if (isNaN(prev) || isNaN(current)) return;

        switch (this.operation) {
            case '+':
                computation = prev + current;
                break;
            case '-':
                computation = prev - current;
                break;
            case '×':
                computation = prev * current;
                break;
            case '÷':
                if (current === 0) {
                    this.currentOperand = 'Errore';
                    this.previousOperand = '';
                    this.operation = undefined;
                    this.shouldResetScreen = true;
                    return;
                }
                computation = prev / current;
                break;
            default:
                return;
        }

        // Round to avoid floating point precision issues
        computation = Math.round(computation * 1000000000) / 1000000000;

        this.currentOperand = computation.toString();
        this.operation = undefined;
        this.previousOperand = '';
        this.shouldResetScreen = true;
    }

    negate() {
        if (this.currentOperand === '0') return;

        const current = parseFloat(this.currentOperand);
        this.currentOperand = (current * -1).toString();
    }

    percentage() {
        const current = parseFloat(this.currentOperand);
        if (isNaN(current)) return;

        this.currentOperand = (current / 100).toString();
        this.shouldResetScreen = true;
    }

    getDisplayNumber(number) {
        if (number === 'Errore') return number;

        const stringNumber = number.toString();
        const integerDigits = parseFloat(stringNumber.split('.')[0]);
        const decimalDigits = stringNumber.split('.')[1];

        let integerDisplay;
        if (isNaN(integerDigits)) {
            integerDisplay = '';
        } else {
            integerDisplay = integerDigits.toLocaleString('it-IT', {
                maximumFractionDigits: 0
            });
        }

        if (decimalDigits != null) {
            return `${integerDisplay}.${decimalDigits}`;
        } else {
            return integerDisplay;
        }
    }

    updateDisplay() {
        this.currentOperandTextElement.innerText = this.getDisplayNumber(this.currentOperand);

        if (this.operation != null) {
            this.previousOperandTextElement.innerText =
                `${this.getDisplayNumber(this.previousOperand)} ${this.operation}`;
        } else {
            this.previousOperandTextElement.innerText = '';
        }
    }
}

// ========== INITIALIZE CALCULATOR ==========
const previousOperandTextElement = document.getElementById('previousOperand');
const currentOperandTextElement = document.getElementById('currentOperand');
const calculator = new Calculator(previousOperandTextElement, currentOperandTextElement);

// ========== BUTTON HANDLERS ==========
document.querySelectorAll('.button').forEach(button => {
    button.addEventListener('click', () => {
        const action = button.dataset.action;

        // Add visual feedback
        button.classList.add('active');
        setTimeout(() => button.classList.remove('active'), 100);

        switch (action) {
            case 'number':
                calculator.appendNumber(button.dataset.value);
                calculator.updateDisplay();
                break;

            case 'operator':
                calculator.chooseOperation(button.dataset.value);
                calculator.updateDisplay();
                break;

            case 'equals':
                calculator.compute();
                calculator.updateDisplay();
                break;

            case 'clear':
                calculator.clear();
                calculator.updateDisplay();
                break;

            case 'backspace':
                calculator.delete();
                calculator.updateDisplay();
                break;

            case 'decimal':
                calculator.appendNumber('.');
                calculator.updateDisplay();
                break;

            case 'negate':
                calculator.negate();
                calculator.updateDisplay();
                break;

            case 'percent':
                calculator.percentage();
                calculator.updateDisplay();
                break;
        }
    });
});

// ========== KEYBOARD SUPPORT ==========
document.addEventListener('keydown', (e) => {
    let button;

    if ((e.key >= '0' && e.key <= '9')) {
        button = document.querySelector(`[data-value="${e.key}"]`);
    } else if (e.key === '.') {
        button = document.querySelector('[data-action="decimal"]');
    } else if (e.key === '+') {
        button = document.querySelector('[data-value="+"]');
    } else if (e.key === '-') {
        button = document.querySelector('[data-value="-"]');
    } else if (e.key === '*') {
        button = document.querySelector('[data-value="×"]');
    } else if (e.key === '/') {
        e.preventDefault(); // Prevent Firefox quick find
        button = document.querySelector('[data-value="÷"]');
    } else if (e.key === 'Enter' || e.key === '=') {
        button = document.querySelector('[data-action="equals"]');
    } else if (e.key === 'Backspace') {
        button = document.querySelector('[data-action="backspace"]');
    } else if (e.key === 'Escape' || e.key === 'c' || e.key === 'C') {
        button = document.querySelector('[data-action="clear"]');
    } else if (e.key === '%') {
        button = document.querySelector('[data-action="percent"]');
    }

    if (button) {
        button.click();
        button.focus();
    }
});

// ========== PWA INSTALLATION ==========
let deferredPrompt;
const installPrompt = document.getElementById('installPrompt');
const installButton = document.getElementById('installButton');
const dismissButton = document.getElementById('dismissButton');

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;
    // Show the install prompt
    installPrompt.classList.remove('hidden');
});

installButton.addEventListener('click', async () => {
    if (!deferredPrompt) {
        // If the prompt is not available, try to show the browser's install UI
        return;
    }

    // Show the install prompt
    deferredPrompt.prompt();

    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.userChoice;

    // The user responded to the prompt
    if (outcome === 'accepted') {
        console.log('L\'utente ha accettato l\'installazione');
    } else {
        console.log('L\'utente ha rifiutato l\'installazione');
    }

    // Clear the deferred prompt
    deferredPrompt = null;
    installPrompt.classList.add('hidden');
});

dismissButton.addEventListener('click', () => {
    installPrompt.classList.add('hidden');
});

window.addEventListener('appinstalled', () => {
    // App was installed
    installPrompt.classList.add('hidden');
    deferredPrompt = null;
});

// ========== SERVICE WORKER REGISTRATION ==========
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
            .then((registration) => {
                console.log('Service Worker registrato con successo:', registration.scope);
            })
            .catch((error) => {
                console.log('Registrazione Service Worker fallita:', error);
            });
    });
}

// ========== TOUCH FEEDBACK ==========
// Add haptic feedback on supported devices
if ('vibrate' in navigator) {
    document.querySelectorAll('.button').forEach(button => {
        button.addEventListener('click', () => {
            navigator.vibrate(10); // Light vibration for 10ms
        });
    });
}

// Prevent double-tap zoom on mobile
document.addEventListener('touchend', (e) => {
    e.preventDefault();
    e.target.click();
}, { passive: false });
