// Common passwords list (in italiano e inglese)
const commonPasswords = [
    'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', 'master',
    'dragon', '111111', 'baseball', 'iloveyou', 'trustno1', 'sunshine',
    'princess', 'admin', 'welcome', 'shadow', 'ashley', 'football',
    'jesus', 'michael', 'ninja', 'mustang', 'password1', 'password123',
    'passw0rd', 'letmein', 'login', 'starwars', 'photoshop', 'password12',
    '123456789', '1234567890', 'qwerty123', 'qwertyuiop', 'asdfgh',
    'password!', '123abc', 'admin123', 'root', 'toor', 'test', 'guest',
    'senha', 'password1234', '1q2w3e4r', 'qazwsx', 'p@ssw0rd', 'pass',
    'passwort', 'passer', 'p@ssword', 'qwertyuiop', '123qwe', '1qaz2wsx',
    'zaq12wsx', 'football123', 'soccer', 'hockey', 'baseball123', 'batman',
    'superman', 'spiderman', 'pokemon', 'charlie', 'andrew', 'joshua',
    'jordan', 'matthew', 'hunter', 'danielle', 'amanda', 'jessica',
    'taylor', 'sophie', 'samantha', 'nicholas', 'joseph', 'alexander',
    'emily', 'chloe', 'olivia', 'emma', 'sophia', 'isabella', 'mia',
    'charlotte', 'london', 'newyork', 'america', 'europe', 'italy',
    'bonjour', 'hola', 'ciao', 'hallo', 'hello', 'welcome123'
];

// Special characters
const specialChars = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?`~]/;

// DOM elements
const passwordInput = document.getElementById('passwordInput');
const togglePassword = document.getElementById('togglePassword');
const strengthBar = document.getElementById('strengthBar');
const strengthLabel = document.getElementById('strengthLabel');
const scoreValue = document.getElementById('scoreValue');
const tipsList = document.getElementById('tipsList');
const lengthInfo = document.getElementById('lengthInfo');
const charsInfo = document.getElementById('charsInfo');
const crackTimeInfo = document.getElementById('crackTimeInfo');
const criteriaItems = document.querySelectorAll('.criterion');

// Password strength checker class
class PasswordStrengthChecker {
    constructor(password) {
        this.password = password;
        this.criteria = {
            length: password.length >= 8,
            numbers: /\d/.test(password),
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            special: specialChars.test(password),
            common: !this.isCommonPassword(password)
        };
    }

    isCommonPassword(password) {
        return commonPasswords.includes(password.toLowerCase());
    }

    calculateScore() {
        let score = 0;
        const passedCriteria = Object.values(this.criteria).filter(Boolean).length;

        // Base score from criteria
        score = passedCriteria;

        // Bonus for extra length
        if (this.password.length >= 12) score += 0.5;
        if (this.password.length >= 16) score += 0.5;

        // Bonus for complexity
        if (this.criteria.numbers && this.criteria.uppercase &&
            this.criteria.lowercase && this.criteria.special) {
            score += 0.5;
        }

        // Penalty for common passwords
        if (this.criteria.common === false) {
            score = Math.min(score, 1);
        }

        return Math.min(Math.round(score), 5);
    }

    getStrengthLabel() {
        const score = this.calculateScore();
        const labels = {
            0: 'Molto Debole',
            1: 'Debole',
            2: 'Discreta',
            3: 'Buona',
            4: 'Forte',
            5: 'Molto Forte'
        };
        return labels[score] || '-';
    }

    getTips() {
        const tips = [];

        if (!this.password) {
            return ['Inizia a digitare per ricevere consigli personalizzati'];
        }

        if (this.password.length < 8) {
            tips.push(`La password è troppo corta. Aggiungi almeno ${8 - this.password.length} caratteri.`);
        } else if (this.password.length < 12) {
            tips.push('Considera di usare almeno 12 caratteri per maggiore sicurezza.');
        }

        if (!this.criteria.numbers) {
            tips.push('Aggiungi alcuni numeri per aumentare la complessità.');
        }

        if (!this.criteria.uppercase) {
            tips.push('Inserisci lettere maiuscole per rendere la password più forte.');
        }

        if (!this.criteria.lowercase) {
            tips.push('Usa lettere minuscole nella tua password.');
        }

        if (!this.criteria.special) {
            tips.push('Includi caratteri speciali come !@#$% per aumentare la sicurezza.');
        }

        if (this.criteria.common === false) {
            tips.push('Questa è una password molto comune! Scegline un\'unica e difficile da indovinare.');
        }

        if (this.calculateScore() >= 4 && tips.length === 0) {
            tips.push('Ottimo lavoro! La tua password è molto forte.');
            tips.push('Ricorda di usare una password diversa per ogni account.');
        }

        return tips;
    }

    getCharTypes() {
        const types = [];
        if (this.criteria.lowercase) types.push('Minuscole');
        if (this.criteria.uppercase) types.push('Maiuscole');
        if (this.criteria.numbers) types.push('Numeri');
        if (this.criteria.special) types.push('Speciali');
        return types.length > 0 ? types.join(', ') : '-';
    }

    estimateCrackTime() {
        if (!this.password) return '-';

        const length = this.password.length;
        const poolSize = this.getPoolSize();
        const combinations = Math.pow(poolSize, length);

        // Assumiamo 10 miliardi di tentativi al secondo (hash veloce)
        const guessesPerSecond = 10_000_000_000;
        const secondsToCrack = combinations / (2 * guessesPerSecond);

        if (combinations < 1000) return 'Istantaneo';
        if (secondsToCrack < 60) return 'Meno di 1 minuto';
        if (secondsToCrack < 3600) return `${Math.round(secondsToCrack / 60)} minuti`;
        if (secondsToCrack < 86400) return `${Math.round(secondsToCrack / 3600)} ore`;
        if (secondsToCrack < 2592000) return `${Math.round(secondsToCrack / 86400)} giorni`;
        if (secondsToCrack < 31536000) return `${Math.round(secondsToCrack / 2592000)} mesi`;
        if (secondsToCrack < 3153600000) return `${Math.round(secondsToCrack / 31536000)} anni`;
        if (secondsToCrack < 3153600000000) return `${Math.round(secondsToCrack / 31536000000)} secoli';
        if (secondsToCrack < 3.1536e17) return milioniDiAnni(Math.round(secondsToCrack / 3.1536e15));
        return 'Milioni di anni';
    }

    getPoolSize() {
        let pool = 0;
        if (this.criteria.lowercase) pool += 26;
        if (this.criteria.uppercase) pool += 26;
        if (this.criteria.numbers) pool += 10;
        if (this.criteria.special) pool += 32;
        return Math.max(pool, 1);
    }
}

function milioniDiAnni(anni) {
    if (anni >= 1000000000) return `${(anni / 1000000000).toFixed(1)} miliardi di anni`;
    if (anni >= 1000000) return `${(anni / 1000000).toFixed(1)} milioni di anni`;
    return `${anni} anni`;
}

// Update UI
function updateUI(password) {
    const checker = new PasswordStrengthChecker(password);
    const score = checker.calculateScore();

    // Update strength bar
    const percentage = (score / 5) * 100;
    strengthBar.style.width = `${percentage}%`;
    strengthBar.className = `strength-bar strength-${score}`;

    // Update strength label and score
    strengthLabel.textContent = checker.getStrengthLabel();
    scoreValue.textContent = score;

    // Update criteria
    Object.keys(checker.criteria).forEach((key, index) => {
        const item = document.querySelector(`[data-criteria="${key}"]`);
        if (item) {
            if (checker.criteria[key]) {
                item.classList.add('passed');
                item.querySelector('.icon').textContent = '✓';
            } else {
                item.classList.remove('passed');
                item.querySelector('.icon').textContent = '❌';
            }
        }
    });

    // Update tips
    const tips = checker.getTips();
    tipsList.innerHTML = tips.map(tip => `<li>${tip}</li>`).join('');

    // Update info section
    lengthInfo.textContent = `${password.length} caratteri`;
    charsInfo.textContent = checker.getCharTypes();
    crackTimeInfo.textContent = checker.estimateCrackTime();
}

// Event listeners
passwordInput.addEventListener('input', (e) => {
    updateUI(e.target.value);
});

// Toggle password visibility
togglePassword.addEventListener('click', () => {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;

    // Update icon
    const icon = togglePassword.querySelector('svg');
    if (type === 'text') {
        icon.innerHTML = `
            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
            <line x1="1" y1="1" x2="23" y2="23"></line>
        `;
    } else {
        icon.innerHTML = `
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
        `;
    }
});

// Clear security notice after 5 seconds
setTimeout(() => {
    const notice = document.querySelector('.security-notice');
    if (notice) {
        notice.style.opacity = '0.7';
    }
}, 10000);

// Initialize
updateUI('');
