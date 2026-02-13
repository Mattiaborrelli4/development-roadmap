# 🔐 Caesar Cipher Tool

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-yellow)](LICENSE)
[![Purpose](https://img.shields.io/badge/Purpose-Educational-green)]()

> **⚠️ AVVERTENZA IMPORTANTE:** Questo è uno strumento **EDUCATIVO** per apprendere la crittografia classica. Il cifrario di Caesar **NON è sicuro** per uso moderno e NON deve essere utilizzato per proteggere dati reali.

Un tool completo in Python per imparare il cifrario di Caesar, uno dei primi sistemi di crittografia della storia. Include cifratura, decifratura, brute force, analisi delle frequenze e supporto per file.

## 📚 Indice

- [Caratteristiche](#-caratteristiche)
- [Storia](#-storia-del-cifrario-di-caesar)
- [Come Funziona](#-come-funziona)
- [Installazione](#-installazione)
- [Utilizzo](#-utilizzo)
- [Perché NON è Sicuro](#-perché-non-è-sicuro)
- [Struttura del Progetto](#-struttura-del-progetto)

## ✨ Caratteristiche

- **🔒 Cifratura** - Cripta testo con chiave personalizzabile
- **🔑 Decifratura** - Decripta testo conoscendo la chiave
- **💥 Brute Force** - Prova tutte le chiavi possibili
- **📊 Analisi delle Frequenze** - Analisi statistica per crittanalisi
- **📁 Operazioni su File** - Cripta e decripta interi file
- **🌍 Alfabeti Multipli** - Supporta inglese, italiano, e custom
- **🎨 Visualizzazione** - Rappresentazione visiva del processo di cifratura
- **🖥️ CLI Ricca** - Interfaccia a riga di comando con output colorato

## 📖 Storia del Cifrario di Caesar

Il cifrario di Caesar è uno dei più antichi sistemi di crittografia conosciuti, prende il nome da **Gaio Giulio Cesare** (100-44 a.C.), che lo usava per comunicare con i suoi generali during le campagne militari.

### Svetonio, Vita dei Cesari (121 d.C.)

> "Existunt et ad Ciceronem, ad familiares, diversa epistolae stylo... si qua occultius perferenda erant, per notas scribat, id est sic structo litterarum ordine, ut nullum verbum effici posset: qui si qui investigare et persequi velit, quartam elementorum litteram, id est D pro A et persequitur aliis."

> *"Esistono lettere di Cesare a Cicerone e ai suoi familiari... se doveva trasmettere qualcosa in modo più occulto, lo scriveva in cifrate, cioè con un tale ordinamento delle lettere che nessuna parola potesse essere compresa: chi volesse indagare e seguirle, spostava la quarta lettera degli elementi, cioè D al posto di A e così via per le altre."*

Svetonio descrive che Cesare usava uno **shift di 3** (quarta lettera), sebbene altri storici romani menzionino l'uso di shift diversi.

## 🧮 Come Funziona

### Il Principio Matematico

Il cifrario di Caesar è un **cifrario a sostituzione monoalfabetica**. Ogni lettera del testo in chiaro viene sostituita da una lettera fissa di posizione inferiore nell'alfabeto.

#### Formule Matematiche

Per alfabeto di N lettere:

```
Cifratura:  C = (P + K) mod N
Decifratura: P = (C - K) mod N
```

Dove:
- **P** = carattere del plaintext (testo in chiaro)
- **C** = carattere del ciphertext (testo cifrato)
- **K** = chiave (shift/spostamento)
- **N** = lunghezza dell'alfabeto
- **mod** = operazione di modulo (resto della divisione)

#### Esempio Pratico

Chiave **K = 3**, Alfabeto **N = 26** (inglese):

```
A → D     (0 + 3 = 3)
B → E     (1 + 3 = 4)
C → F     (2 + 3 = 5)
...
X → A     (23 + 3 = 26; 26 mod 26 = 0)
Y → B     (24 + 3 = 27; 27 mod 26 = 1)
Z → C     (25 + 3 = 28; 28 mod 26 = 2)
```

Esempio completo:
```
Testo:  HELLO WORLD
Chiave: 3
Cifrato: KHOOR ZRUOG
```

### Aritmetica Modulare

L'operazione di modulo è fondamentale perché crea un sistema **ciclico**:

```
... X Y Z A B C ...
```

Dopo Z si torna a A, permettendo di cifrare qualsiasi testo con qualsiasi chiave.

## 🚀 Installazione

### Requisiti

- Python 3.10 o superiore
- pip (gestore pacchetti Python)

### Passi di Installazione

1. **Clona o scarica il repository:**
```bash
cd caesar-cipher-tool
```

2. **Installa le dipendenze:**
```bash
pip install -r requirements.txt
```

3. **Verifica l'installazione:**
```bash
python main.py --help
```

### Dipendenze

```txt
# requirements.txt
rich>=13.0.0  # Per output CLI colorato e formattato
```

**Nota:** Tutte le altre funzionalità usano solo la libreria standard di Python!

## 💻 Utilizzo

### Interfaccia a Riga di Comando

Il tool offre una CLI completa con sottocomandi:

#### 1. Cifratura (Encrypt)

```bash
# Cifra un testo con chiave 3
python main.py encrypt "HELLO WORLD" --key 3

# Output atteso:
# KHOOR ZRUOG

# Cifra con chiave personalizzata
python main.py encrypt "ATTACCO DELL'ALBA" --key 5 --alphabet italian

# Mostra rappresentazione visiva del processo
python main.py encrypt "CIAO" --key 3 --visual

# Salva su file
python main.py encrypt "MESSAGGIO SEGRETO" --key 7 --output cifrato.txt
```

#### 2. Decifratura (Decrypt)

```bash
# Decifra un testo conoscendo la chiave
python main.py decrypt "KHOOR ZRUOG" --key 3

# Output atteso:
# HELLO WORLD

# Decifra con alfabeto italiano
python main.py decrypt "FYYFHZT IQJSQFYF" --key 5 --alphabet italian
```

#### 3. Brute Force

```bash
# Prova tutte le 25 chiavi possibili
python main.py brute-force "KHOOR ZRUOG"

# Output: tabella con tutte le possibilità
# Chiave 1: JGNNQ YTQNF
# Chiave 2: IFMMP XSOME
# Chiave 3: HELLO WORLD  ← Testo in chiaro
# ...
```

#### 4. Analisi delle Frequenze

```bash
# Analizza un testo
python main.py analyze --text "KHOOR ZRUOG"

# Analizza un file
python main.py analyze --file cifrato.txt

# Trova automaticamente la chiave più probabile
python main.py analyze --file mistero.txt --find-key
```

#### 5. Operazioni su File

```bash
# Cripta un file
python main.py file-encrypt documento.txt --key 3 --output documento_criptato.txt

# Decripta un file
python main.py file-decrypt documento_criptato.txt --key 3 --output documento_decriptato.txt
```

#### 6. Informazioni

```bash
# Mostra storia e spiegazioni
python main.py info

# Lista alfabeti disponibili
python main.py alphabets
```

### Uso come Libreria Python

Puoi usare le funzioni nel tuo codice:

```python
from cipher import CaesarCipher, caesar_cipher
from analysis import FrequencyAnalyzer
from config import get_alphabet

# Uso semplice
cifrato = caesar_cipher("HELLO", key=3, encrypt=True)
print(cifrato)  # KHOOR

# Uso avanzato con classe
cipher = CaesarCipher(get_alphabet("english"))
cifrato = cipher.encrypt("ATTACK AT DAWN", key=5)
decifrato = cipher.decrypt(cifrato, key=5)

# Analisi delle frequenze
analyzer = FrequencyAnalyzer(language="english")
freq = analyzer.count_frequency(cifrato, get_alphabet("english"))
report = analyzer.get_frequency_report(cifrato, get_alphabet("english"))
print(report)
```

### Test

Esegui i test unitari:

```bash
python tests/test_cipher.py
```

Output previsto:
```
test_brute_force ... ok
test_calculate_percentage ... ok
test_chi_squared_test ... ok
test_count_frequency ... ok
...
----------------------------------------------------------------------
Ran 23 tests in 0.XXXs

OK
```

## ⚠️ Perché NON è Sicuro

Il cifrario di Caesar è **estremamente vulnerabile** per diversi motivi:

### 1. Spazio delle Chiavi Limitato

Per un alfabeto di 26 lettere esistono solo **25 chiavi significative** (la chiave 0 non cambia nulla, la chiave 26 è equivalente alla 0).

```python
# Tutte le chiavi possibili:
for key in range(1, 26):
    print(f"Chiave {key}: {decrypt(ciphertext, key)}")
```

Un attaccante può provare tutte le chiavi in **millisecondi**.

### 2. Analisi delle Frequenze

Ogni lingua ha **frequenze caratteristiche** delle lettere:

| Lettera | Italiano | Inglese |
|---------|----------|---------|
| E       | 11.79%   | 12.70%  |
| A       | 11.74%   | 8.17%   |
| I       | 11.28%   | 6.97%   |
| O       | 9.20%    | 7.51%   |
| Z       | 1.10%    | 0.07%   |

Il cifrario di Caesar **preserva** le frequenze:
- Se 'E' è la lettera più frequente nel testo in chiaro
- La lettera cifrata con shift 3 sarà 'H'
- Quindi 'H' sarà la lettera più frequente nel testo cifrato

Questo rende il cifrario vulnerabile all'**analisi statistica**.

### 3. Attacco a Testo Noto

Se un attaccante conosce anche **una sola parola** del testo originale (es. "SIGNATURE", "CONFIDENTIAL"), può:
1. Cifrare la parola nota con tutte le 25 chiavi
2. Confrontare con il testo cifrato
3. Identificare la chiave quando trova una corrispondenza

### 4. Indice di Coincidenza

L'**Indice di Coincidenza (IC)** misura quanto il testo assomiglia alla lingua attesa:

```
IC_italiano ≈ 0.0738
IC_inglese  ≈ 0.0667
IC_casuale  ≈ 0.0385
```

Il cifrario di Caesar **non cambia** l'IC, permettendo di identificare se un testo usa la stessa lingua del testo cifrato.

### Esempio di Attacco

```python
# Testo cifrato sconosciuto
ciphertext = "WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ"

# 1. Prova brute force (25 tentativi)
for key in range(1, 26):
    decrypted = decrypt(ciphertext, key)
    print(f"Key {key}: {decrypted}")

# 2. Analizza frequenze
analyzer = FrequencyAnalyzer(language="english")
best_key, score, plaintext = analyzer.find_best_key(ciphertext)

# 3. Identifica lingua con IC
ic = index_of_coincidence(ciphertext)
print(f"IC: {ic}")  # ~0.066 → Probabile inglese
```

### Storia di Attacchi

- **IX secolo d.C.**: Al-Kindi scopre l'analisi delle frequenze
- **Medioevo**: Gli studiosi arabi craccano regolarmente cifrari di substitution
- **Rinascimento**: Tutti i cifrari semplici considerati insicuri
- **Oggi**: Possibile craccare in mano (senza computer)

## 🔐 Alternative Moderne Sicure

Per proteggere dati reali, usa algoritmi moderni:

### Simmetrici (stessa chiave per cifrare/decifrare)

| Algoritmo | Chiave | Note |
|-----------|--------|------|
| **AES** | 128/192/256 bit | Standard governativo USA |
| **ChaCha20** | 256 bit | Veloce, mobile-friendly |
| **Twofish** | 128/256 bit | Alternativa ad AES |

### Asimmetrici (chiave pubblica/privata)

| Algoritmo | Chiave | Note |
|-----------|--------|------|
| **RSA** | 2048+ bit | Basato su fattorizzazione |
| **ECC** | 256+ bit | Basato su curve ellittiche |
| **Ed25519** | 256 bit | Firma digitale moderna |

### Librerie Python Sicure

```python
# AES con cryptography
from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
ciphertext = f.encrypt(b"messaggio")

# RSA con pycryptodome
from Crypto.PublicKey import RSA
key = RSA.generate(2048)
```

**⚠️ MAI implementare crittografia da zero per uso reale!**

## 📂 Struttura del Progetto

```
caesar-cipher-tool/
├── main.py              # CLI entry point con argparse
├── cipher.py            # Core CaesarCipher class
├── analysis.py          # FrequencyAnalyzer e statistiche
├── file_ops.py          # Operazioni di file I/O
├── config.py            # Configurazione alfabeti
├── requirements.txt     # Dipendenze
├── tests/
│   └── test_cipher.py   # Unit tests completi
├── README.md            # Questo file
└── .gitignore           # File da ignorare in git
```

### Moduli Principali

#### `cipher.py`
- `CaesarCipher`: Classe principale per cifratura/decifratura
- `caesar_cipher()`: Funzione helper per uso rapido
- Supporto alfabeti custom
- Rappresentazione visiva del processo

#### `analysis.py`
- `FrequencyAnalyzer`: Analisi delle frequenze
- `index_of_coincidence()`: Calcolo IC
- `entropy()`: Entropia di Shannon
- `chi_squared_test()`: Test statistico
- `find_best_key()`: Trova chiave più probabile

#### `file_ops.py`
- `CaesarFileHandler`: Gestione file
- `encrypt_file()`: Cifra file intero
- `decrypt_file()`: Decifra file intero
- `brute_force_file()`: Prova tutte le chiavi su file

#### `config.py`
- Alfabeti predefiniti (inglese, italiano)
- Funzioni helper per ottenere alfabeti
- Validazione chiavi

## 🎓 Scopo Educativo

Questo tool è progettato per:

✅ **Apprendere** i concetti base della crittografia
✅ **Capire** l'aritmetica modulare
✅ **Esplorare** l'analisi delle frequenze
✅ **Sperimentare** con la crittanalisi
✅ **Comprendere** perché i cifrari classici sono insicuri
✅ **Apprezzare** la crittografia moderna

## ❌ NON usare per:

❌ Proteggere password reali
❌ Cifrare documenti sensibili
❌ Comunicazioni private
❌ Dati personali o finanziari
❌ Qualsiasi cosa richieda sicurezza reale

## 📜 License

Questo progetto è creato **esclusivamente per scopi educativi**. È libero da usare per insegnare e apprendere, ma non per applicazioni di sicurezza reali.

## 🤝 Contributi

Contributi educativi benvenuti! Idee:
- Aggiungere altri alfabeti (spagnolo, francese, tedesco)
- Visualizzazioni grafiche (matplotlib)
- Altri cifrari classici (Vigenère, Playfair)
- Tutorial interattivi

## 📚 Risorse per Approfondire

### Libri
- "The Code Book" di Simon Singh
- "Cryptography Engineering" di Ferguson, Schneier, Kohno
- "Understanding Cryptography" di Paar, Pelzl

### Online
- [Khan Academy: Cryptography](https://www.khanacademy.org/computing/computer-science/cryptography)
- [Crypto Museum](https://www.cryptomuseum.com/)
- [Schneier on Security](https://www.schneier.com/)

---

**Creato per scopi educativi** 🎓 | **Python 3.10+** | **Ma non usarlo per cose serie!** 😅
