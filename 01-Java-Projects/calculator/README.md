# Calcolatrice Scientifica Java

Una calcolatrice scientifica interattiva sviluppata in Java, progettata come progetto educativo per studenti universitari principianti.

![Java](https://img.shields.io/badge/Java-17+-orange.svg)
![License](https://img.shields.io/badge/License-Educational-blue.svg)
![Level](https://img.shields.io/badge/Livello-Principiante-green.svg)

## Indice

- [Descrizione](#descrizione)
- [Funzionalita](#funzionalita)
- [Prerequisiti](#prerequisiti)
- [Installazione e Esecuzione](#installazione-ed-esecuzione)
- [Struttura del Progetto](#struttura-del-progetto)
- [Concetti Java Dimostrati](#concetti-java-dimostrati)
- [Esempi di Utilizzo](#esempi-di-utilizzo)
- [Note Educative](#note-educative)
- [Miglioramenti Futuri](#miglioramenti-futuri)

## Descrizione

Questo progetto implementa una calcolatrice scientifica completa con interfaccia a riga di comando (CLI). E stato progettato specificamente per insegnare i concetti fondamentali della programmazione Java attraverso un esempio pratico e funzionale.

### Caratteristiche Principali

- Interfaccia utente testuale semplice e intuitiva
- Gestione completa delle eccezioni
- Storico delle operazioni eseguite
- Commenti educativi dettagliati nel codice
- Codice ben strutturato e documentato

## Funzionalita

### Operazioni Base

| Operazione | Simbolo | Descrizione |
|------------|---------|-------------|
| Addizione | + | Somma di due numeri |
| Sottrazione | - | Differenza tra due numeri |
| Moltiplicazione | * | Prodotto di due numeri |
| Divisione | / | Quoziente di due numeri (con controllo divisione per zero) |

### Operazioni Scientifiche

| Operazione | Funzione | Descrizione |
|------------|----------|-------------|
| Potenza | x^y | Elevamento a potenza |
| Radice Quadrata | sqrt | Radice quadrata di un numero |
| Seno | sin | Calcolo del seno (angolo in gradi) |
| Coseno | cos | Calcolo del coseno (angolo in gradi) |
| Tangente | tan | Calcolo della tangente (angolo in gradi) |
| Logaritmo | log | Logaritmo naturale (base e) |

### Funzionalita Aggiuntive

- Storico operazioni: Visualizza tutte le operazioni eseguite durante la sessione
- Gestione errori: Messaggi chiari per input non validi ed errori matematici
- Formattazione output: Risultati con precisione appropriata

## Prerequisiti

- Java Development Kit (JDK) versione 17 o superiore
- Un ambiente di sviluppo (IDE o editor di testo)
- Terminale o prompt dei comandi

### Verifica Installazione Java

```bash
javac -version
java -version
```

## Installazione e Esecuzione

### 1. Clonazione o Download del Progetto

Il progetto si trova nella directory:
```
01-Java-Projects/calculator/
```

### 2. Compilazione

Aprire il terminale nella directory `calculator/` e eseguire:

```bash
javac ScientificCalculator.java
```

Questo creera il file `ScientificCalculator.class`.

### 3. Esecuzione

Dopo la compilazione, eseguire il programma con:

```bash
java ScientificCalculator
```

### 4. Utilizzo

Seguire le istruzioni a schermo:
1. Selezionare un'operazione digitando il numero corrispondente
2. Inserire i valori richiesti quando richiesto
3. Visualizzare il risultato
4. Le operazioni vengono salvate automaticamente nello storico
5. Selezionare "0" per uscire

## Struttura del Progetto

```
calculator/
├── ScientificCalculator.java    # Codice sorgente principale
└── README.md                    # Documentazione del progetto
```

### Componenti Principali del Codice

```java
public class ScientificCalculator {
    // Campi della classe
    private Scanner scanner;
    private ArrayList<String> history;

    // Metodi principali
    public ScientificCalculator()  // Costruttore
    public void start()             // Loop principale
    private void displayMenu()      // Visualizzazione menu

    // Metodi per operazioni
    private void performAddition()
    private void performSubtraction()
    private void performMultiplication()
    private void performDivision()
    private void performPower()
    private void performSquareRoot()
    private void performSin()
    private void performCos()
    private void performTan()
    private void performLogarithm()

    // Metodi di utilita
    private void addToHistory(String operation)
    private void displayHistory()

    // Punto di ingresso
    public static void main(String[] args)
}
```

## Concetti Java Dimostrati

### 1. Programmazione Orientata agli Oggetti (OOP)

- **Classi**: Struttura principale del programma
- **Oggetti**: Creazione e utilizzo di istanze
- **Costruttori**: Inizializzazione dello stato dell'oggetto
- **Incapsulamento**: Uso di campi `private` e metodi `public`

```java
public class ScientificCalculator {
    private Scanner scanner;  // Campo privato - incapsulamento

    public ScientificCalculator() {  // Costruttore
        // Inizializzazione
    }
}
```

### 2. Strutture di Controllo

#### Condizionali
```java
if (num2 == 0) {
    throw new ArithmeticException("Divisione per zero!");
}
```

#### Switch
```java
switch (choice) {
    case 0:
        running = false;
        break;
    case 1:
        performAddition();
        break;
    // ...
}
```

#### Loop
```java
while (running) {
    // Codice del loop
}
```

### 3. Gestione delle Eccezioni

```java
try {
    double num = scanner.nextDouble();
    if (num < 0) {
        throw new ArithmeticException("Numero negativo!");
    }
} catch (ArithmeticException e) {
    System.out.println("Errore: " + e.getMessage());
} catch (Exception e) {
    System.out.println("Errore generico: " + e.getMessage());
}
```

### 4. Collection Framework

```java
// Creazione di una ArrayList
private ArrayList<String> history = new ArrayList<>();

// Aggiunta di elementi
history.add(operation);

// Iterazione
for (int i = 0; i < history.size(); i++) {
    System.out.println(history.get(i));
}
```

### 5. Libreria Standard Java

#### Classe Math
```java
Math.pow(base, exponent)    // Potenza
Math.sqrt(number)           // Radice quadrata
Math.sin(radians)           // Seno
Math.cos(radians)           // Coseno
Math.tan(radians)           // Tangente
Math.log(number)            // Logaritmo naturale
Math.toRadians(degrees)     // Conversione gradi -> radianti
```

#### Classe Scanner
```java
Scanner scanner = new Scanner(System.in);
double num = scanner.nextDouble();
scanner.nextLine();  // Consuma il newline
scanner.close();     // Chiude lo scanner
```

### 6. Input/Output

```java
// Output
System.out.println("Messaggio con nuova riga");
System.out.print("Messaggio senza nuova riga");

// Input
Scanner scanner = new Scanner(System.in);
int choice = scanner.nextInt();
```

### 7. Metodi

```java
// Metodo privato con ritorno
private void addToHistory(String operation) {
    history.add(operation);
}

// Metodo statico main
public static void main(String[] args) {
    ScientificCalculator calc = new ScientificCalculator();
    calc.start();
}
```

## Esempi di Utilizzo

### Esempio 1: Addizione

```
Seleziona un'operazione (0-11): 1

--- ADDIZIONE ---
Inserisci il primo numero: 15
Inserisci il secondo numero: 27

Risultato: 42.0
[Operazione salvata nello storico]
```

### Esempio 2: Potenza

```
Seleziona un'operazione (0-11): 5

--- POTENZA ---
Inserisci la base: 2
Inserisci l'esponente: 10

Risultato: 1024.0
[Operazione salvata nello storico]
```

### Esempio 3: Funzioni Trigonometriche

```
Seleziona un'operazione (0-11): 7

--- SENO ---
Inserisci l'angolo in gradi: 90

Risultato: 1.0
Nota: Angolo convertito da gradi a radianti per il calcolo.
[Operazione salvata nello storico]
```

### Esempio 4: Storico Operazioni

```
Seleziona un'operazione (0-11): 11

=== STORICO OPERAZIONI ===
1. 15.00 + 27.00 = 42.00
2. 2.00 ^ 10.00 = 1024.0000
3. sin(90.00°) = 1.0000
```

### Esempio 5: Gestione Errori

```
Seleziona un'operazione (0-11): 4

--- DIVISIONE ---
Inserisci il numeratore: 10
Inserisci il denominatore: 0

Errore matematico: Divisione per zero non consentita!
```

## Note Educative

### 1. Perché ArrayList?

`ArrayList` è una collezione dinamica che cresce automaticamente quando necessario:
- Dimensione flessibile (a differenza degli array)
- Metodi convenienti per aggiungere, rimuovere e accedere agli elementi
- Ottimizzata per accesso sequenziale

### 2. Gestione dello Scanner

```java
scanner.nextLine();  // Consuma il newline dopo nextInt/nextDouble
```

Questo è necessario perché `nextInt()` e `nextDouble()` leggono solo il numero e lasciano il carattere newline nel buffer.

### 3. Conversione Gradi-Radianti

Le funzioni trigonometriche di Java (`Math.sin`, `Math.cos`, etc.) lavorano con radianti, non gradi. Ecco perché convertiamo:
```java
double radians = Math.toRadians(degrees);
```

### 4. Gestione delle Eccezioni

Il progetto dimostra due tipi di gestione errori:
- **InputMismatchException**: Input non numerico
- **ArithmeticException**: Errori matematici (divisione per zero, dominio funzioni)

### 5. String Formatting

```java
String.format("%.2f + %.2f = %.2f", num1, num2, result)
```
- `%.2f`: Formatta il numero con 2 decimali
- `%.4f`: Formatta con 4 decimali (per operazioni scientifiche)

### 6. Chiusura delle Risorse

```java
scanner.close();  // Rilascia le risorse di sistema
```

È buona pratica chiudere lo scanner quando non serve più per prevenire memory leak.

## Miglioramenti Futuri

Suggerimenti per studenti che vogliono espandere il progetto:

### Livello Principiante
- [ ] Aggiungere operazioni modulo (resto della divisione)
- [ ] Implementare valore assoluto (Math.abs)
- [ ] Aggiungere costanti matematiche (PI, E)
- [ ] Salvare lo storico in un file di testo

### Livello Intermedio
- [ ] Supporto per operazioni con parentesi
- [ ] Conversione tra unità di misura
- [ ] Calcolo di fattoriale e numeri di Fibonacci
- [ ] Implementare un sistema di memoria (M+, M-, MR, MC)

### Livello Avanzato
- [ ] Grafica con Swing o JavaFX
- [ ] Parsing di espressioni matematiche complesse
- [ ] Supporto per numeri complessi
- [ ] Creare un'interfaccia grafica con plotting di funzioni
- [ ] Implementare il pattern Strategy per le operazioni

### Best Practices da Imparare
- [ ] Scrivere unit test con JUnit
- [ ] Implementare il logging invece di System.out.println
- [ ] Applicare il pattern MVC (Model-View-Controller)
- [ ] Documentare con Javadoc completo

## Risorse per l'Apprendimento

### Documentazione Ufficiale
- [Java Documentation](https://docs.oracle.com/en/java/)
- [Math Class JavaDoc](https://docs.oracle.com/javase/17/docs/api/java.base/java/lang/Math.html)
- [ArrayList JavaDoc](https://docs.oracle.com/javase/17/docs/api/java.base/java/util/ArrayList.html)

### Tutorial Utili
- [Oracle Java Tutorials](https://docs.oracle.com/javase/tutorial/)
- [W3Schools Java](https://www.w3schools.com/java/)
- [Baeldung Java](https://www.baeldung.com/java-tutorial)

## Domande per lo Studio

1. Perché usiamo `private` per i campi della classe?
2. Qual è la differenza tra `print()` e `println()`?
3. Perché è necessario gestire le eccezioni?
4. Come funziona la conversione tra gradi e radianti?
5. Perché usiamo `ArrayList` invece di un array normale?
6. Qual è lo scopo del costruttore?
7. Perché il metodo `main` è `static`?
8. Come possiamo estendere la calcolatrice con nuove operazioni?

## Contributi

Questo è un progetto educativo. Sentiti libero di:
- Studiare il codice
- Fare modifiche
- Aggiungere funzionalità
- Condividere con altri studenti

## Licenza

Questo progetto è destinato esclusivamente a scopi educativi. Puoi liberamente utilizzarlo, modificarlo e distribuirlo per scopi di apprendimento.

---

**Autore**: Progetto Formativo
**Versione**: 1.0
**Ultimo Aggiornamento**: Febbraio 2026
**Livello**: Principiante - Universitario
**Linguaggio**: Java 17+
