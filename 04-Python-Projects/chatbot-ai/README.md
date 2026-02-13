# Chatbot AI - Progetto Educativo Python

## Descrizione del Progetto

Un chatbot educativo semplice scritto in Python che utilizza **pattern matching**, espressioni regolari e un sistema di apprendimento base. Progettato specificamente per studenti universitari principianti che vogliono imparare concetti fondamentali di NLP (Natural Language Processing) e programmazione Python.

## Caratteristiche Principali

- **Pattern Matching**: Utilizza espressioni regolari per riconoscere gli intenti dell'utente
- **Confidenza Scoring**: Calcola quanto bene un pattern corrisponde all'input
- **Contesto Conversazionale**: Ricorda gli ultimi 3 messaggi per coerenza
- **Modalità Apprendimento**: Impara nuovi pattern durante la conversazione
- **Risposte di Fallback**: Gestisce input non riconosciuti in modo intelligente
- **Persistenza Dati**: Salva i pattern appresi tra le sessioni
- **Statistiche**: Traccia le metriche della conversazione
- **Multi-tema**: Supporta vari argomenti (meteo, notizie, barzellette, aiuto)

## Requisiti

### Software Necessario
- Python 3.7 o superiore
- Un editor di testo (VS Code, PyCharm, o qualsiasi altro)

### Librerie Python
```bash
# Nessuna libreria esterna richiesta!
# Utilizza solo la libreria standard Python:
# - json
# - random
# - re (espressioni regolari)
# - os
# - datetime
# - typing
```

## Struttura del Progetto

```
chatbot-ai/
│
├── chatbot.py              # Codice principale del chatbot
├── training_data.json      # Dati di training iniziali (generato automaticamente)
├── learned_data.json       # Pattern appresi (creato durante l'uso)
└── README.md               # Questo file
```

## Come Utilizzare

### 1. Avviare il Chatbot

Apri il terminale o prompt dei comandi e naviga nella cartella del progetto:

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\chatbot-ai"
```

Esegui il programma:

```bash
python chatbot.py
```

### 2. Comandi Disponibili

Durante la conversazione, puoi utilizzare questi comandi speciali:

- **`aiuto`** - Mostra i comandi disponibili e gli argomenti conosciuti
- **`impara`** - Entra in modalità apprendimento per insegnare nuovi pattern
- **`statistiche`** - Mostra le statistiche della conversazione corrente
- **`esci`** - Termina la conversazione

### 3. Esempio di Conversazione

```
Chatbot: Ciao! Sono il tuo assistente virtuale. Come posso aiutarti?

Tu: ciao come stai
Chatbot: Ciao! Come posso aiutarti oggi?

Tu: raccontami una barzelletta
Chatbot: Perché i programmatori preferiscono il mode scuro?
         Perché la luce attira i bug!

Tu: che tempo fa
Chatbot: Non posso controllare il meteo reale, ma spero sia bello!

Tu: impara
[Entri in modalità apprendimento]
```

## Concetti Tecnici

### 1. Pattern Matching con Regex

Il chatbot utilizza espressioni regolari per riconoscere gli intenti:

```python
# Esempio di pattern per saluti
r"\b(ciao|salve|hey|buongiorno)\b.*"
```

- `\b` = confine della parola (word boundary)
- `(...)` = gruppo di opzioni
- `|` = OR logico
- `.*` = qualsiasi carattere (zero o più volte)

### 2. Calcolo della Confidenza

Il sistema calcola quanto bene un pattern corrisponde:

```python
def calculate_confidence(self, pattern: str, user_input: str) -> float:
    # Match completo = +0.3 punti
    # Lunghezza match = fino a +0.2 punti
    # Parole chiave multiple = +0.1 punti
    # Massimo: 1.0 (100%)
```

### 3. Estrazione Entità

Identifica parole chiave rimuovendo le "stopword" (parole comuni):

```python
stopword = {"il", "la", "di", "a", "con", ...}
entities = [word for word in words if word not in stopword]
```

### 4. Gestione del Contesto

Mantiene gli ultimi 3 messaggi per coerenza conversazionale:

```python
def update_context(self, message: str) -> None:
    self.context.append(message)
    if len(self.context) > 3:
        self.context = self.context[-3:]
```

## Architettura del Codice

### Classe Principale: `Chatbot`

#### Metodi Chiave

| Metodo | Descrizione |
|--------|-------------|
| `__init__()` | Inizializza il chatbot e carica i dati |
| `load_training_data()` | Carica gli intenti dal JSON |
| `get_response()` | Trova la risposta migliore per l'input |
| `calculate_confidence()` | Calcola il punteggio di matching |
| `extract_entities()` | Estrae parole chiave dall'input |
| `update_context()` | Aggiorna la storia della conversazione |
| `learn_mode()` | Permette di insegnare nuovi pattern |
| `save_learning()` | Salva i pattern appresi |
| `main()` | Loop principale della conversazione |

### Struttura dei Dati

#### Training Data (training_data.json)
```json
{
  "nome_intent": {
    "patterns": ["regex1", "regex2"],
    "responses": ["risposta1", "risposta2"]
  }
}
```

## Funzionalità Educational

### Cosa Imparerai

1. **Programmazione a Oggetti**: Classi e metodi
2. **Espressioni Regolari**: Pattern matching in Python
3. **Gestione File JSON**: Lettura e scrittura di dati
4. **NLP Base**: Tokenizzazione e estrazione entità
5. **Sistema di Scoring**: Algoritmi di confidenza
6. **Gestione Contesto**: Memoria conversazionale
7. **Error Handling**: Gestione eccezioni robusta
8. **Type Hinting**: Annotazioni di tipo Python

## Personalizzazione

### Aggiungere Nuovi Intenti

Modifica `training_data.json` o usa la modalità `impara` durante la conversazione:

```json
{
  "nuovo_intent": {
    "patterns": ["\\b(parola1|parola2)\\b.*"],
    "responses": ["Risposta 1", "Risposta 2"]
  }
}
```

### Modificare Stopword

Modifica la lista `stopword` nel metodo `extract_entities()`:

```python
stopword = {"il", "la", "tu", "mio", ...}
```

## Troubleshooting

### Problema: Il chatbot non risponde correttamente

**Soluzione**: Controlla che `training_data.json` esista. Verrà creato automaticamente alla prima esecuzione.

### Problema: Errori di codifica caratteri

**Soluzione**: Assicurati che il file sia salvato in UTF-8. Il codice utilizza `encoding='utf-8'` per la lettura/scrittura.

### Problema: Pattern non riconosciuti

**Soluzione**: Usa la modalità `impara` per insegnare nuovi pattern. Più pattern aggiungi, più intelligente diventa il chatbot!

## Estensioni Possibili

Idee per migliorare il progetto:

1. **Integrazione API**: Collegare a vere API meteo/notizie
2. **Machine Learning**: Usare NLTK o spaCy per NLP avanzato
3. **Database**: Salvare conversazioni in SQLite
4. **Interfaccia Grafica**: Aggiungere GUI con Tkinter
5. **Multi-lingua**: Supportare più lingue
6. **Sentiment Analysis**: Riconoscere emozioni dell'utente
7. **Voice Input**: Integrare riconoscimento vocale

## Note Educative

### Perché Questo Progetto?

Questo chatbot dimostra concetti fondamentali di AI/NLP senza complessità eccessive:

- **No AI esterne**: Tutta la logica è in Python puro
- **Comprensibile**: Codice ben commentato per studenti
- **Estendibile**: Facile da modificare e migliorare
- **Pedagogico**: Ogni funzione ha uno scopo educativo

### Limitazioni Intentional

Il chatbot NON:

- Usa API esterne (OpenAI, Google, etc.)
- Ha vero machine learning
- Capisce linguaggio naturale complesso
- Ha memoria a lungo termine

Queste limitazioni sono **intentional** per mantenere il progetto accessibile ai principianti!

## Risorse per Studio

### Concetti Chiave da Approfondire

1. **Regex**: https://docs.python.org/3/library/re.html
2. **JSON**: https://docs.python.org/3/library/json.html
3. **OOP**: https://docs.python.org/3/tutorial/classes.html
4. **Type Hints**: https://docs.python.org/3/library/typing.html

## Licenza

Questo è un progetto educativo. Sentiti libero di usarlo, modificarlo e condividerlo per scopi didattici.

## Autore

Progetto creato per scopi educativi.
Target: Studenti universitari principianti
Linguaggio: Python 3.x

---

**Buon divertimento con il tuo Chatbot AI! 🤖**
