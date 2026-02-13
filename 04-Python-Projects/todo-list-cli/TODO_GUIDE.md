# 📝 Guida Completa: To-Do List CLI in Python

## 🎯 Benvenuto, Studente!

Questa guida ti accompagnerà nella realizzazione del tuo primo progetto Python pratico: una **To-Do List a riga di comando**. Non preoccuparti se sei alle prime armi - questo progetto è pensato proprio per te!

---

## 📋 Indice

1. [Introduzione al Progetto](#introduzione-al-progetto)
2. [Obiettivi di Apprendimento](#obiettivi-di-apprendimento)
3. [Prerequisiti](#prerequisiti)
4. [Istruzioni per l'Uso](#istruzioni-per-luso)
5. [Spiegazione del Codice](#spiegazione-del-codice)
6. [Concetti Python Utilizzati](#concetti-python-utilizzati)
7. [Esercizi Proposti](#esercizi-proposti)
8. [Risorse Utili](#risorse-utili)

---

## 🎓 Introduzione al Progetto

### Cos'è una To-Do List CLI?

Una **To-Do List CLI** (Command Line Interface) è un'applicazione che ti permette di gestire i tuoi compiti direttamente dal terminale, senza interfaccia grafica. Ecco cosa potrai fare:

- ✅ **Aggiungere** nuovi task alla tua lista
- 📋 **Visualizzare** tutti i task presenti
- ❌ **Completare** i task finiti
- 🗑️ **Rimuovere** i task non più necessari
- 💾 **Salvare** la tua lista su file per non perdere nulla

### Perché iniziare con questo progetto?

Questo progetto è **perfetto per iniziare** perché:

1. **Utilizza concetti fondamentali**: liste, dizionari, funzioni, cicli
2. **È immediatamente utile**: puoi usarlo davvero per organizzare i tuoi compiti
3. **Non richiede librerie esterne**: solo Python standard!
4. **E' estendibile**: puoi aggiungere features man mano che impari
5. **Ti insegna il pensiero computazionale**: organizzare dati e operazioni

---

## 🎯 Obiettivi di Apprendimento

Alla fine di questo progetto, saprai:

### Competenze Tecniche
- ✨ Creare e manipolare **liste** in Python
- 📚 Utilizzare **dizionari** per strutturare dati complessi
- 🔄 Scrivere **cicli** (`for`, `while`) per iterare sugli elementi
- 🎯 Definire e utilizzare **funzioni** per organizzare il codice
- 📁 Leggere e scrivere **file** (JSON)
- 🔀 Gestire il **flusso di esecuzione** con `if/elif/else`
- 🎪 Gestire l'**input/output** da terminale

### Competenze Logiche
- 🧩 Pensare in termini di **struttura dati**
- 🔍 Risolvere problemi in modo **modulare**
- 🛠️ Scrivere codice **riutilizzabile**
- 🐛 Debuggare errori comuni

---

## 📚 Prerequisiti

### Conoscenze Necessarie

Prima di iniziare, assicurati di comprendere:

#### 1. Variabili e Tipi di Dato
```python
# Variabili
nome = "Mario"
eta = 20
task_completato = True

# Tipi base
stringa = "Questo è un testo"
numero_intero = 42
numero_decimale = 3.14
booleano = True
```

#### 2. Operazioni Base
```python
# Operazioni aritmetiche
somma = 5 + 3
differenza = 10 - 2
prodotto = 4 * 7
quoziente = 20 / 4

# Operazioni su stringhe
testo = "Hello, " + "World!"  # Concatenazione
lunghezza = len(testo)        # Lunghezza
```

#### 3. Condizioni
```python
eta = 18

if eta >= 18:
    print("Sei maggiorenne")
else:
    print("Sei minorenne")
```

#### 4. Cicli Base
```python
# Ciclo for
for i in range(5):
    print(i)  # Stampa 0, 1, 2, 3, 4

# Ciclo while
conto = 0
while conto < 3:
    print(conto)
    conto += 1
```

### Installazione Python

1. **Verifica se Python è installato:**
   ```bash
   python --version
   # oppure
   python3 --version
   ```

2. **Se non installato, scaricalo da:** [python.org](https://www.python.org/downloads/)

3. **IDE Consigliato:**
   - **VS Code** + Python Extension (gratuito, potente)
   - **PyCharm Community** (gratuito, completo)
   - **Thonny** (molto semplice per principianti)

---

## 🚀 Istruzioni per l'Uso

### Come Eseguire il Programma

1. **Apri il terminale** nella cartella del progetto:
   ```bash
   cd "C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects"
   ```

2. **Esegui il programma:**
   ```bash
   python todo.py
   # oppure
   python3 todo.py
   ```

### Esempio di Interazione

Ecco cosa vedrai quando eseguirai il programma:

```
╔════════════════════════════════════════╗
║     📝 LA TUA TO-DO LIST              ║
╚════════════════════════════════════════╝

Menu:
1. ➕ Aggiungi un nuovo task
2. 📋 Mostra tutti i task
3. ✅ Segna task come completato
4. ❌ Rimuovi un task
5. 💾 Salva la lista
6. 📖 Carica la lista
7. 🚪 Esci

Scegli un'opzione (1-7): _
```

### Flusso Tipico di Utilizzo

#### Scenario 1: Creare la Prima Lista

```
Scegli un'opzione (1-7): 1
Inserisci il task: Studiare Python
Priorità (alta/media/bassa): alta
Categoria: studio

✅ Task aggiunto!

Scegli un'opzione (1-7): 1
Inserisci il task: Fare la spesa
Priorità (alta/media/bassa): media
Categoria: personale

✅ Task aggiunto!

Scegli un'opzione (1-7): 2

📋 LA TUA TO-DO LIST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] 1. Studiare Python (Priorità: alta, Categoria: studio)
[ ] 2. Fare la spesa (Priorità: media, Categoria: personale)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Totale: 2 task
```

#### Scenario 2: Completare un Task

```
Scegli un'opzione (1-7): 3
Quale task vuoi completare? (inserisci il numero): 1

✅ Task "Studiare Python" completato!

Scegli un'opzione (1-7): 2

📋 LA TUA TO-DO LIST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[✓] 1. Studiare Python (Priorità: alta, Categoria: studio)
[ ] 2. Fare la spesa (Priorità: media, Categoria: personale)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Totale: 2 task (1 completati)
```

#### Scenario 3: Salvare e Ricaricare

```
Scegli un'opzione (1-7): 5
💾 Lista salvata in 'todo_list.json'

(Chiudi il programma... Riapri...)

Scegli un'opzione (1-7): 6
📖 Lista caricata da 'todo_list.json'

Scegli un'opzione (1-7): 2

📋 LA TUA TO-DO LIST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[✓] 1. Studiare Python (Priorità: alta, Categoria: studio)
[ ] 2. Fare la spesa (Priorità: media, Categoria: personale)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Totale: 2 task (1 completati)
```

---

## 📖 Spiegazione del Codice

### Struttura del Programma

Il programma è organizzato in **funzioni**, ognuna con un compito specifico:

```
todo.py
├── mostra_menu()           : Mostra il menu principale
├── aggiungi_task()         : Aggiunge un nuovo task
├── mostra_task()           : Visualizza tutti i task
├── completa_task()         : Segna un task come completato
├── rimuovi_task()          : Rimuove un task
├── salva_lista()           : Salva la lista su file
├── carica_lista()          : Carica la lista da file
└── main()                  : Funzione principale
```

---

### Analisi Funzione per Funzione

#### 1. Struttura Dati

```python
# Lista principale: contiene tutti i task
todo_list = []

# Esempio di task (dizionario)
task = {
    "titolo": "Studiare Python",
    "completato": False,
    "priorita": "alta",
    "categoria": "studio"
}
```

**Spiegazione:**
- **`todo_list`**: Una lista che contiene dizionari (ogni dizionario è un task)
- **Ogni task ha:**
  - `titolo`: Descrizione del task (stringa)
  - `completato`: Stato (True/False)
  - `priorita`: Importanza (alta/media/bassa)
  - `categoria`: Tipo di task (studio/lavoro/personale)

#### 2. Funzione `mostra_menu()`

```python
def mostra_menu():
    """Mostra il menu principale all'utente"""
    print("\n╔════════════════════════════════════════╗")
    print("║     📝 LA TUA TO-DO LIST              ║")
    print("╚════════════════════════════════════════╝")
    print("\nMenu:")
    print("1. ➕ Aggiungi un nuovo task")
    print("2. 📋 Mostra tutti i task")
    print("3. ✅ Segna task come completato")
    print("4. ❌ Rimuovi un task")
    print("5. 💾 Salva la lista")
    print("6. 📖 Carica la lista")
    print("7. 🚪 Esci")
```

**Cosa imparerai:**
- 📝 Come definire una **funzione** con `def`
- 📄 Come stampare testo formattato
- 💡 L'importanza di documentare con **docstring** (`"""..."""`)

#### 3. Funzione `aggiungi_task()`

```python
def aggiungi_task():
    """Aggiunge un nuovo task alla lista"""
    titolo = input("Inserisci il task: ")

    # Validazione input
    while True:
        priorita = input("Priorità (alta/media/bassa): ").lower()
        if priorita in ["alta", "media", "bassa"]:
            break
        print("⚠️ Priorità non valida! Riprova.")

    categoria = input("Categoria: ")

    # Crea il dizionario del task
    nuovo_task = {
        "titolo": titolo,
        "completato": False,
        "priorita": priorita,
        "categoria": categoria
    }

    todo_list.append(nuovo_task)
    print("\n✅ Task aggiunto!")
```

**Cosa imparerai:**
- 🎯 Come usare `input()` per ricevere dati dall'utente
- 🔄 Come validare l'input con un `while True`
- 📦 Come creare un **dizionario**
- ➕ Come aggiungere elementi a una lista con `.append()`

#### 4. Funzione `mostra_task()`

```python
def mostra_task():
    """Mostra tutti i task nella lista"""
    if not todo_list:
        print("\n📋 La tua lista è vuota!")
        return

    print("\n📋 LA TUA TO-DO LIST:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    for i, task in enumerate(todo_list, start=1):
        stato = "[✓]" if task["completato"] else "[ ]"
        print(f"{stato} {i}. {task['titolo']} "
              f"(Priorità: {task['priorita']}, "
              f"Categoria: {task['categoria']})")

    completati = sum(1 for task in todo_list if task["completato"])
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Totale: {len(todo_list)} task ({completati} completati)")
```

**Cosa imparerai:**
- 🔄 Come usare `enumerate()` per avere indice e valore
- ❌ Come verificare se una lista è vuota con `if not lista`
- 🔢 Come usare **f-string** per formattare stringhe
- 🧮 Come contare elementi con `.sum()` e generator expressions
- 🔀 Come usare l'operatore ternario: `valore1 if condizione else valore2`

#### 5. Funzione `completa_task()`

```python
def completa_task():
    """Segna un task come completato"""
    if not todo_list:
        print("\n⚠️ Nessun task da completare!")
        return

    mostra_task()

    while True:
        try:
            indice = int(input("\nQuale task vuoi completare? (inserisci il numero): "))
            if 1 <= indice <= len(todo_list):
                todo_list[indice - 1]["completato"] = True
                print(f"\n✅ Task '{todo_list[indice - 1]['titolo']}' completato!")
                break
            else:
                print("⚠️ Numero non valido! Riprova.")
        except ValueError:
            print("⚠️ Inserisci un numero valido!")
```

**Cosa imparerai:**
- 🔢 Come convertire stringhe in numeri con `int()`
- 🔒 Come gestire errori con `try/except`
- 🎯 Come validare che un numero sia in un range
- 📝 Come accedere agli elementi di una lista con l'indice
- ⚠️ Nota: usiamo `indice - 1` perché l'utente vede numeri da 1, ma Python usa indici da 0

#### 6. Funzione `rimuovi_task()`

```python
def rimuovi_task():
    """Rimuove un task dalla lista"""
    if not todo_list:
        print("\n⚠️ Nessun task da rimuovere!")
        return

    mostra_task()

    while True:
        try:
            indice = int(input("\nQuale task vuoi rimuovere? (inserisci il numero): "))
            if 1 <= indice <= len(todo_list):
                task_rimosso = todo_list.pop(indice - 1)
                print(f"\n❌ Task '{task_rimosso['titolo']}' rimosso!")
                break
            else:
                print("⚠️ Numero non valido! Riprova.")
        except ValueError:
            print("⚠️ Inserisci un numero valido!")
```

**Cosa imparerai:**
- 🗑️ Come rimuovere elementi con `.pop(indice)`
- 💾 Come `.pop()` restituisce l'elemento rimosso
- 🔄 Pattern di validazione già visto in `completa_task()`

#### 7. Funzione `salva_lista()`

```python
import json

def salva_lista():
    """Salva la lista in un file JSON"""
    try:
        with open("todo_list.json", "w") as file:
            json.dump(todo_list, file, indent=4)
        print("\n💾 Lista salvata in 'todo_list.json'")
    except Exception as e:
        print(f"\n⚠️ Errore nel salvataggio: {e}")
```

**Cosa imparerai:**
- 📦 Come importare il modulo `json`
- 📁 Come aprire un file con `with open()`
- 💾 Come scrivere dati in JSON con `json.dump()`
- 🔒 Come gestire errori con `try/except`
- ✨ L'importanza del contest manager `with` (chiude automaticamente il file)

#### 8. Funzione `carica_lista()`

```python
def carica_lista():
    """Carica la lista da un file JSON"""
    global todo_list  # Necessario per modificare la variabile globale

    try:
        with open("todo_list.json", "r") as file:
            todo_list = json.load(file)
        print("\n📖 Lista caricata da 'todo_list.json'")
    except FileNotFoundError:
        print("\n⚠️ Nessun file salvato trovato!")
    except Exception as e:
        print(f"\n⚠️ Errore nel caricamento: {e}")
```

**Cosa imparerai:**
- 🌍 Come usare `global` per modificare una variabile globale
- 📖 Come leggere dati JSON con `json.load()`
- 🎯 Come gestire file non esistenti con `FileNotFoundError`
- 🔒 Diversi tipi di eccezioni

#### 9. Funzione `main()`

```python
def main():
    """Funzione principale del programma"""
    # Carica la lista all'avvio (se esiste)
    carica_lista()

    while True:
        mostra_menu()

        scelta = input("\nScegli un'opzione (1-7): ")

        if scelta == "1":
            aggiungi_task()
        elif scelta == "2":
            mostra_task()
        elif scelta == "3":
            completa_task()
        elif scelta == "4":
            rimuovi_task()
        elif scelta == "5":
            salva_lista()
        elif scelta == "6":
            carica_lista()
        elif scelta == "7":
            # Chiede se salvare prima di uscire
            salva = input("Vuoi salvare prima di uscire? (s/n): ").lower()
            if salva == "s":
                salva_lista()
            print("👋 Arrivederci!")
            break
        else:
            print("\n⚠️ Scelta non valida! Riprova.")
```

**Cosa imparerai:**
- 🔄 Come usare un `while True` per un loop infinito
- 🔀 Come usare `if/elif/else` per multipli casi
- 🚪 Come usare `break` per uscire da un loop
- 🎯 Come organizzare il flusso principale del programma

#### 10. Blocco `if __name__ == "__main__":`

```python
if __name__ == "__main__":
    main()
```

**Spiegazione:**
- ✨ Questo è lo standard Python per avviare un programma
- 🎯 Permette di importare questo file come modulo senza eseguire automaticamente `main()`
- 📚 Se esegui `python todo.py`, `__name__` è `"__main__"`, quindi `main()` viene eseguita

---

## 🔑 Concetti Python Utilizzati

### 1. Liste (Lists)

```python
# Creare una lista
todo_list = []

# Aggiungere elementi
todo_list.append(task)

# Accedere agli elementi
primo_task = todo_list[0]

# Lunghezza di una lista
numero_task = len(todo_list)

# Iterare su una lista
for task in todo_list:
    print(task["titolo"])
```

**Quando usarle:** Quando hai una collezione ordinata di elementi che può cambiare.

### 2. Dizionari (Dictionaries)

```python
# Creare un dizionario
task = {
    "titolo": "Studiare Python",
    "completato": False
}

# Accedere ai valori
print(task["titolo"])

# Modificare valori
task["completato"] = True

# Verificare se una chiave esiste
if "categoria" in task:
    print(task["categoria"])
```

**Quando usarli:** Quando devi associare chiavi a valori (es. proprietà di un oggetto).

### 3. Cicli (Loops)

#### For Loop
```python
# Iterare su una lista
for task in todo_list:
    print(task["titolo"])

# Con enumerate (indice + valore)
for i, task in enumerate(todo_list, start=1):
    print(f"{i}. {task['titolo']}")
```

#### While Loop
```python
# Loop con condizione
conto = 0
while conto < 5:
    print(conto)
    conto += 1

# Loop infinito con break
while True:
    scelta = input("Scegli: ")
    if scelta == "exit":
        break
```

**Quando usarli:**
- **For**: Quando sai quante iterazioni fare
- **While**: Quando dipende da una condizione

### 4. Funzioni (Functions)

```python
# Definire una funzione
def saluta(nome):
    """Funzione che saluta"""
    return f"Ciao, {nome}!"

# Chiamare una funzione
messaggio = saluta("Mario")
print(messaggio)  # Ciao, Mario!
```

**Vantaggi:**
- ♻️ Riutilizzabilità del codice
- 📦 Organizzazione logica
- 🧪 Facilità di testing

### 5. Input/Output

```python
# Input da utente
nome = input("Come ti chiami? ")

# Output formattato (f-string)
età = 20
print(f"Ciao, {nome}! Hai {età} anni.")
```

### 6. Gestione File e JSON

```python
import json

# Scrivere su file
with open("dati.json", "w") as file:
    json.dump(dati, file)

# Leggere da file
with open("dati.json", "r") as file:
    dati = json.load(file)
```

**Vantaggi di JSON:**
- 📦 Formato standard per lo scambio dati
- 👁️ Leggibile da umani
- 🔄 Supportato da molti linguaggi

### 7. Gestione Errori

```python
try:
    numero = int(input("Inserisci un numero: "))
    print(f"Il numero è: {numero}")
except ValueError:
    print("⚠️ Non hai inserito un numero valido!")
except Exception as e:
    print(f"⚠️ Errore generico: {e}")
```

**Best Practice:**
- 🎯 Cattura eccezioni specifiche prima di quelle generiche
- 📝 Fornisci messaggi di errore chiari
- 🔒 Non esporre dettagli sensibili in produzione

---

## 💪 Esercizi Proposti

### 🟢 ESERCIZI FACILI (Principianti Assoluti)

#### 1. Aggiungi Data di Creazione
**Obiettivo:** Tracciare quando un task è stato creato.

**Suggerimento:**
```python
from datetime import datetime

task = {
    "titolo": "Studiare Python",
    "completato": False,
    "data_creazione": datetime.now().strftime("%Y-%m-%d %H:%M")
}
```

**Risultato:** Ogni task mostra quando è stato creato.

---

#### 2. Mostra Solo Task Completati/Incompleti
**Obiettivo:** Filtra i task per stato.

**Suggerimento:**
```python
def mostra_filtrati(mostra_completati):
    for task in todo_list:
        if task["completato"] == mostra_completati:
            print(task["titolo"])
```

**Risultato:** Nuove opzioni nel menu:
- 8. Mostra solo task completati
- 9. Mostra solo task da fare

---

#### 3. Aggiungi "Modifica Task"
**Obiettivo:** Permetti di modificare il titolo di un task.

**Suggerimento:**
```python
def modifica_task():
    indice = int(input("Quale task vuoi modificare? ")) - 1
    nuovo_titolo = input("Nuovo titolo: ")
    todo_list[indice]["titolo"] = nuovo_titolo
```

**Risultato:** Puoi correggere errori nei task.

---

### 🟡 ESERCIZI INTERMEDI (Hai Capito le Basi)

#### 4. Sistema di Priorità con Ordinamento
**Obiettivo:** Mostra i task ordinati per priorità.

**Suggerimento:**
```python
def ordina_per_priorita():
    # Mappa priorità a numeri
    priorita_valore = {"alta": 3, "media": 2, "bassa": 1}

    # Ordina la lista
    todo_list.sort(
        key=lambda x: priorita_valore[x["priorita"]],
        reverse=True
    )
```

**Risultato:** I task ad alta priorità appaiono per primi.

---

#### 5. Cerca Task per Parola Chiave
**Obiettivo:** Trova task che contengono una certa parola.

**Suggerimento:**
```python
def cerca_task(parola_chiave):
    trovati = []
    for task in todo_list:
        if parola_chiave.lower() in task["titolo"].lower():
            trovati.append(task)
    return trovati
```

**Risultato:** Nuova opzione "Cerca task" nel menu.

---

#### 6. Statistiche della To-Do List
**Obiettivo:** Mostra statistiche utili.

**Suggerimento:**
```python
def mostra_statistiche():
    totali = len(todo_list)
    completati = sum(1 for t in todo_list if t["completato"])
    da_fare = totali - completati
    percentuale = (completati / totali * 100) if totali > 0 else 0

    print(f"📊 STATISTICHE:")
    print(f"Totali: {totali}")
    print(f"Completati: {completati}")
    print(f"Da fare: {da_fare}")
    print(f"Percentuale completamento: {percentuale:.1f}%")
```

**Risultato:** Visualizza il tuo stato di produttività.

---

#### 7. Più Liste (Lavoro, Personale, Studio)
**Obiettivo:** Gestisci liste separate per categorie.

**Suggerimento:**
```python
# Invece di una lista, usa un dizionario di liste
tutte_le_liste = {
    "lavoro": [],
    "personale": [],
    "studio": []
}

# Scegli su quale lista lavorare
lista_corrente = "personale"
```

**Risultato:** Menu per selezionare la categoria di task.

---

### 🔴 ESERCIZI AVANZATI (Challenge)

#### 8. Tag per Task
**Obiettivo:** Assegna più tag a ogni task.

**Suggerimento:**
```python
task = {
    "titolo": "Studiare Python",
    "completato": False,
    "tag": ["studio", "programmazione", "urgente"]
}

# Ricerca per tag
def cerca_per_tag(tag):
    return [t for t in todo_list if tag in t["tag"]]
```

**Risultato:** Puoi categorizzare task in modo più flessibile.

---

#### 9. Deadline e Scadenze
**Obiettivo:** Aggiungi date di scadenza e avvisa se scaduti.

**Suggerimento:**
```python
from datetime import datetime

task = {
    "titolo": "Consegnare progetto",
    "scadenza": "2026-02-15"
}

def controlla_scadenze():
    oggi = datetime.now().date()
    for task in todo_list:
        if "scadenza" in task:
            scadenza = datetime.strptime(task["scadenza"], "%Y-%m-%d").date()
            if scadenza < oggi and not task["completato"]:
                print(f"⚠️ SCADUTO: {task['titolo']}")
```

**Risultato:** Il programma ti avvisa dei task scaduti.

---

#### 10. Export in Formati Diversi
**Obiettivo:** Esporta la lista in TXT, CSV, o Markdown.

**Suggerimento:**
```python
def esporta_txt():
    with open("todo_list.txt", "w") as file:
        for task in todo_list:
            stato = "[X]" if task["completato"] else "[ ]"
            file.write(f"{stato} {task['titolo']}\n")

def esporta_markdown():
    with open("todo_list.md", "w") as file:
        file.write("# La Mia To-Do List\n\n")
        for task in todo_list:
            stato = "- [x]" if task["completato"] else "- [ ]"
            file.write(f"{stato} {task['titolo']}\n")
```

**Risultato:** Puoi condividere la tua lista in vari formati.

---

#### 11. Undo Functionality
**Obiettivo:** Annulla l'ultima azione.

**Suggerimento:**
```python
# Mantiene una storia delle azioni
storia = []

def aggiungi_task():
    # ... codice per aggiungere ...
    storia.append(("aggiungi", todo_list[-1]))

def undo():
    if storia:
        ultima_azione = storia.pop()
        if ultima_azione[0] == "aggiungi":
            todo_list.remove(ultima_azione[1])
        print("↩️ Azione annullata!")
```

**Risultato:** Puoi correggere errori rapidamente.

---

#### 12. Task Ricorrenti
**Obiettivo:** Task che si ripetono (es. "Pulire casa" ogni settimana).

**Suggerimento:**
```python
task = {
    "titolo": "Pulire casa",
    "ricorrente": True,
    "frequenza": "settimanale",
    "ultimo_completamento": "2026-02-04"
}

def controlla_ricorrenti():
    oggi = datetime.now().date()
    for task in todo_list:
        if task.get("ricorrente"):
            # Logica per ricreare il task se passato il tempo
            pass
```

**Risultato:** Task automatici per abitudini ricorrenti.

---

## 🎓 Roadmap di Apprendimento

### Week 1: Fondamenta
- ✅ Variabili e tipi
- ✅ Liste e dizionari
- ✅ Cicli e condizioni
- ✅ Funzioni base

### Week 2: Files e JSON
- ✅ Input/Output
- ✅ Gestione file
- ✅ Formato JSON
- ✅ Error handling

### Week 3: Miglioramenti
- ✅ Completa 3 esercizi facili
- ✅ Completa 2 esercizi intermedi
- ✅ Refactoring del codice

### Week 4: Features Avanzate
- ✅ Sfida con 2 esercizi avanzati
- ✅ Documentazione del codice
- ✅ Condivisione su GitHub

---

## 📚 Risorse Utili

### Documentazione Ufficiale
- 📖 [Python.org Tutorial IT](https://docs.python.org/it/3/tutorial/)
- 📖 [Python Documentation](https://docs.python.org/3/)

### Corsi Gratuiti
- 🎓 [freeCodeCamp Python](https://www.freecodecamp.org/learn/python-for-everybody/)
- 🎓 [Automate the Boring Stuff](https://automatetheboringstuff.com/)
- 🎓 [Codecademy Python](https://www.codecademy.com/learn/learn-python-3)

### Practice
- 💪 [HackerRank Python](https://www.hackerrank.com/domains/python)
- 💪 [LeetCode Python](https://leetcode.com/problemset/all/?difficulty=Easy&topicSlugs=python)
- 💪 [Exercism Python](https://exercism.org/tracks/python)

### Community
- 💬 [Python Italia Discord](https://discord.gg/pythonitalia)
- 💬 [r/learnpython Reddit](https://www.reddit.com/r/learnpython/)
- 💬 [Stack Overflow Python Tag](https://stackoverflow.com/questions/tagged/python)

---

## 🌟 Consigli per il Successo

### Durante lo Sviluppo
1. **Inizia piccolo:** Implementa le funzioni base prima
2. **Testa spesso:** Esegui il programma dopo ogni modifica
3. **Commenta il codice:** Scrivi cosa fa ogni funzione
4. **Non copiare-incollare:** Scrivi il codice a mano per imparare
5. **Sperimenta:** Modifica il codice per vedere cosa succede

### Quando sei Bloccato
1. **Leggi l'errore:** I messaggi di errore ti dicono il problema
2. **Dividi il problema:** Suddividi in parti più piccole
3. **Stampa variabili:** Usa `print()` per vedere i valori
4. **Cerca online:** Qualcuno ha sicuramente avuto lo stesso problema
5. **Chiedi aiuto:** Non aver paura di domandare!

### Buone Pratiche
- ✅ Usa nomi descrittivi per le variabili (`todo_list`, non `x`)
- ✅ Organizza il codice in funzioni piccole e focalizzate
- ✅ Aggiungi docstring alle funzioni
- ✅ Gestisci gli errori in modo graceful
- ✅ Mantieni il codice pulito e indentato correttamente

---

## 🎉 Congratulazioni!

Se sei arrivato fino a qui e hai completato il progetto:

🏆 **Hai creato il tuo primo programma Python utile!**
✨ **Hai imparato concetti fondamentali di programmazione!**
🚀 **Sei pronto per progetti più complessi!**

### Cosa fare dopo?
1. ✅ Condividi il tuo progetto su GitHub
2. ✅ Sfida un amico a migliorarlo
3. ✅ Passa al prossimo progetto: **Number Guessing Game** o **Unit Converter**

---

## 📝 Checklist del Progetto

Usa questa checklist per tenere traccia dei tuoi progressi:

### Base (Obbligatorio)
- [ ] `todo.py` creato e funzionante
- [ ] Menu principale implementato
- [ ] Aggiunta task funzionante
- [ ] Visualizzazione task funzionante
- [ ] Completamento task funzionante
- [ ] Rimozione task funzionante
- [ ] Salvataggio in JSON funzionante
- [ ] Caricamento da JSON funzionante

### Miglioramenti (Consigliati)
- [ ] Almeno 3 esercizi facili completati
- [ ] Almeno 2 esercizi intermedi completati
- [ ] Codice commentato e documentato
- [ ] Gestione errori completa
- [ ] Validazione input utente

### Extra (Sfida)
- [ ] Almeno 1 esercizio avanzato completato
- [ ] README con istruzioni scritte da te
- [ ] Progetto su GitHub
- [ ] Demo del funzionamento

---

**Ricorda:** L'importante non è essere perfetti, ma imparare facendo! Ogni errore è un'opportunità per capire meglio come funziona Python.

Buon coding! 🐍💪

---

*Questa guida è stata creata per accompagnarti nel tuo percorso di apprendimento di Python. Se trovi errori o vuoi suggerire miglioramenti, sentiti libero di contribuire!*
