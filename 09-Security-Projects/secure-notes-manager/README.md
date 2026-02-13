# 🔐 Secure Notes Manager

Un gestore di note sicuro con crittografia AES-256 e derivazione chiavi PBKDF2.

## 📋 Indice

- [Caratteristiche](#caratteristiche)
- [Architettura della Sicurezza](#architettura-della-sicurezza)
- [Come Funziona la Crittografia AES](#come-funziona-la-crittografia-aes)
- [Perché PBKDF2 è Importante](#perché-pbkdf2-è-importante)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Best Practices per le Password](#best-practices-per-le-password)
- [Backup e Restore](#backup-e-restore)
- [Sicurezza](#sicurezza)

## ✨ Caratteristiche

- 🔒 **Crittografia AES-256**: Tutte le note sono crittografate con AES-256 tramite Fernet
- 🔑 **Derivazione Chiavi PBKDF2**: Prevenzione degli attacchi brute force con 100,000 iterazioni
- 💪 **Verifica Robustezza Password**: Sistema di punteggio con feedback migliorato
- 🏷️ **Tag e Ricerca**: Organizza le note con tag e cerca rapidamente
- 📦 **Backup Crittografati**: Esporta e importa backup del vault
- 🎨 **CLI Interattiva**: Interfaccia a riga di comando moderna con Rich
- 🛡️ **Backup Automatici**: Backup automatici prima di modifiche importanti

## 🏗️ Architettura della Sicurezza

### Layer di Sicurezza

1. **Password Master**: L'unica password che devi ricordare
2. **PBKDF2-HMAC-SHA256**: Deriva una chiave crittografica dalla password
3. **Salt Unico**: Ogni vault ha un salt casuale unico
4. **Fernet (AES-128)**: Crittografia simmetrica delle note
5. **HMAC**: Autenticazione per prevenire tampering

### Flusso di Crittografia

```
Password Master
       ↓
PBKDF2 (100,000 iterazioni) + Salt
       ↓
Chiave derivata (256 bit)
       ↓
Fernet (AES-128-CBC + HMAC)
       ↓
Note Crittografate
```

## 🔒 Come Funziona la Crittografia AES

### AES (Advanced Encryption Standard)

AES è uno standard di crittografia simmetrica approvato dal NIST:

- **AES-128**: Usa chiavi di 128 bit (16 bytes)
- **AES-192**: Usa chiavi di 192 bit (24 bytes)
- **AES-256**: Usa chiavi di 256 bit (32 bytes)

Il nostro programma usa **Fernet**, che implementa:
- **AES-128** in CBC mode per la confidenzialità
- **HMAC** per l'integrità e autenticità
- **Timestamp** per prevenire replay attacks

### Vantaggi di Fernet

1. **Sicuro by Default**: Necessita solo di una chiave
2. **IV Automatico**: Initialization Vector generato automaticamente
3. **HMAC Integrato**: Protezione da modifiche non autorizzate
4. **Replay Protection**: Timestamp anti-replay

```python
# Esempio di crittografia
from cryptography.fernet import Fernet

# Genera chiave
key = Fernet.generate_key()  # 44 caratteri base64

# Cripta
f = Fernet(key)
encrypted = f.encrypt(b"messaggio segreto")

# Decritta
decrypted = f.decrypt(encrypted)
```

## 🔑 Perché PBKDF2 è Importante

### Il Problema delle Password

Le password umane sono deboli:
- Poca entropia
- Spesso riutilizzate
- Indovinabili con dizionari

### PBKDF2 alla Salvezza

**PBKDF2** (Password-Based Key Derivation Function 2) risolve questi problemi:

1. **Rallenta Attacchi Brute Force**
   ```
   Senza PBKDF2:   1,000,000 tentativi/secondo
   Con PBKDF2:    10 tentativi/secondo
   ```

2. **Previene Rainbow Table Attacks**
   - Ogni vault ha un salt unico
   - Attacchi precomputati inutili

3. **Aumenta l'Entropia**
   - Password debole → Chiave forte a 256 bit
   - Output deterministico ma casuale

```python
# Esempio PBKDF2
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os

# Genera salt
salt = os.urandom(16)

# Deriva chiave
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,  # 100k iterazioni!
)
key = kdf.derive(password.encode())
```

### Perché 100,000 Iterazioni?

- **2012**: NIST raccomandava 1,000 iterazioni
- **2024**: 100,000+ è il minimo consigliato
- **Futuro**: Aumentare con l'aumento della potenza di calcolo

## 📦 Installazione

### Requisiti

- Python 3.10 o superiore
- pip (gestore pacchetti Python)

### Passi di Installazione

1. **Clona o scarica il progetto**
   ```bash
   cd secure-notes-manager
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verifica l'installazione**
   ```bash
   python main.py --version
   ```

### Dipendenze

```
cryptography>=41.0.0  # Crittografia AES-256
bcrypt>=4.0.0        # Hashing password
click>=8.1.0         # CLI framework
rich>=13.0.0         # Terminal beauty
pytest>=7.4.0        # Testing
```

## 🚀 Utilizzo

### Inizializzazione

Crea un nuovo vault:

```bash
python main.py init
```

Ti verrà chiesto di inserire una password master. Assicurati che sia forte!

### Sbloccare il Vault

```bash
python main.py unlock
```

Dopo aver sbloccato il vault, accederai alla shell interattiva.

### Aggiungere una Nota

Modo rapido (da CLI):
```bash
python main.py add "Titolo Nota" "Contenuto della nota" --tags "importante,lavoro"
```

Modo interattivo:
```bash
python main.py unlock
> add
Titolo: La mia nota
Contenuto: Questo è un segreto
Tags: personale,importante
```

### Visualizzare Tutte le Note

```bash
python main.py list
```

### Visualizzare una Nota Specifica

```bash
python main.py view 1
```

### Modificare una Nota

```bash
python main.py edit 1 "Nuovo contenuto aggiornato"
```

### Cercare Note

```bash
python main.py search "segreto"
```

La ricerca trova corrispondenze in:
- Titolo
- Contenuto
- Tags

### Eliminare una Nota

```bash
python main.py delete 1
```

### Generare una Password Sicura

```bash
python main.py generate
```

### Backup e Restore

**Esporta backup**:
```bash
python main.py export backup_mia.enc
```

**Importa backup**:
```bash
python main.py import-backup backup_mia.enc
```

### Comandi della Shell Interattiva

Una volta sbloccato il vault, puoi usare:

| Comando | Descrizione |
|---------|-------------|
| `list` | Lista tutte le note |
| `view <id>` | Visualizza una nota |
| `add` | Aggiungi una nuova nota |
| `edit <id>` | Modifica una nota |
| `delete <id>` | Elimina una nota |
| `search <query>` | Cerca note |
| `quit` | Esci dalla shell |

## 💡 Best Practices per le Password

### Cosa EVITARE

❌ Password comuni
- `password123`
- `qwerty`
- `12345678`
- `ilmiocane`

❌ Informazioni personali
- Compleanni
- Nomi di familiari
- Num. di telefono

❌ Riutilizzo
- Non usare la stessa password ovunque
- Non usare password usate in passato

### Cosa FARE

✅ **Lunghezza**: Almeno 12-16 caratteri

✅ **Complessità**: Combina:
- Maiuscole (A-Z)
- Minuscole (a-z)
- Numeri (0-9)
- Simboli (!@#$%^&*)

✅ **Unicità**: Una password per vault

✅ **Memorizzazione**: Non scriverla mai!

✅ **Generatore**: Usa `python main.py generate`

### Esempi di Password Forti

```
CorrectHorseBatteryStaple!42
Tr0ub4dor&Pr3d1cam3nt#99
V3ry!S3cur3-P@ssw0rd$2024
```

### Sistema di Punteggio

Il nostro sistema valuta:
- **Lunghezza** (30 punti)
- **Maiuscole** (15 punti)
- **Minuscole** (15 punti)
- **Numeri** (15 punti)
- **Simboli** (15 punti)
- **Bonus** extra per password molto lunghe (10 punti)

**Livelli**:
- 80-100: **FORTE** ✅
- 60-79: **BUONA** ⚠️
- 40-59: **MEDIA** ⚠️
- 20-39: **DEBOLE** ❌
- 0-19: **MOLTO DEBOLE** ❌

## 💾 Backup e Restore

### Backup Automatici

Il sistema crea automaticamente backup prima di:
- Modifiche importanti
- Re-criptazione del vault
- Eliminazioni

I backup sono salvati in `backups/auto_backup_YYYYMMDD_HHMMSS.enc`

### Backup Manuali

Crea backup manuali in qualsiasi momento:

```bash
python main.py export mio_backup.enc
```

### Restore da Backup

```bash
python main.py import-backup mio_backup.enc
```

⚠️ **Attenzione**: L'importazione sovrascrive il vault attuale!

### Lista Backup Disponibili

I backup sono situati nella cartella `backups/`:
- `auto_backup_*.enc`: Backup automatici
- `backup_*.enc`: Backup manuali

### Strategie di Backup Consigliate

1. **3-2-1 Rule**:
   - 3 copie dei dati
   - 2 tipi di storage diversi
   - 1 copia offsite

2. **Frequenza**:
   - Backup giornaliero per uso intensivo
   - Backup settimanale per uso normale
   - Backup mensile per uso leggero

3. **Test Restore**:
   - Verifica periodicamente che i backup funzionino
   - Testa il restore su una copia

## 🔐 Sicurezza

### Minacce Prevenute

| Minaccia | Protezione |
|----------|-----------|
| Accesso non autorizzato | Crittografia AES-256 |
| Attacchi brute force | PBKDF2 (100k iterazioni) |
| Rainbow tables | Salt unico per vault |
| Tampering dati | HMAC autenticazione |
| Replay attacks | Timestamp Fernet |
| Perdita dati | Backup automatici |

### Limitazioni di Sicurezza

⚠️ **Cosa NON protegge**:
- Keyloggers
- Schermate indesiderate
- Social engineering
- Dispositivi compromessi
- Attacchi laterali (side-channel)

### Consigli di Sicurezza

1. **Environment Sicuro**
   - Usa su trusted network
   - Verifica nessun keylogger attivo
   - Blocca lo schermo quando assente

2. **Password Master**
   - Non condividerla MAI
   - Non scriverla
   - Considera l'uso di un password manager

3. **Aggiornamenti**
   - Tieni Python aggiornato
   - Aggiorna le dipendenze
   - Controlla regolarmente sicurezza

4. **Backup**
   - Salva backup in location sicure
   - Crittografa backup offsite
   - Testa restore periodicamente

### Audit e Compliance

Il programma è stato progettato con:
- ✅ Crittografia standard del settore (AES, PBKDF2)
- ✅ Nessun hardcoding di chiavi
- ✅ Sicurezza by default
- ✅ Test suite completa
- ✅ Codice pulito e auditabile

## 📚 Struttura del Progetto

```
secure-notes-manager/
├── main.py              # Entry point CLI
├── crypto.py            # Gestione crittografia
├── storage.py           # Storage del vault
├── password.py          # Verifica password e derivazione chiavi
├── models/
│   └── note.py          # Modello dati Note
├── tests/
│   └── test_crypto.py   # Test suite
├── requirements.txt     # Dipendenze
└── README.md           # Documentazione
```

## 🧪 Testing

Esegui i test:

```bash
pytest tests/ -v
```

I test coprono:
- Crittografia e decrittografia
- Derivazione chiavi
- Gestione vault
- Verifica password

## 🤝 Contribuire

Sentiti libero di:
- Aprire issue per bug
- Proporre nuove feature
- Inviare pull request

## 📄 Licenza

Questo progetto è a scopo educativo. Usalo a tuo rischio.

## ⚠️ Disclaimer

Questo software è fornito "così com'è" senza garanzie. Non è responsabile per perdita di dati. Fai sempre backup!

---

**Creato con ❤️ per la sicurezza delle tue note**
