# Convertitore di Unità in Python
## Progetto Pratico per Studenti Universitari

---

## INDICE

1. [Introduzione al Progetto](#1-introduzione-al-progetto)
2. [Come Usare il Convertitore](#2-come-usare-il-convertitore)
3. [Spiegazione del Codice](#3-spiegazione-del-codice)
4. [Formule di Conversione](#4-formule-di-conversione)
5. [Concetti Python Utilizzati](#5-concetti-python-utilizzati)
6. [Esercizi Proposti](#6-esercizi-proposti)

---

## 1. INTRODUZIONE AL PROGETTO

### Cos'è il Convertitore di Unità?

Il Convertitore di Unità è un'applicazione a riga di comando (CLI) scritta in Python che permette di convertire facilmente tra diverse unità di misura. Supporta tre categorie principali:

- **Temperatura**: Celsius, Fahrenheit, Kelvin
- **Lunghezza**: metri, piedi, chilometri, miglia
- **Peso**: chilogrammi, libbre

Questo progetto è stato progettato specificamente per scopo educativo e dimostra l'uso pratico di funzioni, condizioni, cicli e gestione dell'input in Python.

### Obiettivi di Apprendimento

Attraverso questo progetto imparerai:

- A organizzare il codice in funzioni riutilizzabili
- A gestire l'input dell'utente con validazione
- A implementare formule matematiche di conversione
- A creare un'interfaccia a menu interattiva
- A usare condizionali (if/elif/else) per il controllo di flusso
- A gestire gli errori con try/except
- A strutturare un progetto Python completo

### Prerequisiti

Per completare questo progetto devi conoscere:

- **Base di Python**: variabili, tipi di dati (int, float, str)
- **Input/Output**: funzione `print()` e `input()`
- **Operatori matematici**: `+`, `-`, `*`, `/`
- **Condizionali**: `if`, `elif`, `else`
- **Cicli**: `while`
- **Funzioni**: definizione e chiamata di funzioni

### File del Progetto

```
unit-converter/
├── unit_converter.py      # Codice principale del convertitore
└── README_CONVERTER.md     # Questa documentazione
```

---

## 2. COME USARE IL CONVERTITORE

### Installazione

Il progetto usa solo la libreria standard di Python, quindi non serve installare nulla.

**Passo 1**: Assicurati di avere Python installato (versione 3.6 o superiore)

Verifica con:
```bash
python --version
```

**Passo 2**: Naviga nella cartella del progetto
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\unit-converter"
```

**Passo 3**: Esegui il programma
```bash
python unit_converter.py
```

### Esempi di Conversione Completi

#### ESEMPIO 1: Conversione Temperatura (Celsius -> Fahrenheit)

Convertiamo 25 gradi Celsius in Fahrenheit.

```
============================================================
  UNIT CONVERTER - Convertitore di Unità
============================================================
  Programma didattico per imparare Python
============================================================

------------------------------------------------------------
MENU PRINCIPALE
------------------------------------------------------------
Scegli il tipo di conversione:
  [1] Temperatura
  [2] Lunghezza
  [3] Peso
  [0] Esci dal programma

Inserisci la tua scelta (0-3): 1

============================================================
  CONVERSIONI TEMPERATURA
============================================================
Scegli la conversione desiderata:
  [1] Celsius -> Fahrenheit
  [2] Fahrenheit -> Celsius
  [3] Celsius -> Kelvin
  [4] Kelvin -> Celsius
  [5] Fahrenheit -> Kelvin
  [6] Kelvin -> Fahrenheit

Inserisci il numero della conversione (1-6): 1
Inserisci il valore da convertire: 25

[OK] 25.00 gradi Celsius = 77.00 gradi Fahrenheit
```

#### ESEMPIO 2: Conversione Lunghezza (Metri -> Miglia)

Convertiamo 1000 metri in miglia.

```
------------------------------------------------------------
MENU PRINCIPALE
------------------------------------------------------------
Scegli il tipo di conversione:
  [1] Temperatura
  [2] Lunghezza
  [3] Peso
  [0] Esci dal programma

Inserisci la tua scelta (0-3): 2

============================================================
  CONVERSIONI LUNGHEZZA
============================================================
Scegli la conversione desiderata:
  [1] Metri -> Piedi
  [2] Piedi -> Metri
  [3] Metri -> Chilometri
  [4] Chilometri -> Metri
  [5] Metri -> Miglia
  [6] Miglia -> Metri

Inserisci il numero della conversione (1-6): 5
Inserisci il valore da convertire: 1000

[OK] 1000.0000 metri = 0.6214 miglia
```

#### ESEMPIO 3: Conversione Peso (Chilogrammi -> Libbre)

Convertiamo 70 chilogrammi in libbre.

```
------------------------------------------------------------
MENU PRINCIPALE
------------------------------------------------------------
Scegli il tipo di conversione:
  [1] Temperatura
  [2] Lunghezza
  [3] Peso
  [0] Esci dal programma

Inserisci la tua scelta (0-3): 3

============================================================
  CONVERSIONI PESO
============================================================
Scegli la conversione desiderata:
  [1] Chilogrammi -> Libbre
  [2] Libbre -> Chilogrammi

Inserisci il numero della conversione (1-2): 1
Inserisci il valore da convertire: 70

[OK] 70.00 chilogrammi = 154.32 libbre
```

### Funzionalità del Menu

- **Menu principale**: Scegli tra 3 categorie o esci (0)
- **Menu secondario**: Seleziona il tipo specifico di conversione
- **Input valore**: Inserisci il valore numerico da convertire
- **Validazione automatica**: Il programma controlla che l'input sia valido
- **Risultato formattato**: Visualizza il risultato con precisione appropriata
- **Conversioni multiple**: Il programma torna al menu principale dopo ogni conversione

### Gestione Errori

Il programma include una gestione errori che:

- Verifica che la scelta del menu sia valida
- Controlla che il valore inserito sia un numero
- Per il peso, verifica che il valore non sia negativo
- Mostra messaggi di errore chiari senza far crashare il programma

---

## 3. SPIEGAZIONE DEL CODICE

### Struttura del Programma

Il programma è organizzato in sezioni chiare:

```
1. Docstring iniziale e import
2. Funzioni di conversione temperatura
3. Menu temperatura
4. Funzioni di conversione lunghezza
5. Menu lunghezza
6. Funzioni di conversione peso
7. Menu peso
8. Menu principale
9. Punto di ingresso (if __name__ == "__main__")
```

### Analisi Funzione per Funzione

#### SEZIONE 1: Intestazione e Import

```python
"""
UNIT CONVERTER - Convertitore di Unità Didattico
================================================

Questo programma è stato progettato per scopo educativo.
Demonstra l'uso di funzioni, condizioni, cicli e gestione input.

Autore: Studente Python
Data: 2025
"""

import math  # Importiamo il modulo math per funzioni matematiche avanzate
```

**Spiegazione:**
- La tripla virgoletta `"""` crea una docstring che documenta il file
- `import math` importa il modulo matematico (anche se non usato direttamente, prepara il codice per estensioni future)

#### FUNZIONI DI CONVERSIONE TEMPERATURA

##### celsius_to_fahrenheit()

```python
def celsius_to_fahrenheit(celsius):
    """
    Converte Celsius in Fahrenheit.
    Formula: (C × 9/5) + 32

    Argomento:
        celsius (float): temperatura in gradi Celsius

    Ritorna:
        float: temperatura in gradi Fahrenheit
    """
    # Moltiplichiamo per 9/5 (che è 1.8) e aggiungiamo 32
    fahrenheit = (celsius * 9 / 5) + 32
    return fahrenheit
```

**Analisi dettagliata:**
1. **Definizione funzione**: `def nome(parametro):`
2. **Docstring**: Documenta cosa fa la funzione, i parametri e il valore di ritorno
3. **Variabile locale**: `fahrenheit` è calcolata e poi ritornata
4. **Return**: Restituisce il risultato al chiamante

**Uso tipico:**
```python
risultato = celsius_to_fahrenheit(25)
print(risultato)  # Output: 77.0
```

##### fahrenheit_to_kelvin() - Funzione Composta

```python
def fahrenheit_to_kelvin(fahrenheit):
    """
    Converte Fahrenheit in Kelvin.
    Formula: (F - 32) × 5/9 + 273.15
    """
    kelvin = (fahrenheit - 32) * 5 / 9 + 273.15
    return kelvin
```

**Nota importante:**
Questa funzione dimostra come combinare più passaggi in una sola espressione. Sottrae 32, moltiplica per 5/9, e aggiunge 273.15, combinando due conversioni (F->C e C->K).

#### FUNZIONI DI CONVERSIONE LUNGHEZZA

##### metri_to_piedi()

```python
def metri_to_piedi(metri):
    """
    Converte metri in piedi.
    Formula: metri × 3.28084
    """
    piedi = metri * 3.28084
    return piedi
```

**Struttura simile** a tutte le funzioni di conversione:
1. Prende un parametro (il valore da convertire)
2. Applica la formula di conversione
3. Salva il risultato in una variabile locale
4. Restituisce il risultato con `return`

##### metri_to_chilometri() - Conversione Semplice

```python
def metri_to_chilometri(metri):
    """
    Converte metri in chilometri.
    Formula: metri × 0.001
    """
    # Dividiamo per 1000 (moltiplicare per 0.001 è equivalente)
    chilometri = metri * 0.001
    return chilometri
```

**Nota sul commento:**
Il commento spiega che moltiplicare per 0.001 è equivalente a dividere per 1000. Questo aiuta a capire perché usiamo 0.001 invece di 1000.

#### FUNZIONI DI CONVERSIONE PESO

##### chilogrammi_to_libbre()

```python
def chilogrammi_to_libbre(chilogrammi):
    """
    Converte chilogrammi in libbre.
    Formula: kg × 2.20462
    """
    libbre = chilogrammi * 2.20462
    return libbre
```

#### FUNZIONI MENU

Tutte le funzioni menu (`menu_temperature()`, `menu_lunghezza()`, `menu_peso()`) seguono la stessa struttura:

##### Struttura Generale di un Menu

```python
def menu_categoria():
    # 1. Stampa il menu con le opzioni
    print("\n" + "=" * 60)
    print("  TITOLO DEL MENU")
    print("=" * 60)
    print("Scegli la conversione desiderata:")
    print("  [1] Opzione 1")
    print("  [2] Opzione 2")
    # ... altre opzioni

    # 2. Ottieni la scelta dell'utente
    scelta = input("\nInserisci il numero: ").strip()

    # 3. Valida la scelta
    if scelta not in ['1', '2', ...]:
        print("[!] Scelta non valida.")
        return

    # 4. Ottieni il valore da convertire
    try:
        valore = float(input("Inserisci il valore: "))
    except ValueError:
        print("[!] Errore: devi inserire un numero valido.")
        return

    # 5. Esegui la conversione appropriata
    if scelta == '1':
        risultato = funzione_conversione_1(valore)
        print(f"\n[OK] {valore:.2f} unità1 = {risultato:.2f} unità2")
    elif scelta == '2':
        risultato = funzione_conversione_2(valore)
        print(f"\n[OK] {valore:.2f} unità2 = {risultato:.2f} unità1")
    # ... altre opzioni
```

**Elementi chiave:**

1. **`.strip()`**: Rimuove spazi all'inizio e alla fine dell'input
   ```python
   input = "  1  "
   input.strip()  # "1"
   ```

2. **Validazione con `not in`**:
   ```python
   if scelta not in ['1', '2', '3']:
       # La scelta non è valida
   ```

3. **Gestione errori con `try/except`**:
   ```python
   try:
       valore = float(input("..."))
   except ValueError:
       # Si esegue se float() fallisce
       print("Errore!")
   ```

4. **Formattazione output con f-strings**:
   ```python
   print(f"{valore:.2f}")  # 2 decimali
   print(f"{valore:.4f}")  # 4 decimali
   ```

##### menu_peso() - Validazione Aggiuntiva

```python
def menu_peso():
    # ... (codice menu precedente)

    # Verifichiamo che il peso sia positivo
    if valore < 0:
        print("[!] Attenzione: il peso non può essere negativo.")
        return
```

**Nota importante:**
Questa funzione include una validazione aggiuntiva specifica per il peso, che non può essere negativo. Questo dimostra come aggiungere controlli specifici per diversi tipi di dati.

#### FUNZIONE PRINCIPALE

##### menu_principale()

```python
def menu_principale():
    """
    Funzione principale che gestisce il ciclo del programma.
    Mostra il menu principale e continua finché l'utente non sceglie di uscire.
    """
    # Messaggio di benvenuto
    print("\n" + "=" * 60)
    print("  UNIT CONVERTER - Convertitore di Unità")
    print("=" * 60)
    print("  Programma didattico per imparare Python")
    print("=" * 60)

    # Ciclo principale del programma
    while True:
        print("\n" + "-" * 60)
        print("MENU PRINCIPALE")
        print("-" * 60)
        print("Scegli il tipo di conversione:")
        print("  [1] Temperatura")
        print("  [2] Lunghezza")
        print("  [3] Peso")
        print("  [0] Esci dal programma")

        scelta = input("\nInserisci la tua scelta (0-3): ").strip()

        if scelta == '1':
            menu_temperature()
        elif scelta == '2':
            menu_lunghezza()
        elif scelta == '3':
            menu_peso()
        elif scelta == '0':
            print("\nGrazie per aver usato Unit Converter!")
            print("Alla prossima!")
            break  # Esce dal ciclo while
        else:
            print("\n[!] Scelta non valida.")
```

**Concetti chiave:**

1. **`while True`**: Ciclo infinito che continua finché non incontriamo `break`
   ```python
   while True:
       # Codice che si ripete all'infinito
       if condizione_uscita:
           break  # Esce dal ciclo
   ```

2. **`break`**: Esce immediatamente dal ciclo
   ```python
   while True:
       scelta = input("0 per uscire: ")
       if scelta == '0':
           break  # Esce dal while
   ```

3. **Chiamata funzioni**: Il menu principale chiama altri menu
   ```python
   if scelta == '1':
       menu_temperature()  # Chiama la funzione del menu temperatura
   ```

#### PUNTO DI INGRESSO

```python
if __name__ == "__main__":
    """
    __name__ è una variabile speciale di Python.
    Quando eseguiamo direttamente questo file, __name__ è "__main__".
    Se importassimo questo file in un altro programma, questo codice non verrebbe eseguito.
    """
    menu_principale()
```

**Spiegazione di `if __name__ == "__main__"`:**

Questa è una convenzione Python importante:

- Quando esegui direttamente il file: `python unit_converter.py`
  - `__name__` = `"__main__"`
  - Il codice sotto l'if viene eseguito

- Quando importi il file in altro codice: `import unit_converter`
  - `__name__` = `"unit_converter"`
  - Il codice sotto l'if NON viene eseguito

**Vantaggi:**
- Permette di importare le funzioni senza eseguire il programma
- Separa la definizione delle funzioni dall'esecuzione
- Rende il modulo riutilizzabile

---

## 4. FORMULE DI CONVERSIONE

### Temperature

#### Da Celsius a Fahrenheit
```
°F = (°C × 9/5) + 32
```

**Spiegazione:**
- Moltiplichiamo per 9/5 (ovvero 1.8)
- Aggiungiamo 32 (punto di congelamento dell'acqua in °F)

**Perché questa formula?**
- L'intervallo tra congelamento (0°C) ed ebollizione (100°C) dell'acqua è 100 gradi Celsius
- In Fahrenheit è 32°F - 212°F = 180 gradi
- Quindi 100°C = 180°F, ovvero 1°C = 1.8°F
- L'acqua congela a 32°F, quindi aggiungiamo questo offset

**Esempio:**
```
25°C = (25 × 9/5) + 32 = 45 + 32 = 77°F
```

#### Da Fahrenheit a Celsius
```
°C = (°F - 32) × 5/9
```

**Spiegazione:**
- Sottraiamo 32 (rimuoviamo l'offset)
- Moltiplichiamo per 5/9 (ovvero circa 0.556)

**Esempio:**
```
77°F = (77 - 32) × 5/9 = 45 × 0.556 = 25°C
```

#### Da Celsius a Kelvin
```
K = °C + 273.15
```

**Spiegazione:**
- Semplice addizione dell'offset assoluto
- 0 Kelvin = zero assoluto (-273.15°C)
- Lo zero assoluto è la temperatura più bassa teoricamente possibile

**Esempio:**
```
25°C = 25 + 273.15 = 298.15K
```

#### Da Kelvin a Celsius
```
°C = K - 273.15
```

**Esempio:**
```
298.15K = 298.15 - 273.15 = 25°C
```

#### Da Fahrenheit a Kelvin (Formula Combinata)
```
K = (°F - 32) × 5/9 + 273.15
```

**Spiegazione:**
- Prima convertiamo Fahrenheit in Celsius: (°F - 32) × 5/9
- Poi convertiamo Celsius in Kelvin: + 273.15
- Combiniamo le due formule in una sola espressione

**Esempio:**
```
77°F = (77 - 32) × 5/9 + 273.15 = 25 + 273.15 = 298.15K
```

#### Da Kelvin a Fahrenheit (Formula Combinata)
```
°F = (K - 273.15) × 9/5 + 32
```

**Esempio:**
```
298.15K = (298.15 - 273.15) × 9/5 + 32 = 45 + 32 = 77°F
```

### Lunghezza

#### Da Metri a Piedi
```
ft = m × 3.28084
```

**Spiegazione:**
- 1 piede (foot) = 0.3048 metri (definizione esatta)
- 1 metro = 1/0.3048 = 3.28084 piedi

**Origine:**
- Il piede era originariamente basato sulla lunghezza del piede umano
- Ora è definito esattamente come 0.3048 metri

**Esempio:**
```
5 metri = 5 × 3.28084 = 16.4042 piedi
```

#### Da Piedi a Metri
```
m = ft × 0.3048
```

**Esempio:**
```
10 piedi = 10 × 0.3048 = 3.048 metri
```

#### Da Metri a Chilometri
```
km = m × 0.001
```

**Spiegazione:**
- "Kilo" significa 1000 in greco
- 1 chilometro = 1000 metri
- Quindi 1 metro = 0.001 chilometri

**Esempio:**
```
5000 metri = 5000 × 0.001 = 5 chilometri
```

#### Da Chilometri a Metri
```
m = km × 1000
```

**Esempio:**
```
5.5 chilometri = 5.5 × 1000 = 5500 metri
```

#### Da Metri a Miglia
```
mi = m × 0.000621371
```

**Spiegazione:**
- 1 miglio (statunitense) = 1609.344 metri (definizione esatta)
- 1 metro = 1/1609.344 = 0.000621371 miglia

**Origine:**
- La miglia deriva dal "mille passus" romano (mille passi)
- 1 miglio = 5280 piedi

**Esempio:**
```
1000 metri = 1000 × 0.000621371 = 0.6214 miglia
```

#### Da Miglia a Metri
```
m = mi × 1609.34
```

**Esempio:**
```
10 miglia = 10 × 1609.34 = 16093.4 metri (circa 16 km)
```

### Peso

#### Da Chilogrammi a Libbre
```
lb = kg × 2.20462
```

**Spiegazione:**
- 1 libbra (pound) = 0.45359237 kg (definizione esatta internazionale)
- 1 kg = 1/0.45359237 = 2.20462 libbre

**Origine:**
- La libbra deriva dal peso di vari cereali
- Esistono diverse varianti (libbra avoirdupois, troy, etc.)
- Quella usata qui è la libbra avoirdupois internazionale

**Esempio:**
```
70 kg = 70 × 2.20462 = 154.3234 libbre
```

#### Da Libbre a Chilogrammi
```
kg = lb × 0.453592
```

**Esempio:**
```
154 libbre = 154 × 0.453592 = 69.8532 kg
```

### Tabella di Riepilogo

| Categoria | Da | A | Formula | Esempio |
|-----------|-----|---|---------|---------|
| Temperatura | Celsius | Fahrenheit | (C × 9/5) + 32 | 25°C = 77°F |
| Temperatura | Fahrenheit | Celsius | (F - 32) × 5/9 | 77°F = 25°C |
| Temperatura | Celsius | Kelvin | C + 273.15 | 25°C = 298.15K |
| Temperatura | Kelvin | Celsius | K - 273.15 | 298.15K = 25°C |
| Temperatura | Fahrenheit | Kelvin | (F - 32) × 5/9 + 273.15 | 77°F = 298.15K |
| Temperatura | Kelvin | Fahrenheit | (K - 273.15) × 9/5 + 32 | 298.15K = 77°F |
| Lunghezza | Metri | Piedi | m × 3.28084 | 5 m = 16.4042 ft |
| Lunghezza | Piedi | Metri | ft × 0.3048 | 10 ft = 3.048 m |
| Lunghezza | Metri | Chilometri | m × 0.001 | 5000 m = 5 km |
| Lunghezza | Chilometri | Metri | km × 1000 | 5.5 km = 5500 m |
| Lunghezza | Metri | Miglia | m × 0.000621371 | 1000 m = 0.6214 mi |
| Lunghezza | Miglia | Metri | mi × 1609.34 | 10 mi = 16093.4 m |
| Peso | Chilogrammi | Libbre | kg × 2.20462 | 70 kg = 154.32 lb |
| Peso | Libbre | Chilogrammi | lb × 0.453592 | 154 lb = 69.85 kg |

---

## 5. CONCETTI PYTHON UTILIZZATI

### Funzioni

Le funzioni sono blocchi di codice riutilizzabili che eseguono un compito specifico.

**Sintassi:**
```python
def nome_funzione(parametro1, parametro2):
    """Docstring opzionale che spiega cosa fa."""
    # Codice della funzione
    risultato = calcolo_qualcosa(parametro1, parametro2)
    return risultato
```

**Componenti:**
1. `def`: Parola chiave per definire una funzione
2. `nome_funzione`: Nome descrittivo (snake_case)
3. `parametri`: Dati di input (opzionali)
4. `return`: Restituisce il risultato (opzionale)

**Perché usare funzioni?**
- **Riutilizzabilità**: Scrivi una volta, usi molte volte
- **Organizzazione**: Dividi il problema in parti più piccole
- **Leggibilità**: Codice più facile da capire e mantenere
- **Testing**: Più facile testare funzioni singole

**Esempio dal progetto:**
```python
def chilogrammi_to_libbre(chilogrammi):
    """Converte chilogrammi in libbre."""
    libbre = chilogrammi * 2.20462
    return libbre

# Puoi chiamarla più volte
print(chilogrammi_to_libbre(70))  # 154.3234
print(chilogrammi_to_libbre(50))  # 110.231
print(chilogrammi_to_libbre(100)) # 220.462
```

**Tipi di funzioni nel progetto:**

1. **Funzioni di conversione**: Prendono un valore, restituiscono il convertito
   ```python
   def celsius_to_fahrenheit(celsius):
       return (celsius * 9 / 5) + 32
   ```

2. **Funzioni menu**: Gestiscono l'interfaccia utente, non restituiscono nulla
   ```python
   def menu_temperature():
       # Stampa menu, ottiene input, stampa risultato
       # Nessun return (implicitamente return None)
   ```

### Input/Output

#### Output con print()

La funzione `print()` visualizza testo nella console.

```python
print("Testo semplice")
print("Valore variabile:", variabile)
print(f"Valore formattato: {variabile:.2f}")
```

**Metodi di formattazione stringa:**

1. **f-strings (moderno, consigliato)**:
   ```python
   nome = "Mario"
   eta = 25
   print(f"Ciao, sono {nome} e ho {eta} anni.")
   # Output: Ciao, sono Mario e ho 25 anni.
   ```

2. **Moltiplicazione stringa**:
   ```python
   print("=" * 60)
   # Output: ============================================================
   ```

3. **Carattere newline**:
   ```python
   print("\nQuesto va a capo prima")
   print("Questo\nva\na\ncapo\npiù\nvolte")
   ```

4. **Formattazione numeri**:
   ```python
   numero = 123.456789
   print(f"{numero:.2f}")  # 123.46 (2 decimali, arrotondato)
   print(f"{numero:.4f}")  # 123.4568 (4 decimali)
   print(f"{numero:.0f}")  # 123 (nessun decimale)
   ```

#### Input con input()

La funzione `input()` ottiene testo dall'utente.

```python
valore = input("Prompt: ")  # Restituisce sempre una stringa
```

**Conversione tipi:**
```python
# Da stringa a intero
intero = int(input("Inserisci un intero: "))

# Da stringa a decimale
decimale = float(input("Inserisci un decimale: "))
```

**Metodo .strip():**
```python
input_utente = "  1  "
input_utente = input_utente.strip()  # "1"
input_utente = input("...").strip()  # Stessa cosa in una riga
```

### Condizionali

Permettono di eseguire codice solo se una condizione è vera.

**Sintassi:**
```python
if condizione1:
    # Codice se condizione1 è vera
elif condizione2:
    # Codice se condizione1 è falsa E condizione2 è vera
else:
    # Codice se tutte le condizioni precedenti sono false
```

**Operatori di confronto:**
| Operatore | Significato | Esempio |
|-----------|-------------|---------|
| `==` | Uguale | `a == b` |
| `!=` | Diverso | `a != b` |
| `<` | Minore di | `a < b` |
| `>` | Maggiore di | `a > b` |
| `<=` | Minore o uguale | `a <= b` |
| `>=` | Maggiore o uguale | `a >= b` |

**Operatori di appartenenza:**
| Operatore | Significato | Esempio |
|-----------|-------------|---------|
| `in` | Contenuto in | `scelta in ['1', '2', '3']` |
| `not in` | Non contenuto in | `scelta not in ['1', '2', '3']` |

**Esempio dal progetto:**
```python
scelta = input("Inserisci la tua scelta (0-3): ").strip()

if scelta == '1':
    menu_temperature()
elif scelta == '2':
    menu_lunghezza()
elif scelta == '3':
    menu_peso()
elif scelta == '0':
    print("Arrivederci!")
    break
else:
    print("Scelta non valida.")
```

**Esempio con not in:**
```python
if scelta not in ['1', '2', '3', '4', '5', '6']:
    print("[!] Scelta non valida. Torna al menu principale.")
    return
```

### Cicli

Permettono di ripetere codice più volte.

#### While Loop

Il ciclo `while` continua finché la condizione è vera.

```python
while condizione:
    # Codice ripetuto finché condizione è vera
```

**Ciclo infinito con break:**
```python
while True:  # True è sempre vero
    # Codice che si ripete all'infinito
    risposta = input("Continuare? (s/n): ")
    if risposta == 'n':
        break  # Esce dal ciclo
```

**Istruzioni di controllo:**
- `break`: Esce completamente dal ciclo
- `continue`: Salta alla prossima iterazione

**Esempio dal progetto:**
```python
def menu_principale():
    # ... setup ...

    while True:
        # Mostra menu
        scelta = input("...")

        if scelta == '0':
            print("Arrivederci!")
            break  # Esce dal while True

        # ... altre scelte ...
```

**Esempio con continue:**
```python
while True:
    input_utente = input("Inserisci un numero positivo: ")
    numero = float(input_utente)

    if numero < 0:
        print("Numero negativo, riprova.")
        continue  # Torna all'inizio del while

    # Questo codice si esegue solo se numero >= 0
    print(f"Hai inserito {numero}")
    break
```

### Gestione Errori (Try/Except)

La gestione degli errori permette al programma di gestire situazioni impreviste senza crashare.

**Sintassi:**
```python
try:
    # Codice che potrebbe generare errore
    risultato = operazione_rischiosa()
except TipoErrore:
    # Codice eseguito se c'è un errore
    print("Si è verificato un errore!")
```

**Errori comuni:**

| Errore | Quando si verifica | Esempio |
|--------|-------------------|---------|
| `ValueError` | Conversione fallita | `int("ciao")` |
| `ZeroDivisionError` | Divisione per zero | `1/0` |
| `KeyError` | Chiave non presente in dizionario | `dizionario['chiave_inesistente']` |
| `IndexError` | Indice fuori range in una lista | `lista[100]` |
| `TypeError` | Operazione con tipo inappropriato | `"2" + 2` |

**Esempio dal progetto:**
```python
try:
    # Prova a convertire l'input in float
    valore = float(input("Inserisci il valore da convertire: "))
except ValueError:
    # Se l'utente inserisce testo invece di numeri
    print("[!] Errore: devi inserire un numero valido.")
    return  # Esce dalla funzione
```

**Gestione multi-errori:**
```python
try:
    risultato = operazione_complessa()
except ValueError:
    print("Valore non valido!")
except TypeError:
    print("Tipo di dato errato!")
except Exception as e:
    print(f"Errore generico: {e}")
```

### Moduli e Import

Python permette di organizzare il codice in moduli riutilizzabili.

**Importare un modulo:**
```python
import math

# Usa le funzioni del modulo
risultato = math.sqrt(25)  # 5.0
pi = math.pi  # 3.14159...
```

**Moduli comuni:**

| Modulo | Utilizzo | Funzioni comuni |
|--------|----------|-----------------|
| `math` | Funzioni matematiche | `sqrt()`, `sin()`, `cos()`, `pi` |
| `random` | Numeri casuali | `random()`, `randint()`, `choice()` |
| `datetime` | Date e orari | `datetime.now()`, `date()` |
| `json` | Gestione JSON | `load()`, `dump()` |
| `csv` | Gestione CSV | `reader()`, `writer()` |

**Nota nel progetto:**
Il modulo `math` è importato ma non usato direttamente. È preparato per estensioni future che potrebbero richiedere funzioni matematiche avanzate.

### Variabili e Tipi di Dati

**Tipi di dati base:**
```python
# Interi
eta = 25  # int

# Decimali
altezza = 1.75  # float

# Stringhe
nome = "Mario"  # str

# Booleani
 maggiorenne = True  # bool
```

**Nomi variabili:**
- Devono iniziare con una lettera o underscore
- Possono contenere lettere, numeri e underscore
- Case sensitive (`nome` != `Nome`)
- Convenzione: snake_case (`mio_nome`, non `mioNome`)

**Commenti:**
```python
# Questo è un commento su una riga

"""
Questo è un commento
su più righe (docstring)
"""
```

### Funzioni Stringa

**Metodi utili:**
```python
testo = "Ciao Mondo"

testo.lower()      # "ciao mondo" (minuscolo)
testo.upper()      # "CIAO MONDO" (maiuscolo)
testo.strip()      # Rimuove spazi inizio/fine
testo.split()      # ["Ciao", "Mondo"] (dividi in lista)
testo.center(20)   # "     Ciao Mondo     " (centra)
testo.count("a")   # Conta occorrenze
testo.replace("a", "e")  # Sostituisce caratteri
```

---

## 6. ESERCIZI PROPOSTI

### Esercizi Base

#### Esercizio 1: Aggiungere Conversione Area

Crea una nuova categoria "Area" con conversioni tra:
- Metri quadrati <-> Piedi quadrati
- Metri quadrati <-> Iarde quadrate

**Formule:**
```
1 m² = 10.7639 ft²
1 m² = 1.19599 yd²
```

**Obiettivi:**
- Capire come aggiungere una nuova categoria
- Seguire la struttura esistente del codice

**Soluzione parziale:**
```python
def metri_quadrati_to_piedi_quadrati(metri_quadrati):
    """Converte metri quadrati in piedi quadrati."""
    return metri_quadrati * 10.7639

def menu_area():
    """Mostra il menu per le conversioni di area."""
    # TODO: implementa il menu
    pass

# Aggiorna menu_principale per includere l'opzione [4] Area
```

#### Esercizio 2: Aggiungere Validazione Negative

Nel menu temperatura e lunghezza, aggiungi la validazione per verificare che il valore non sia negativo (come nel menu peso).

**Obiettivi:**
- Capire come riutilizzare la logica di validazione
- Comprendere quando la validazione è appropriata

**Soluzione:**
```python
# Nel menu_temperature(), dopo try/except
if valore < -273.15:  # Zero assoluto in Celsius
    print("[!] Attenzione: non esistono temperature sotto lo zero assoluto!")
    return

# Nel menu_lunghezza(), dopo try/except
if valore < 0:
    print("[!] Attenzione: la lunghezza non può essere negativa!")
    return
```

#### Esercizio 3: Formattazione Condizionale

Modifica i menu per formattare il risultato in modo diverso a seconda del valore.

**Obiettivi:**
- Capire come usare condizioni per la formattazione
- Migliorare l'esperienza utente

**Esempio:**
```python
# Se il risultato è molto grande o molto piccolo, usa notazione scientifica
if risultato > 10000 or risultato < 0.001:
    print(f"\n[OK] {valore:.2f} unità1 = {risultato:.2e} unità2")
else:
    print(f"\n[OK] {valore:.2f} unità1 = {risultato:.4f} unità2")
```

### Esercizi Intermedi

#### Esercizio 4: Conversione Multipla

Permetti all'utente di fare conversioni multiple consecutive nella stessa categoria senza tornare al menu principale.

**Obiettivi:**
- Capire come creare un loop secondario
- Migliorare l'usabilità del programma

**Soluzione suggerita:**
```python
def menu_temperature():
    while True:  # Loop per permettere conversioni multiple
        print("\n" + "=" * 60)
        print("  CONVERSIONI TEMPERATURA")
        # ... resto del menu ...

        # Esegui conversione...

        # Chiedi se vuole continuare
        continua = input("\nVuoi fare un'altra conversione di temperatura? (s/n): ").strip().lower()
        if continua != 's':
            break  # Torna al menu principale
```

#### Esercizio 5: Cronologia delle Conversioni

Salva le conversioni fatte durante la sessione e permetti di visualizzarle.

**Obiettivi:**
- Usare liste per memorizzare dati
- Capire come passare dati tra funzioni

**Soluzione suggerita:**
```python
# In cima al file
cronologia = []

def menu_temperature():
    # ... dopo aver calcolato il risultato ...
    entry = {
        'tipo': 'Temperatura',
        'da': 'Celsius',
        'a': 'Fahrenheit',
        'valore': valore,
        'risultato': risultato
    }
    cronologia.append(entry)
    # ... stampa risultato ...

def mostra_cronologia():
    """Mostra tutte le conversioni fatte."""
    print("\n" + "=" * 60)
    print("  CRONOLOGIA DELLE CONVERSIONI")
    print("=" * 60)
    for i, entry in enumerate(cronologia, 1):
        print(f"{i}. {entry['valore']} {entry['da']} = {entry['risultato']} {entry['a']}")

# Aggiungi opzione nel menu principale per visualizzare la cronologia
```

#### Esercizio 6: Conversione Inversa Automatica

Quando l'utente fa una conversione, proponi automaticamente l'inversa.

**Obiettivi:**
- Capire come mantenere lo stato tra conversioni
- Migliorare l'esperienza utente

**Esempio:**
```python
# Dopo la conversione Celsius -> Fahrenheit
print(f"\n[OK] {valore:.2f} gradi Celsius = {risultato:.2f} gradi Fahrenheit")

inversa = input(f"\nVuoi convertire {risultato:.2f}°F in °C? (s/n): ").lower()
if inversa == 's':
    risultato_inverso = fahrenheit_to_celsius(risultato)
    print(f"\n[OK] {risultato:.2f} gradi Fahrenheit = {risultato_inverso:.2f} gradi Celsius")
```

### Esercizi Avanzati

#### Esercizio 7: File di Configurazione

Sposta le formule di conversione in un file JSON esterno e caricalo all'avvio.

**Obiettivi:**
- Capire come leggere file esterni
- Separare configurazione dal codice
- Usare il modulo `json`

**Struttura file conversioni.json:**
```json
{
  "temperatura": {
    "c_to_f": {
      "fattore": 1.8,
      "offset": 32,
      "descrizione": "Celsius -> Fahrenheit"
    },
    "f_to_c": {
      "fattore": 0.555555556,
      "offset": -17.7777778,
      "descrizione": "Fahrenheit -> Celsius"
    }
  }
}
```

**Codice per caricare:**
```python
import json

def carica_conversioni():
    """Carica le configurazioni di conversione da file JSON."""
    try:
        with open('conversioni.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("File conversioni.json non trovato. Uso configurazione predefinita.")
        return None
```

#### Esercizio 8: Conversione Catena

Permetti all'utente di fare conversioni a catena (es. km -> m -> ft).

**Obiettivi:**
- Capire come concatenare funzioni
- Implementare logica più complessa

**Esempio:**
```python
def conversione_catena():
    """Permette conversioni multiple in sequenza."""
    print("\nModalità conversione a catena")
    print("Esempio: 1 km -> m -> ft")

    # 1. Ottieni valore e unità iniziale
    valore = float(input("Inserisci il valore: "))
    unita_partenza = input("Unità di partenza (km, m, ft, mi): ").lower()

    # 2. Sequenza di conversioni
    valore_corrente = valore
    unita_corrente = unita_partenza

    while True:
        print(f"\nValore attuale: {valore_corrente} {unita_corrente}")
        prossima_unita = input("Converti in (o 'fine' per terminare): ").lower()

        if prossima_unita == 'fine':
            break

        # Trova e esegui la conversione appropriata
        # TODO: implementa la logica di conversione

        valore_corrente = risultato
        unita_corrente = prossima_unita

    print(f"\nRisultato finale: {valore_corrente} {unita_corrente}")
```

#### Esercizio 9: Aggiungere Unit Test

Crea test per verificare che le conversioni siano corrette.

**Obiettivi:**
- Imparare il concetto di testing
- Validare il codice
- Usare l'istruzione `assert`

**Codice di test:**
```python
def test_conversioni():
    """Esegue test su tutte le funzioni di conversione."""
    print("Esecuzione test in corso...")

    # Test temperatura
    assert celsius_to_fahrenheit(0) == 32, "Errore: 0°C dovrebbe essere 32°F"
    assert celsius_to_fahrenheit(100) == 212, "Errore: 100°C dovrebbe essere 212°F"
    assert round(celsius_to_fahrenheit(25), 2) == 77, "Errore: 25°C dovrebbe essere 77°F"

    # Test lunghezza
    assert round(metri_to_piedi(1), 5) == 3.28084, "Errore: 1m dovrebbe essere 3.28084ft"
    assert round(metri_to_chilometri(1000), 1) == 1.0, "Errore: 1000m dovrebbe essere 1km"

    # Test peso
    assert round(chilogrammi_to_libbre(1), 5) == 2.20462, "Errore: 1kg dovrebbe essere 2.20462lb"

    print("Tutti i test passati!")

# Aggiungi al menu principale: [T] Esegui Test
```

#### Esercizio 10: Esportazione Risultati

Permetti di salvare le conversioni in un file di testo.

**Obiettivi:**
- Capire come scrivere su file
- Creare output formattato
- Gestire eccezioni file I/O

**Codice:**
```python
def esporta_cronologia(filename):
    """Esporta la cronologia delle conversioni su file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("CRONOLOGIA DELLE CONVERSIONI\n")
            f.write("=" * 60 + "\n\n")

            for entry in cronologia:
                f.write(f"{entry['valore']} {entry['da']} = {entry['risultato']} {entry['a']}\n")
                f.write(f"Tipo: {entry['tipo']}\n")
                f.write("-" * 40 + "\n")

        print(f"\n[OK] Cronologia esportata in {filename}")
    except IOError as e:
        print(f"\n[!] Errore durante l'esportazione: {e}")
```

### Challenge Finale: Grafici delle Conversioni

Crea una versione che genera un grafico delle conversioni più usate.

**Librerie necessarie:**
```bash
pip install matplotlib
```

**Codice esempio:**
```python
import matplotlib.pyplot as plt

def grafico_statistiche():
    """Genera un grafico delle conversioni per categoria."""
    if not cronologia:
        print("Nessuna conversione registrata.")
        return

    # Conta conversioni per categoria
    conteggi = {}
    for entry in cronologia:
        tipo = entry['tipo']
        conteggi[tipo] = conteggi.get(tipo, 0) + 1

    # Crea il grafico
    plt.figure(figsize=(10, 6))
    plt.bar(conteggi.keys(), conteggi.values(), color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    plt.title("Statistiche Conversioni per Categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Numero di Conversioni")
    plt.grid(axis='y', alpha=0.3)

    # Salva il grafico
    plt.savefig('statistiche_conversioni.png', dpi=300, bbox_inches='tight')
    print("\n[OK] Grafico salvato come 'statistiche_conversioni.png'")

    # Mostra il grafico (opzionale, richiede finestra grafica)
    # plt.show()
```

---

## CONCLUSIONI

### Cosa Hai Imparato

Attraverso questo progetto hai acquisito competenze fondamentali in Python:

1. **Strutturazione del codice**: Organizzazione in funzioni chiare e riutilizzabili
2. **Gestione dell'input**: Validazione e gestione errori dell'utente
3. **Interfacce a menu**: Creazione di CLI interattive
4. **Condizionali e cicli**: Controllo del flusso del programma
5. **Documentazione**: Uso efficace di commenti e docstring

### Prossimi Passi

Per continuare il tuo percorso Python:

1. **Classi e Oggetti**: Impara la programmazione orientata agli oggetti
2. **Moduli e Package**: Organizza codice in moduli riutilizzabili
3. **Gestione File**: Leggi e scrivi file di testo, CSV, JSON
4. **Librerie Esterne**: Scopri numpy, pandas, matplotlib
5. **Testing**: Scrivi unit test con pytest
6. **Git**: Impara il controllo di versione

### Idee per Estendere il Progetto

- Aggiungi una categoria "Velocità" (km/h, mph, nodi, m/s)
- Implementa un convertitore di valuta con tassi aggiornabili
- Crea una versione grafica con tkinter
- Aggiungi un sistema di preferiti per le conversioni usate spesso
- Implementa la conversione di date e orari tra fusi orari

### Risorse Utili

- **Documentazione Python ufficiale italiana**: https://docs.python.org/it/3/
- **Tutorial Python ufficiale**: https://docs.python.org/it/3/tutorial/
- **W3Schools Python**: https://www.w3schools.com/python/
- **Real Python**: https://realpython.com/ (in inglese)
- **Programmare in Python**: https://www.programmareinpython.it/ (italiano)

### Consigli per lo Studio

1. **Pratica regolarmente**: Scrivi codice ogni giorno, anche poco
2. **Sperimenta**: Modifica il codice esistente per capire cosa succede
3. **Leggi codice altrui**: Studia progetti open source
4. **Chiedi aiuto**: Partecipa a community e forum
5. **Insegna ad altri**: Spiegare aiuta a fissare i concetti

### Buono Studio

Congratulazioni per aver completato questo progetto. Ricorda che la programmazione si imprime praticando!

Continua a esercitarti, sperimenta con il codice e non aver paura di fare errori - è così che si impara.

---

**Autore**: Progetto didattico per studenti universitari
**Versione**: 1.0
**Data**: Febbraio 2026
**Linguaggio**: Python 3.6+
