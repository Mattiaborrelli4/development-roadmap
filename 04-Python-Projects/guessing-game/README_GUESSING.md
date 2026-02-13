# 🎮 Gioco "Indovina il Numero" - Guida Completa

<div align="center">

**Un progetto Python perfetto per iniziare a programmare!**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Livello](https://img.shields.io/badge/Livello-Principiante-green.svg)](#)
[![Tempo](https://img.shields.io/badge/Tempo-30--60_min-yellow.svg)](#)

</div>

---

## 📚 Indice

- [Introduzione](#introduzione)
- [Obiettivi di Apprendimento](#obiettivi-di-apprendimento)
- [Prerequisiti](#prerequisiti)
- [Come Giocare](#come-giocare)
- [Spiegazione del Codice](#spiegazione-del-codice)
- [Concetti Python Utilizzati](#concetti-python-utilizzati)
- [Esercizi Proposti](#esercizi-proposti)
- [FAQ - Domande Frequenti](#faq---domande-frequenti)

---

## 🌟 Introduzione

Benvenuto al tuo primo progetto Python! Questo è il **Gioco "Indovina il Numero"**, un classico della programmazione che ti aiuterà a comprendere i concetti fondamentali della programmazione in modo divertente e interattivo.

### 🎯 Cos'è questo gioco?

Il computer pensa a un numero casuale tra **1 e 100** e il tuo obiettivo è **indovinarlo** nel minor numero di tentativi possibili! Il gioco ti darà dei suggerimenti se il tuo tentativo è **più alto** o **più basso** del numero segreto.

### ✨ Perché questo progetto?

Questo è il progetto **perfetto per iniziare** perché:
- 🎓 Ti insegna i concetti base senza usare classi
- 🎯 È immediatamente gratificante
- 🔧 Puoi facilmente estenderlo e personalizzarlo
- 📊 Introduce concetti importanti come input/output, cicli e funzioni

---

## 🎓 Obiettivi di Apprendimento

Completando questo progetto, imparerai:

| Concetto | Descrizione |
|----------|-------------|
| 🔢 **Input/Output** | Come interagire con l'utente tramite `input()` e `print()` |
| 🎲 **Modulo Random** | Come generare numeri casuali |
| ➰ **Ciclo While** | Come ripetere azioni finché una condizione è vera |
| 🔀 **Condizionali** | Come prendere decisioni con `if`, `elif`, `else` |
| 📦 **Funzioni** | Come organizzare il codice in blocchi riutilizzabili |
| 🎣 **Gestione Errori** | Come gestire input non validi con `try/except` |
| 📈 **Variabili e Tipi** | Come lavorare con interi, stringhe e booleani |

---

## 📋 Prerequisiti

Prima di iniziare, assicurati di avere:

### ✅ Software Necessario
- **Python 3.x** installato sul tuo computer
  - Per verificare: apri il terminale e digita `python --version`
- Un **editor di codice** (consigliati):
  - [VS Code](https://code.visualstudio.com/) 🌟 Raccomandato
  - [PyCharm Community](https://www.jetbrains.com/pycharm/)
  - [Thonny](https://thonny.org/) (perfetto per principianti)
  - Oppure anche un semplice editor di testo

### 🧠 Conoscenze Base
Nessuna esperienza di programmazione richiesta! Questo progetto è pensato per chi:
- Sta scrivendo il suo primo programma Python
- Conosce le basi teoriche ma non ha mai fatto pratica
- Vuole consolidare i concetti fondamentali

---

## 🎮 Come Giocare

### 🚀 Avviare il Gioco

1. **Apri il terminale** o il prompt dei comandi
2. **Naviga** nella cartella del progetto:
   ```bash
   cd C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\guessing-game
   ```
3. **Lancia** il gioco con:
   ```bash
   python number_guess.py
   ```
   oppure:
   ```bash
   python3 number_guess.py
   ```

### 📖 Regole del Gioco

1. 🎲 Il computer genera un numero casuale tra **1 e 100**
2. ⚡ **Scegli la difficoltà**:
   - **Facile (F)** - 15 tentativi
   - **Medio (M)** - 10 tentativi
   - **Difficile (D)** - 5 tentativi
3. 💭 Dopo ogni tentativo, il gioco ti dirà se:
   - ✅ **Hai indovinato!** → Hai vinto!
   - 📈 **Troppo basso** → Il numero segreto è più alto
   - 📉 **Troppo alto** → Il numero segreto è più basso
4. 🔄 Alla fine puoi decidere se giocare ancora

### 🎯 Esempio di Partita Completa

Ecco come appare una tipica partita:

```
============================================================
   BENVENUTO AL GIOCO 'INDOVINA IL NUMERO'!
============================================================

Il computer ha scelto un numero casuale tra 1 e 100.
Il tuo obiettivo è indovinarlo nel minor numero di tentativi.
Dopo ogni tentativo, ti verrà detto se il numero è più alto o più basso.

Livelli di difficoltà disponibili:
  [F] Facile   - 15 tentativi
  [M] Medio   - 10 tentativi
  [D] Difficile - 5 tentativi

------------------------------------------------------------

Scegli la difficoltà (F/M/D): M

Hai scelto: MEDIO - Hai 10 tentativi disponibili.


Tentativi rimasti: 10
Inserisci un numero tra 1 e 100: 50

📉 Il numero 50 è troppo ALTO.
💡 Suggerimento: Prova con un numero più basso!
----------------------------------------

Tentativi rimasti: 9
Inserisci un numero tra 1 e 100: 25

📈 Il numero 25 è troppo BASSO.
💡 Suggerimento: Prova con un numero più alto!
----------------------------------------

Tentativi rimasti: 8
Inserisci un numero tra 1 e 100: 37

📈 Il numero 37 è troppo BASSO.
💡 Suggerimento: Prova con un numero più alto!
----------------------------------------

Tentativi rimasti: 7
Inserisci un numero tra 1 e 100: 43

🎉 CONGRATULAZIONI! Hai indovinato il numero 43!
----------------------------------------

============================================================
🏆 RISULTATO: VITTORIA!
Ottimo lavoro! Hai dimostrato buone capacità deduttive.
Livello completato: Medio ⭐⭐
============================================================

Vuoi giocare ancora? (S/N): n

Grazie per aver giocato! Arrivederci! 👋

============================================================
   Fine del gioco - Speriamo ti sia piaciuto!
============================================================
```

---

## 💻 Spiegazione del Codice

Analizziamo il codice funzione per funzione. Non preoccuparti se qualcosa non è chiaro subito - la programmazione si impara con la pratica!

Il tuo codice è ben organizzato in **10 funzioni**, ognuna con un compito specifico. Questo è un ottimo esempio di **programmazione modulare**!

### 📋 Struttura delle Funzioni

```
number_guess.py
├── mostra_intestazione()        → Mostra il benvenuto
├── scegli_difficolta()          → Seleziona la difficoltà
├── genera_numero_segreto()       → Crea il numero da indovinare
├── ottieni_tentativo()           → Legge e valida l'input
├── controlla_tentativo()         → Confronta tentativo con segreto
├── mostra_feedback()             → Stampa i suggerimenti
├── gioca()                       → Gestisce una partita
├── mostra_risultato_finale()     → Mostra vittoria/sconfitta
├── vuoi_giocare_ancora()         → Chiede se rigiocare
└── main()                        → Controller principale
```

---

### 🎨 Funzione `mostra_intestazione()`

```python
def mostra_intestazione():
    """Mostra il titolo del gioco e il benvenuto."""
    print("=" * 60)
    print("   BENVENUTO AL GIOCO 'INDOVINA IL NUMERO'!")
    print("=" * 60)
    # ... resto del codice ...
```

**Cosa fa:**
- Stampa la schermata di benvenuto
- Spiega le regole del gioco
- Mostra i livelli di difficoltà disponibili

**Concetti chiave:**
- **`"=" * 60`**: Ripete il carattere "=" 60 volte per creare una linea
- **Docstring**: La stringa tra tripla virgoletta spiega cosa fa la funzione
- **Nessun return**: La funzione solo stampa, non restituisce valori

---

### ⚡ Funzione `scegli_difficolta()`

```python
def scegli_difficolta():
    """Permette all'utente di scegliere il livello di difficoltà."""
    while True:
        scelta = input("Scegli la difficoltà (F/M/D): ").strip().upper()

        if scelta == "F":
            tentativi = 15
            print(f"\nHai scelto: FACILE - Hai {tentativi} tentativi disponibili.\n")
            return tentativi
        elif scelta == "M":
            # ...
        elif scelta == "D":
            # ...
        else:
            print("\n❌ Scelta non valida! Inserisci F, M, o D.")
```

**Cosa fa:**
- Chiede all'utente di scegliere la difficoltà
- Valida l'input (accetta F/M/D in maiuscolo o minuscolo)
- Restituisce il numero di tentativi consentiti

**Concetti chiave:**

| Metodo | Spiegazione | Esempio |
|--------|-------------|---------|
| **`.strip()`** | Rimuove spazi all'inizio e alla fine | `" M "` → `"M"` |
| **`.upper()`** | Converte in maiuscolo | `"m"` → `"M"` |
| **`while True`** | Loop finché non usciamo con `return` | Continua a chiedere |
| **`f"{variabile}"`** | f-string per formattare stringhe | `f"Hai {tentativi} tentativi"` |

**Perché `.strip().upper()`?**
Per rendere l'input più flessibile! L'utente può scrivere:
- `"f"` → diventa `"F"` ✓
- `"M "` → diventa `"M"` ✓
- `"  d  "` → diventa `"D"` ✓

---

### 🎲 Funzione `genera_numero_segreto()`

```python
def genera_numero_segreto():
    """Genera e restituisce un numero casuale compreso tra 1 e 100."""
    numero_segreto = random.randint(1, 100)
    return numero_segreto
```

**Cosa fa:**
- Genera un numero intero casuale tra 1 e 100 (entrambi inclusi)
- Lo restituisce al chiamante

**Concetti chiave:**
- **`random.randint(a, b)`**: Genera un intero casuale tra `a` e `b` (inclusi)
- **`return`**: Invia il valore indietro a chi ha chiamato la funzione

**Esempio:**
```python
>>> numero = genera_numero_segreto()
>>> print(numero)
42  # Ogni volta sarà diverso!
```

---

### 🎯 Funzione `ottieni_tentativo()`

```python
def ottieni_tentativo(tentativi_rimasti):
    """Chiede all'utente di inserire un numero e valida l'input."""
    while True:
        print(f"\nTentativi rimasti: {tentativi_rimasti}")
        input_utente = input("Inserisci un numero tra 1 e 100: ").strip()

        try:
            numero = int(input_utente)

            if numero < 1 or numero > 100:
                print("❌ Il numero deve essere tra 1 e 100! Riprova.")
            else:
                return numero

        except ValueError:
            print("❌ Input non valido! Inserisci solo numeri interi.")
```

**Cosa fa:**
- Mostra quanti tentativi rimangono
- Chiede all'utente di inserire un numero
- **Valida** l'input per assicurarsi che sia:
  - Un numero valido (non lettere)
  - Compreso tra 1 e 100
- Continua a chiedere finché l'utente non inserisce un valore valido

**Concetti chiave:**

| Concetto | Spiegazione |
|----------|-------------|
| **`while True`** | Loop infinito che continua finché non usciamo con `return` |
| **`input()`** | Legge quello che l'utente scrive come **stringa** |
| **`.strip()`** | Rimuove spazi superflui |
| **`int()`** | Converte la stringa in un numero intero |
| **`try/except`** | Gestione degli errori - se l'utente inserisce "abc" |
| **`ValueError`** | Eccezione che si solleva quando non possiamo convertire in numero |

**Perché il `while True`?**
Se l'utente inserisce qualcosa di non valido (es. "abc" o "150"), non vogliamo che il programma si blocchi. Vogliamo dargli un'altra possibilità!

---

### 🧮 Funzione `controlla_tentativo()`

```python
def controlla_tentativo(tentativo, numero_segreto):
    """Confronta il tentativo dell'utente con il numero segreto."""
    if tentativo == numero_segreto:
        return "corretto"
    elif tentativo < numero_segreto:
        return "basso"
    else:
        return "alto"
```

**Cosa fa:**
- Confronta il tentativo dell'utente con il numero segreto
- Restituisce una stringa che indica se il tentativo è corretto, troppo basso o troppo alto

**Concetti chiave:**

| Concetto | Spiegazione |
|----------|-------------|
| **`if`** | Controlla se la condizione è vera |
| **`elif`** | "Altrimenti se" - controlla un'altra condizione se la prima è falsa |
| **`else`** | "Altrimenti" - esegue se tutte le condizioni precedenti sono false |
| **Operatori di confronto** | `==` (uguale), `<` (minore), `>` (maggiore) |

**Logica del flusso:**
```
tentativo == numero_segreto?  → Sì → "corretto"
            ↓ No
tentativo < numero_segreto?   → Sì → "basso"
            ↓ No
                             → "alto"
```

---

### 💬 Funzione `mostra_feedback()`

```python
def mostra_feedback(risultato, tentativo):
    """Stampa un messaggio appropriato in base al risultato."""
    if risultato == "corretto":
        print(f"\n🎉 CONGRATULAZIONI! Hai indovinato il numero {tentativo}!")
    elif risultato == "basso":
        print(f"\n📈 Il numero {tentativo} è troppo BASSO.")
        print("💡 Suggerimento: Prova con un numero più alto!")
    else:  # risultato == "alto"
        print(f"\n📉 Il numero {tentativo} è troppo ALTO.")
        print("💡 Suggerimento: Prova con un numero più basso!")
```

**Cosa fa:**
- Stampa un messaggio di feedback appropriato
- Dà suggerimenti se il tentativo è sbagliato

**Concetto chiave:**
- **Separazione dei compiti**: La funzione `controlla_tentativo()` decide solo SE è corretto, mentre `mostra_feedback()` decide COMUNICARLO all'utente

---

### 🎮 Funzione `gioca()`

Questa è la **funzione principale** che gestisce una partita completa. È il cuore del gioco!

```python
def gioca(tentativi_massimi):
    """Esegue una singola partita del gioco."""
    numero_segreto = genera_numero_segreto()
    tentativo_corrente = 0

    while tentativo_corrente < tentativi_massimi:
        tentativi_rimasti = tentativi_massimi - tentativo_corrente
        tentativo = ottieni_tentativo(tentativi_rimasti)
        risultato = controlla_tentativo(tentativo, numero_segreto)
        mostra_feedback(risultato, tentativo)

        tentativo_corrente += 1

        if risultato == "corretto":
            return True

    # Se arriviamo qui, i tentativi sono finiti
    print(f"\n😢 HAI PERSO!")
    print(f"Il numero segreto era: {numero_segreto}")
    return False
```

**Cosa fa:**
- Genera il numero segreto
- Loop principale: chiede tentativi finché non indovina o finiscono i tentativi
- Mostra il feedback appropriato
- Restituisce `True` se vinto, `False` se perso

**Concetti chiave:**

| Concetto | Spiegazione |
|----------|-------------|
| **`tentativo_corrente += 1`** | Incrementa il contatore (equivale a `tentativo_corrente = tentativo_corrente + 1`) |
| **`return True`** | Esce immediatamente dalla funzione e restituisce True |
| **`return False`** | Viene eseguito solo se il loop finisce senza vincere |

---

### 🏆 Funzione `mostra_risultato_finale()`

```python
def mostra_risultato_finale(vittoria, tentativi_massimi):
    """Mostra un messaggio finale basato sul risultato."""
    if vittoria:
        print("🏆 RISULTATO: VITTORIA!")
        if tentativi_massimi == 15:
            print("Livello completato: Facile ⭐")
        elif tentativi_massimi == 10:
            print("Livello completato: Medio ⭐⭐")
        else:  # 5 tentativi
            print("Livello completato: Difficile ⭐⭐⭐")
    else:
        print("💔 RISULTATO: SCONFITTA")
```

**Cosa fa:**
- Mostra un messaggio finale diverso in base al risultato
- Assegna stelle in base alla difficoltà superata

---

### 🔄 Funzione `vuoi_giocare_ancora()`

```python
def vuoi_giocare_ancora():
    """Chiede all'utente se vuole giocare un'altra partita."""
    while True:
        risposta = input("Vuoi giocare ancora? (S/N): ").strip().upper()

        if risposta == "S":
            return True
        elif risposta == "N":
            print("\nGrazie per aver giocato! Arrivederci! 👋")
            return False
        else:
            print("❌ Scelta non valida! Inserisci S (Sì) o N (No).")
```

**Cosa fa:**
- Chiede all'utente se vuole giocare ancora
- Accetta S/N (maiuscolo o minuscolo grazie a `.upper()`)
- Continua a chiedere se l'input non è valido

**Concetti chiave:**

| Metodo | Spiegazione | Esempio |
|--------|-------------|---------|
| **`.strip()`** | Rimuove spazi all'inizio e alla fine | `" S "` → `"S"` |
| **`.upper()`** | Converte in maiuscolo | `"s"` → `"S"` |

---

### 🏁 Funzione `main()`

```python
def main():
    """Funzione principale del programma."""
    mostra_intestazione()

    while True:
        # Fase 1: Scegliamo la difficoltà
        tentativi_massimi = scegli_difficolta()

        # Fase 2: Giociamo la partita
        vittoria = gioca(tentativi_massimi)

        # Fase 3: Mostriamo il risultato finale
        mostra_risultato_finale(vittoria, tentativi_massimi)

        # Fase 4: Chiediamo se vuole giocare ancora
        if not vuoi_giocare_ancora():
            break

    # Messaggio di uscita finale
    print("\n" + "=" * 60)
    print("   Fine del gioco - Speriamo ti sia piaciuto!")
    print("=" * 60)
```

**Cosa fa:**
- È il **"cervello"** del programma
- Gestisce il flusso principale: intestazione → difficoltà → gioco → risultato → rigiocare?
- Usa un loop per permettere più partite consecutive

**Concetti chiave:**

| Concetto | Spiegazione |
|----------|-------------|
| **`if not vuoi_giocare_ancora():`** | Se la funzione restituisce False, esci dal loop |
| **`break`** | Esce immediatamente dal loop `while` |

---

### ▶️ Blocco `if __name__ == "__main__":`

```python
if __name__ == "__main__":
    main()
```

**Cosa fa:**
- È lo **standard Python** per avviare un programma
- Esegue la funzione `main()` solo quando il file viene eseguito direttamente
- Permette di importare le funzioni da questo file in altri programmi senza eseguirlo automaticamente

**Perché usarlo?**
```python
# Se importiamo questo file:
import number_guess
# Il codice qui sotto NON viene eseguito

# Se eseguiamo direttamente:
python number_guess.py
# Il codice qui sotto VIENE eseguito
```

**Concetti chiave:**

| Concetto | Spiegazione |
|----------|-------------|
| **`break`** | Esce immediatamente dal loop |
| **`not`** | Negazione logica → `not True` = `False` |
| **`:.1f`** | Formatta il numero con 1 cifra decimale |

---

### ▶️ Blocco `if __name__ == "__main__":`

```python
if __name__ == "__main__":
    main()
```

**Cosa fa:**
- È lo **standard Python** per avviare un programma
- Esegue la funzione `main()` solo quando il file viene eseguito direttamente
- Permette di importare le funzioni da questo file in altri programmi senza eseguirlo automaticamente

**Perché usarlo?**
```python
# Se importiamo questo file:
import number_guess
# Il codice qui sotto NON viene eseguito

# Se eseguiamo direttamente:
python number_guess.py
# Il codice qui sotto VIENE eseguito
```

---

## 🐍 Concetti Python Utilizzati

### 1. 📦 Modulo `random`

Il modulo `random` è parte della **libreria standard** di Python e fornisce funzioni per generare numeri casuali.

#### **Metodi principali:**

| Metodo | Descrizione | Esempio |
|--------|-------------|---------|
| `random.randint(a, b)` | Intero casuale tra a e b (inclusi) | `random.randint(1, 100)` → 42 |
| `random.random()` | Float casuale tra 0.0 e 1.0 | `random.random()` → 0.7372 |
| `random.choice(lista)` | Elemento casuale da una lista | `random.choice(['a', 'b'])` → 'b' |

#### **Nel nostro gioco:**
```python
import random

numero = random.randint(1, 100)
# Genera un numero intero tra 1 e 100 (entrambi inclusi)
# Possibili risultati: 1, 2, 3, ..., 98, 99, 100
```

---

### 2. ➰ Ciclo `while`

Il ciclo `while` ripete un blocco di codice **finché una condizione è vera**.

#### **Sintassi:**
```python
while condizione:
    # codice da ripetere
```

#### **Esempi:**

```python
# Esempio 1: Contare
count = 0
while count < 5:
    print(count)
    count += 1
# Output: 0, 1, 2, 3, 4

# Esempio 2: Loop infinito con break
while True:
    risposta = input("Scrivi 'quit' per uscire: ")
    if risposta == 'quit':
        break

# Esempio 3: Input valido
while True:
    try:
        numero = int(input("Inserisci un numero: "))
        break  # Esce solo se l'input è valido
    except ValueError:
        print("Non valido! Riprova.")
```

#### **Nel nostro gioco:**
```python
while tentativi < massimi_tentativi:
    # Gioca finché ci sono tentativi disponibili
    # ...
```

---

### 3. 🔀 Condizionali `if`, `elif`, `else`

I condizionali permettono al programma di **prendere decisioni** basate su condizioni.

#### **Sintassi:**
```python
if condizione1:
    # esegue se condizione1 è vera
elif condizione2:
    # esegue se condizione1 è falsa E condizione2 è vera
else:
    # esegue se tutte le condizioni precedenti sono false
```

#### **Operatori di confronto:**

| Operatore | Significato | Esempio |
|-----------|-------------|---------|
| `==` | Uguale | `5 == 5` → True |
| `!=` | Diverso | `5 != 3` → True |
| `<` | Minore | `3 < 5` → True |
| `>` | Maggiore | `5 > 3` → True |
| `<=` | Minore o uguale | `3 <= 3` → True |
| `>=` | Maggiore o uguale | `5 >= 5` → True |

#### **Operatori logici:**

| Operatore | Significato | Esempio |
|-----------|-------------|---------|
| `and` | Entrambe vere | `True and True` → True |
| `or` | Almeno una vera | `True or False` → True |
| `not` | Negazione | `not True` → False |

#### **Nel nostro gioco:**
```python
if tentativo == numero_segreto:
    return "corretto"
elif tentativo < numero_segreto:
    return "basso"
else:
    return "alto"
```

---

### 4. 📦 Funzioni

Le funzioni sono **blocchi di codice riutilizzabili** che eseguono un compito specifico.

#### **Sintassi:**
```python
def nome_funzione(parametro1, parametro2):
    """Docstring: descrive cosa fa la funzione."""
    # codice della funzione
    return risultato  # opzionale
```

#### **Componenti:**

| Componente | Descrizione |
|------------|-------------|
| **`def`** | Parola chiave per definire una funzione |
| **Nome** | Identificatore della funzione (snake_case) |
| **Parametri** | Input della funzione (opzionali) |
| **Docstring** | Documentazione (raccomandata!) |
| **`return`** | Valore restituito (opzionale) |

#### **Esempi:**

```python
# Funzione senza parametri e senza return
def saluta():
    print("Ciao!")

# Funzione con parametro e senza return
def saluta_nome(nome):
    print(f"Ciao, {nome}!")

# Funzione con parametri e return
def somma(a, b):
    return a + b

# Funzione con valore di default
def saluta_personalizzato(nome, saluto="Ciao"):
    print(f"{saluto}, {nome}!")

# Utilizzo
saluta()                          # Ciao!
saluta_nome("Mario")              # Ciao, Mario!
risultato = somma(5, 3)           # 8
saluta_personalizzato("Mario")    # Ciao, Mario!
saluta_personalizzato("Mario", "Hey")  # Hey, Mario!
```

#### **Nel nostro gioco:**
```python
def genera_numero_segreto():
    """Genera un numero casuale tra 1 e 100."""
    return random.randint(1, 100)

def controlla_tentativo(tentativo, numero_segreto):
    """Confronta il tentativo dell'utente con il numero segreto."""
    if tentativo == numero_segreto:
        return "corretto"
    # ...
```

---

### 5. 🎣 Gestione Errori con `try/except`

La gestione degli errori permette al programma di **continuare a funzionare** anche se si verificano errori.

#### **Sintassi:**
```python
try:
    # codice che potrebbe causare un errore
except TipoErrore:
    # codice da eseguire se c'è l'errore
```

#### **Eccezioni comuni:**

| Eccezione | Quando si verifica | Esempio |
|------------|-------------------|---------|
| `ValueError` | Valore non appropriato | `int("abc")` |
| `TypeError` | Tipo non appropriato | `2 + "2"` |
| `ZeroDivisionError` | Divisione per zero | `5/0` |
| `FileNotFoundError` | File non esiste | `open("inesistente.txt")` |

#### **Esempio senza gestione errori:**
```python
numero = int(input("Inserisci un numero: "))
# Se l'utente inserisce "abc" → Il programma si blocca con errore!
```

#### **Esempio con gestione errori:**
```python
try:
    numero = int(input("Inserisci un numero: "))
    print(f"Hai inserito: {numero}")
except ValueError:
    print("⚠️ Per favore inserisci un numero valido!")
    # Il programma continua!
```

#### **Nel nostro gioco:**
```python
try:
    tentativo = int(input("\n🎯 Inserisci un numero tra 1 e 100: "))
    if 1 <= tentativo <= 100:
        return tentativo
    else:
        print("⚠️ Il numero deve essere tra 1 e 100!")
except ValueError:
    print("⚠️ Per favore inserisci un numero valido!")
```

---

### 6. 💬 Input/Output

L'interazione con l'utente avviene tramite `input()` e `print()`.

#### **Input con `input()`:**

```python
# input() restituisce SEMPRE una stringa
nome = input("Come ti chiami? ")  # tipo: str
print(f"Ciao, {nome}!")

# Conversione in numero
eta = int(input("Quanti anni hai? "))  # tipo: int
print(f"L'anno prossimo ne avrai {eta + 1}")

# Conversione in float
altezza = float(input("Quanto sei alto? "))  # tipo: float
```

#### **Output con `print()`:**

```python
# Print semplice
print("Ciao mondo!")

# Print con variabili (metodo vecchio)
print("Ciao,", nome)

# Print con f-string (metodo moderno - RACCOMANDATO)
print(f"Ciao, {nome}!")

# Print multipli
print("Ciao", nome, "!", sep="-")  # Ciao-Mario-!

# Print con formattazione
numero = 3.14159
print(f"Pi greco: {numero:.2f}")   # Pi greco: 3.14
print(f"Numero: {numero:010.2f}")  # Numero: 0000003.14
```

#### **Stringhe speciali:**

| Carattere | Significato | Esempio |
|-----------|-------------|---------|
| `\n` | Nuova riga | `print("Ciao\nMondo")` |
| `\t` | Tabulazione | `print("Ciao\tMondo")` |
| `\\` | Backslash | `print("C:\\cartella")` |
| `\"` | Virgolette | `print("Dice \"Ciao\"")` |

#### **Nel nostro gioco:**
```python
# Input
tentativo = int(input("\n🎯 Inserisci un numero tra 1 e 100: "))
scelta = input("\n🔄 Vuoi giocare ancora? (s/n): ").lower().strip()

# Output
print(f"🎉 COMPLIMENTI! Hai indovinato il numero {numero_segreto}!")
print(f"📈 Hai usato {tentativi} tentativi.")
```

---

### 7. 📝 Docstring

Le **docstring** sono commenti speciali che documentano le funzioni.

#### **Sintassi:**
```python
def nome_funzione(parametri):
    """Questa è una docstring su una riga."""

    pass

def altra_funzione(parametri):
    """
    Questa è una docstring
    su più righe.

    Può contenere:
    - Descrizione della funzione
    - Parametri
    - Valore restituito
    - Esempi
    """
    pass
```

#### **Perché usarle?**
```python
# Senza docstring
def calcola(a, b):
    return a * b
# Cosa fa? Moltiplica? Somma? Potenza?

# Con docstring
def calcola(a, b):
    """Moltiplica due numeri e restituisce il risultato."""
    return a * b
# Ora è chiaro!

# Accesso alla docstring
help(calcola)
# Output: Moltiplica due numeri e restituisce il risultato.
```

#### **Nel nostro gioco:**
```python
def genera_numero_segreto():
    """Genera un numero casuale tra 1 e 100."""
    return random.randint(1, 100)

def controlla_tentativo(tentativo, numero_segreto):
    """
    Confronta il tentativo dell'utente con il numero segreto.
    Restituisce 'corretto', 'basso' o 'alto'.
    """
    # ...
```

---

## 💪 Esercizi Proposti

Ora che hai capito come funziona il gioco, è tempo di **mettere in pratica** quello che hai imparato! Eccoti una serie di esercizi in ordine di difficoltà.

---

### 🟢 Livello: Principiante

#### **1. 🎯 Aggiungi un Livello "Impossibile"**

Il gioco ha già 3 livelli. Aggiungi un quarto livello "Impossibile" con solo **3 tentativi**!

**Suggerimento:** Modifica la funzione `scegli_difficolta()` aggiungendo un'opzione `elif scelta == "I":` con 3 tentativi.

---

#### **2. 🎯 Modifica il Range dei Numeri**

Attualmente il gioco usa numeri da 1 a 100. Modifica il gioco per usare:

```python
# A) Numeri da 1 a 50 (più facile)
# B) Numeri da 1 a 1000 (più difficile)
# C) Numeri da -50 a 50 (con numeri negativi!)
```

**Suggerimento:** Modifica la funzione `genera_numero_segreto()` e aggiorna tutti i messaggi che mostrano il range.

---

#### **3. 📊 Sistema di Punteggio**

Aggiungi un sistema di punteggio basato su:
1. Numero di tentativi usati
2. Difficoltà scelta

```python
# Esempio di formula:
Punteggio base:
  - 1 tentativo: 1000 punti
  - 2 tentativi: 500 punti
  - 3 tentativi: 250 punti
  - Ogni altro: 100 punti

Moltiplicatore difficoltà:
  - Facile: ×1
  - Medio: ×2
  - Difficile: ×3
```

**Suggerimento:** Crea una funzione `calcola_punteggio()` e chiamala alla fine di ogni partita vinta.

---

#### **4. 🔢 Personalizza il Range dei Tentativi**

---

### 🟡 Livello: Intermedio

#### **5. 💾 Salva il Miglior Punteggio**

Salva il miglior punteggio in un file e leggilo all'avvio:

```python
import json

def carica_record():
    """Carica il record dal file."""
    try:
        with open('record.json', 'r') as f:
            dati = json.load(f)
            return dati.get('miglior_punteggio', 0)
    except FileNotFoundError:
        return 0

def salva_record(punteggio):
    """Salva il record nel file se è un nuovo record."""
    try:
        with open('record.json', 'r') as f:
            dati = json.load(f)
    except FileNotFoundError:
        dati = {}

    if punteggio > dati.get('miglior_punteggio', 0):
        dati['miglior_punteggio'] = punteggio
        with open('record.json', 'w') as f:
            json.dump(dati, f)
        print(f"🏆 NUOVO RECORD! {punteggio} punti!")
```

**Suggerimento:** Chiama `carica_record()` all'inizio di `main()` e `salva_record()` dopo ogni vittoria.

---

#### **6. ⏱️ Modalità Contro Crono**

Aggiungi un timer per vedere quanto velocemente indovini:

```python
import time

def gioca_con_timer(tentativi_massimi):
    """Gioca con un timer."""
    tempo_inizio = time.time()

    # Usa la funzione gioca() esistente
    vittoria = gioca(tentativi_massimi)

    tempo_fine = time.time()
    tempo_totale = tempo_fine - tempo_inizio

    print(f"\n⏱️ Tempo impiegato: {tempo_totale:.1f} secondi")

    if vittoria:
        # Calcola un punteggio basato su tempo e tentativi
        punteggio_tempo = int(1000 / tempo_totale)
        print(f"🎯 Punteggio velocità: {punteggio_tempo} punti")

    return vittoria
```

---

#### **7. 📊 Statistiche Avanzate**

Traccia le statistiche durante la sessione di gioco:

```python
statistiche = {
    'partite_giocate': 0,
    'vittorie': 0,
    'sconfitte': 0,
    'livello_completati': {'F': 0, 'M': 0, 'D': 0},
    'serie_vittorie': 0,
    'max_serie_vittorie': 0
}

def aggiorna_statistiche(vittoria, tentativi_massimi):
    """Aggiorna le statistiche dopo ogni partita."""
    statistiche['partite_giocate'] += 1
    if vittoria:
        statistiche['vittorie'] += 1
        # Determina il livello
        if tentativi_massimi == 15:
            statistiche['livello_completati']['F'] += 1
        elif tentativi_massimi == 10:
            statistiche['livello_completati']['M'] += 1
        else:
            statistiche['livello_completati']['D'] += 1
    else:
        statistiche['sconfitte'] += 1
```

**Suggerimento:** Crea una funzione `mostra_statistiche()` che mostri un riepilogo alla fine della sessione.

---

#### **8. 🔢 Lascia all'Utente il Numero di Tentativi**

Invece di scegliere tra preset, lascia che l'utente inserisca il numero di tentativi che desidera:

```python
def scegli_difficolta_personalizzata():
    """Permette all'utente di scegliere il numero esatto di tentativi."""
    print("Scegli la modalità:")
    print("  [P] Preset (Facile/Medio/Difficile)")
    print("  [C] Personalizzato")

    scelta = input("Scelta (P/C): ").strip().upper()

    if scelta == "P":
        # Usa il codice esistente
        return scegli_difficolta()
    elif scelta == "C":
        while True:
            try:
                tentativi = int(input("Inserisci il numero di tentativi (1-50): "))
                if 1 <= tentativi <= 50:
                    print(f"\nHai scelto: {tentativi} tentativi personalizzati.\n")
                    return tentativi
                else:
                    print("Il numero deve essere tra 1 e 50!")
            except ValueError:
                print("Inserisci un numero valido!")
```

---

### 🔴 Livello: Avanzato

#### **9. 👥 Modalità Multigiocatore**

Permetti a 2 giocatori di sfidarsi:

```python
def modalita_multigiocatore():
    """Due giocatori si sfidano a chi indovina prima."""
    print("Modalità Multigiocatore!")
    nome1 = input("Nome Giocatore 1: ")
    nome2 = input("Nome Giocatore 2: ")

    numero_segreto = genera_numero_segreto()

    # Giocatore 1
    print(f"\nTurno di {nome1}")
    tentativi1 = gioca_turno(numero_segreto)

    # Giocatore 2
    print(f"\nTurno di {nome2}")
    tentativi2 = gioca_turno(numero_segreto)

    # Dichiarazione vincitore
    if tentativi1 < tentativi2:
        print(f"🏆 {nome1} vince!")
    elif tentativi2 < tentativi1:
        print(f"🏆 {nome2} vince!")
    else:
        print("🤝 Pareggio!")
```

---

#### **10. 🤖 Suggerimenti Intelligenti**

Implementa un sistema che dà suggerimenti più intelligenti basati su quanto è vicino il tentativo:

```python
def da_suggerimento_intelligente(tentativo, numero_segreto):
    """
    Dà suggerimenti basati su quanto è vicino il tentativo.
    """
    differenza = abs(tentativo - numero_segreto)

    if differenza == 0:
        return "🎉 ESATTO!"
    elif differenza <= 3:
        return "🔥 FUOCISSIMO! Sei vicinissimo (meno di 3 numeri)!"
    elif differenza <= 10:
        return "🌡️ MOLTO CALDO! Sei molto vicino!"
    elif differenza <= 25:
        return("😐 TIEPIDO... Non troppo vicino.")
    elif differenza <= 50:
        return("🧊 FREDDO... Sei lontano.")
    else:
        return("❄️ GLACIALE! Sei molto lontano!")
```

**Suggerimento:** Sostituisci la funzione `mostra_feedback()` con una versione che usa questa funzione.

---

#### **11. 📈 Mostra lo Storico dei Tentativi**

Alla fine di ogni partita, mostra una tabella con tutti i tentativi fatti:

```python
def gioca_con_storico(tentativi_massimi):
    """Versione di gioca() che traccia lo storico."""
    numero_segreto = genera_numero_segreto()
    tentativo_corrente = 0
    storico = []  # Lista per salvare i tentativi

    while tentativo_corrente < tentativi_massimi:
        # ... codice esistente ...

        # Aggiungi lo storico
        storico.append({
            'tentativo': tentativo,
            'risultato': risultato,
            'numero_corretto': numero_segreto if risultato == "corretto" else "?"
        })

        # ... resto del codice ...

    # Mostra lo storico alla fine
    mostra_storico(storico)
    return vittoria

def mostra_storico(storico):
    """Mostra una tabella con i tentativi fatti."""
    print("\n📊 STORICO DEI TENTATIVI:")
    print("-" * 60)
    print(f"{'#':<5} {'Tentativo':<15} {'Risultato':<20}")
    print("-" * 60)

    for i, entry in enumerate(storico, 1):
        print(f"{i:<5} {entry['tentativo']:<15} {entry['risultato']:<20}")

    print("-" * 60)
```

---

#### **12. 🎲 Differenti Modalità di Gioco**

Aggiungi diverse modalità:

```python
def modalita_classica():
    """Indovina un numero tra 1 e 100."""
    pass  # Codice attuale

def modalita_indovina_numero():
    """
    Il computer indovina il tuo numero!
    Devi pensare a un numero e il computer prova a indovinarlo.
    """
    print("Pensa a un numero tra 1 e 100!")
    print("Rispondi con 'alto', 'basso' o 'corretto'.")

    # Implementa la ricerca binaria!
    pass

def modalita_inversione():
    """
    Tu dici se il numero segreto è più alto o più basso
    e il computer cerca di indovinarlo.
    """
    pass
```

---

#### **9. 🤖 Suggerimenti Intelligente**

Implementa un sistema che dà suggerimenti più intelligenti:

```python
def da_suggerimento_intelligente(tentativo, numero_segreto, tentativi_fatti):
    """
    Dà suggerimenti basati su quanto è vicino il tentativo.
    """
    differenza = abs(tentativo - numero_segreto)

    if differenza <= 5:
        return "🔥 Sei FUOCISSIMO! Sei vicinissimo!"
    elif differenza <= 15:
        return("🌡️ Sei CALDO! Sei vicino!")
    elif differenza <= 30:
        return("😐 Tiepido... Non troppo vicino.")
    else:
        return("❄️ Sei FREDDO! Sei lontano.")
```

---

#### **14. 🤖 Modalità Inversa (Il Computer Indovina)**

Il gioco inverso: il computer indovina il tuo numero!

```python
def modalita_computer_indovina():
    """
    Il computer prova a indovinare il numero a cui stai pensando.
    Tu rispondi "alto", "basso" o "corretto".
    """
    print("🤖 MODALITÀ: IL COMPUTER INDOVINA!")
    print("Pensa a un numero tra 1 e 100.")
    input("Premi INVIO quando hai scelto il numero...")

    minimo = 1
    massimo = 100
    tentativi = 0

    while True:
        tentativi += 1
        # Strategia ottima: ricerca binaria!
        tentativo_computer = (minimo + massimo) // 2

        print(f"\n🤖 Il computer prova: {tentativo_computer}")

        risposta = input("Il tuo numero è [a]lto, [b]asso o [c]orretto? ").strip().lower()

        if risposta == 'c':
            print(f"\n🎉 Il computer ha indovinato in {tentativi} tentativi!")
            return tentativi
        elif risposta == 'a':
            massimo = tentativo_computer - 1
        elif risposta == 'b':
            minimo = tentativo_computer + 1
        else:
            print("Risposta non valida!")
            tentativi -= 1  # Non contare questo tentativo
```

**Nota:** Questa modalità implementa la **ricerca binaria**, che è l'algoritmo ottimale per questo gioco! Con questa strategia, il computer indovinerà sempre entro 7 tentativi al massimo!

---

#### **15. 🎨 Interfaccia Grafica (GUI)**

Crea una versione con interfaccia grafica usando `tkinter`:

```python
import tkinter as tk
from tkinter import messagebox

class GiocoIndovinaNumero:
    def __init__(self, root):
        self.root = root
        self.root.title("Indovina il Numero")

        self.numero_segreto = random.randint(1, 100)
        self.tentativi = 0

        # Crea gli elementi GUI
        self.etichetta = tk.Label(root, text="Indovina il numero (1-100):")
        self.etichetta.pack()

        self.input = tk.Entry(root)
        self.input.pack()

        self.bottone = tk.Button(root, text="Prova!", command=self.controlla)
        self.bottone.pack()

        self.risultato = tk.Label(root, text="")
        self.risultato.pack()

    def controlla(self):
        tentativo = int(self.input.get())
        self.tentativi += 1

        if tentativo == self.numero_segreto:
            self.risultato.config(text=f"Complimenti! Hai vinto in {self.tentativi} tentativi!")
        elif tentativo < self.numero_segreto:
            self.risultato.config(text="Troppo basso!")
        else:
            self.risultato.config(text="Troppo alto!")

if __name__ == "__main__":
    root = tk.Tk()
    gioco = GiocoIndovinaNumero(root)
    root.mainloop()
```

---

### 🌟 Sfide Extra

#### **🎯 Sfida 1: Algoritmo Ottimale**

Qual è la strategia migliore per indovinare il numero nel minor numero di tentativi possibili?

**Suggerimento:** Ricerca binaria! Prova sempre il numero nel mezzo del range attuale.

```python
# Strategia ottima: Ricerca binaria
# Range: 1-100
# Tentativo 1: 50 (metà di 1-100)
# Se troppo alto → prova 25 (metà di 1-50)
# Se troppo basso → prova 75 (metà di 50-100)
# ...

# Massimo tentativi necessari con ricerca binaria: log2(100) ≈ 7
```

---

#### **🧮 Sfida 2: Calcola la Probabilità**

Calcola e mostra la probabilità di indovinare al prossimo tentativo:

```python
def calcola_probabilita(range_min, range_max):
    """
    Calcola la probabilità di indovinare.
    Se il range possibile è 20 numeri, probabilità = 1/20 = 5%
    """
    numeri_possibili = range_max - range_min + 1
    probabilita = (1 / numeri_possibili) * 100
    return probabilita

# Esempio d'uso
# Se sai che il numero è tra 20 e 30:
# 11 numeri possibili → probabilità ≈ 9%
```

---

#### **📈 Sfida 3: Visualizza lo Storico**

Mostra allo schermo la storia dei tentativi fatti:

```python
def mostra_storico(tentativi, suggerimenti):
    """Mostra una tabella con i tentativi fatti."""
    print("\n📊 STORICO DEI TENTATIVI:")
    print("-" * 40)
    print(f"{'Tentativo':<12} {'Numero':<12} {'Risultato'}")
    print("-" * 40)

    for i, (num, sug) in enumerate(zip(tentativi, suggerimenti), 1):
        print(f"{i:<12} {num:<12} {sug}")

    print("-" * 40)
```

---

## ❓ FAQ - Domande Frequenti

### 🤔 Domande Generali

#### **Q: Devo memorizzare tutto il codice?**

**R:** No! I programmanti usano sempre riferimento e documentazione. L'importante è:
- ✅ Capire i **concetti** (cos'è un loop, una funzione, etc.)
- ✅ Sapere **cercare** quando serve
- ✅ **Praticare** regolarmente

---

#### **Q: Quanto tempo ci vorrà per completare questo progetto?**

**R:** Dipende dalla tua esperienza:
- 🟢 **Principiante assoluto:** 2-3 ore
- 🟡 **Ha fatto qualche esercizio:** 1-2 ore
- 🟢 **Conosce già le basi:** 30-60 minuti

---

#### **Q: Come posso testare che il codice funzioni?**

**R:** Ecco un piano di test:

```python
# Test 1: Verifica che il numero sia tra 1 e 100
for _ in range(100):
    numero = random.randint(1, 100)
    assert 1 <= numero <= 100, f"Numero fuori range: {numero}"

# Test 2: Verifica la funzione controlla_tentativo
assert controlla_tentativo(50, 50) == "corretto"
assert controlla_tentativo(40, 50) == "basso"
assert controlla_tentativo(60, 50) == "alto"

# Test 3: Verifica la gestione errori
# Prova a inserire lettere invece di numeri
```

---

### 💻 Domande Tecniche

#### **Q: Perché usiamo `while True` e poi `break`?**

**R:** È un pattern comune quando non sappiamo quante volte dovremo ripetere un'azione:

```python
while True:  # Ripeti per sempre
    # ... fai qualcosa ...
    if condizione_di_uscita:
        break  # Esci dal loop
```

**Alternativa più leggibile:**
```python
continuare = True
while continuare:
    # ... fai qualcosa ...
    if condizione_di_uscita:
        continuare = False
```

---

#### **Q: Qual è la differenza tra `return` e `print`?**

**R:**

| Aspetto | `print` | `return` |
|---------|---------|----------|
| **Cosa fa** | Mostra sullo schermo | Restituisce un valore |
| **Chi lo usa** | L'utente che guarda | Il programma che lo usa |
| **Può essere assegnato** | No | Sì |
| **Esce dalla funzione** | No | Sì |

```python
def esempio_print():
    print("Ciao")
    # Continua l'esecuzione

def esempio_return():
    return "Ciao"
    # Esce immediatamente dalla funzione

# Utilizzo
esempio_print()           # Mostra: Ciao
messaggio = esempio_return()  # Non mostra nulla, ma restituisce "Ciao"
print(messaggio)          # Mostra: Ciao
```

---

#### **Q: Perché usiamo f-string invece di altri metodi?**

**R:** Le f-string sono il metodo più moderno e leggibile:

```python
# Metodo vecchio (non raccomandato)
print("Ciao, " + nome + "!")

# Metodo format (ok)
print("Ciao, {}!".format(nome))

# F-string (RACCOMANDATO - Python 3.6+)
print(f"Ciao, {nome}!")

# F-string sono meglio perché:
# 1. Più leggibili
# 2. Più veloci
# 3. Permettono espressioni
print(f"2 + 2 = {2+2}")  # 2 + 2 = 4
```

---

#### **Q: Cos'è `if __name__ == "__main__":`?**

**R:** È un pattern Python che permette di:
1. Eseguire il codice quando il file viene lanciato direttamente
2. Importare le funzioni senza eseguire automaticamente il codice

```python
# number_guess.py
def funzione_util():
    return "Utile"

if __name__ == "__main__":
    # Questo viene eseguito SOLO se lancio:
    # python number_guess.py
    print("Avvio del gioco...")

# altro_file.py
import number_guess

# Posso usare funzione_util() senza avviare il gioco!
print(number_guess.funzione_util())
```

---

### 🐛 Risoluzione Problemi

#### **Q: Il programma si blocca quando inserisco lettere!**

**R:** Assicurati di aver racchiuso l'input in un blocco `try/except`:

```python
# ❌ SBAGLIATO - Si blocca con lettere
numero = int(input("Inserisci un numero: "))

# ✅ CORRETTO - Gestisce l'errore
try:
    numero = int(input("Inserisci un numero: "))
except ValueError:
    print("Devi inserire un numero!")
```

---

#### **Q: Il loop non finisce mai!**

**R:** Controlla che ci sia una condizione di uscita:

```python
# ❌ SBAGLIATO - Loop infinito
while True:
    # ... codice ...
    # Manca il break!

# ✅ CORRETTO - Ha condizione di uscita
while tentativi < max_tentativi:
    # ... codice ...
    # Quando tentativi >= max_tentativi, esce

# OPPURE
while True:
    # ... codice ...
    if condizione:
        break  # Esce explicitamente
```

---

#### **Q: Il numero generato è sempre lo stesso!**

**R:** Questo è normale! `random.randint()` genera numeri diversi ogni volta che **chiami** la funzione, non ogni volta che esegui il programma.

```python
# Se scrivi questo:
numero = random.randint(1, 100)
print(numero)  # Es: 42

# Ogni volta che esegui il programma, avrai un numero diverso
# Ma durante lo stesso esecuzione, se non chiami più la funzione,
# il numero rimane lo stesso

# Per avere un numero diverso ogni partita:
def gioca_partita():
    numero_segreto = random.randint(1, 100)  # Chiami ogni volta!
```

---

### 📚 Domande di Apprendimento

#### **Q: Come posso migliorare le mie abilità in Python?**

**R:** Ecco un percorso di studio:

1. ✅ **Completa questo progetto** (gioco indovina numero)
2. ✅ **Fai gli esercizi proposti** (vedi sopra)
3. ✅ **Sperimenta** - Modifica il codice, guarda cosa succede
4. ✅ **Costruisci altri progetti** semplici:
   - Calcolatrice
   - Gestione lista della spesa
   - Gioco di trivia
5. ✅ **Studia le librerie** standard:
   - `math` - Funzioni matematiche
   - `datetime` - Date e orari
   - `os` - Operazioni sul sistema
   - `json` - Gestione file JSON

---

#### **Q: Qual è il prossimo progetto che dovrei fare?**

**R:** Una volta completato questo, prova in ordine:

1. 🟢 **Calcolatrice** - Input/output, operazioni matematiche
2. 🟢 **Gestione To-Do List** - Liste, dizionari, file
3. 🟡 **Gioco del Tris** - Logica più complessa, 2 giocatori
4. 🟡 **Sistema di Login** - Gestione password, file
5. 🔴 **Semplice Web Scraper** - Richiede librerie esterne

---

#### **Q: Dove posso trovare altre risorse per imparare?**

**R:** Ecco ottime risorse gratuite:

📚 **Documentazione ufficiale:**
- [Python.org Tutorial](https://docs.python.org/3/tutorial/) - Tutorial ufficiale
- [Python Documentation](https://docs.python.org/3/) - Documentazione completa

🎥 **Video corsi gratuiti:**
- [FreeCodeCamp Python](https://www.youtube.com/watch?v=rfscVS0vtbw) - Corsi completi
- [Programming with Mosh](https://www.youtube.com/@programmingwithmosh) - Tutorial chiari

📖 **Libri gratuiti:**
- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/) - Perfetto per principianti
- [Python for Everybody](https://www.py4e.com/) - Corso universitario gratuito

💻 **Siti di pratica:**
- [Codewars](https://www.codewars.com/) - Sfide di codice
- [HackerRank](https://www.hackerrank.com/) - Esercizi vari livelli
- [LeetCode](https://leetcode.com/) - Per algoritmi (più avanzato)

---

### 🎯 Domande sul Progetto

#### **Q: Posso condividere questo progetto con i miei amici?**

**R:** Assolutamente SÌ! Questo è ottimo perché:
- ✅ Puoi confrontarti con altri
- ✅ Puoi imparare dalle loro soluzioni
- ✅ Puoi insegnare agli altri (impari ancora di più!)

**Suggerimento:** Crea un repository GitHub e condividilo!

---

#### **Q: Come posso personalizzare il gioco?**

**R:** Ecco alcune idee:
- 🎨 Cambia i colori del testo
- 🎵 Aggiungi suoni (con libreria `playsound`)
- 🏆 Aggiungi un sistema di achievement
- 📊 Crea grafici dei risultati (con `matplotlib`)
- 🌐 Supporta più lingue
- 📱 Crea una versione web (con Flask o Django)

---

#### **Q: Il gioco è troppo facile/difficile!**

**R:** Puoi aggiustare la difficoltà:

```python
# Più facile
massimi_tentativi = 15
range_numero = (1, 50)

# Più difficile
massimi_tentativi = 5
range_numero = (1, 1000)

# Estremo
massimi_tentativi = 7
range_numero = (-1000, 1000)
```

---

## 🎉 Conclusione

Congratulazioni per aver completato (o essere in procinto di completare) il tuo primo progetto Python! Ricorda:

### ✅ Cosa hai imparato:
- 🔢 Come usare input/output
- 🎲 Come generare numeri casuali
- ➰ Come usare i cicli
- 🔀 Come prendere decisioni con if/elif/else
- 📦 Come organizzare il codice in funzioni
- 🎣 Come gestire gli errori

### 🚀 Prossimi passi:
1. **Completa gli esercizi** proposti sopra
2. **Sperimenta** con il codice
3. **Condividi** il tuo progetto
4. **Crea** nuovi progetti
5. **Insegna** ad altri (la miglior forma di apprendimento!)

### 💡 Ricorda:
> "L'unico modo per imparare a programmare è programmando."
> — Nonno di tutti i programmatori

---

<div align="center">

## 🎮 Buon divertimento con la programmazione!

**Se hai domande o vuoi condividere il tuo progetto, non esitare!**

Made with ❤️ for Python learners

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

</div>
