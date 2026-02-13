# 📚 Guida Completa per Studenti

## 🎯 Indice

1. [Introduzione](#introduzione)
2. [Setup dell'Ambiente](#setup-dellambiente)
3. [Compilazione ed Esecuzione](#compilazione-ed-esecuzione)
4. [Analisi del Codice](#analisi-del-codice)
5. [Concetti Fondamentali](#concetti-fondamentali)
6. [Esercizi Pratici](#esercizi-pratici)
7. [Risoluzione Problemi](#risoluzione-problemi)

---

## 📖 Introduzione

Benvenuto nel progetto **TodoListApp**! Questa applicazione console ti aiuterà a comprendere i concetti fondamentali della programmazione Java.

### Cosa Imparerai

- ✅ Utilizzo di `ArrayList` e `HashMap`
- ✅ Gestione file (lettura e scrittura)
- ✅ Programmazione orientata agli oggetti di base
- ✅ Gestione degli errori con eccezioni
- ✅ Stream API di Java 8
- ✅ Best practice di programmazione

---

## 🛠️ Setup dell'Ambiente

### 1. Installare Java

**Windows:**
1. Scarica JDK da: https://www.oracle.com/java/technologies/downloads/
2. Installa seguendo la procedura guidata
3. Verifica con: `java -version`

**macOS:**
```bash
# Usando Homebrew
brew install openjdk
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install default-jdk
```

### 2. Verifica l'Installazione

Apri il terminale e digita:
```bash
java -version
javac -version
```

Dovresti vedere qualcosa come:
```
java version "17.0.1"
javac 17.0.1
```

---

## ▶️ Compilazione ed Esecuzione

### Metodo 1: Script Automatico

**Windows:**
```bash
run.bat
```

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

### Metodo 2: Comandi Manuali

```bash
# 1. Vai nella directory del progetto
cd todo-list-console

# 2. Compila il file Java
javac TodoListApp.java

# 3. Esegui l'applicazione
java TodoListApp
```

### Compilazione Dettagliata

```bash
# Compilazione con warning dettagliati
javac -Xlint:unchecked TodoListApp.java

# Compilazione con encoding specifico
javac -encoding UTF-8 TodoListApp.java

# Esecuzione con memoria aumentata (se necessario)
java -Xmx512m TodoListApp
```

---

## 🔍 Analisi del Codice

### Struttura del File

```java
import java.io.*;           // Per File I/O
import java.util.*;         // Per ArrayList, HashMap, Scanner
import java.util.stream.*;  // Per Stream API

public class TodoListApp {
    // Variabili statiche (globali per la classe)
    private static ArrayList<String> tasks;
    private static HashMap<String, Integer> priorities;
    private static Scanner scanner;

    // Metodo principale
    public static void main(String[] args) { ... }

    // Metodi di supporto
    private static void addTask() { ... }
    private static void removeTask() { ... }
    // ... altri metodi
}
```

### Spiegazione dei Componenti

#### 1. Import

```java
import java.io.*;
```
Importa tutte le classi del package `java.io` per input/output:
- `File`: Rappresenta un file sul filesystem
- `FileReader`: Legge caratteri da un file
- `FileWriter`: Scrive caratteri su un file
- `BufferedReader`: Legge testo con buffer (più veloce)
- `BufferedWriter`: Scrive testo con buffer (più veloce)
- `IOException`: Eccezione per errori I/O

```java
import java.util.*;
```
Importa le classi del framework Collections:
- `ArrayList`: Lista dinamica ridimensionabile
- `HashMap`: Mappa chiave-valore
- `Scanner`: Parsing dell'input
- `List`: Interfaccia per liste
- `Comparator`: Per ordinamento personalizzato

#### 2. Variabili Statiche

```java
private static ArrayList<String> tasks = new ArrayList<>();
```
- `private`: Accessibile solo dentro questa classe
- `static`: Condivisa tra tutte le istanze (una sola copia)
- `ArrayList<String>`: Lista che contiene solo String
- `new ArrayList<>()`: Crea una nuova lista vuota

```java
private static HashMap<String, Integer> priorities = new HashMap<>();
```
- `HashMap<String, Integer>`: Mappa String → Integer
- Chiave: nome attività (String)
- Valore: priorità (Integer)

#### 3. Metodo Main

```java
public static void main(String[] args) {
    // Punto di ingresso dell'applicazione
    // args: argomenti da linea di comando
}
```

---

## 🎓 Concetti Fondamentali

### ArrayList

**Cos'è:** Un array ridimensionabile che può crescere dinamicamente.

**Operazioni Comuni:**

```java
// Creazione
ArrayList<String> lista = new ArrayList<>();

// Aggiungere elementi
lista.add("Primo");
lista.add("Secondo");

// Accedere a un elemento
String elemento = lista.get(0); // "Primo"

// Dimensione
int dimensione = lista.size(); // 2

// Rimuovere un elemento
lista.remove(0); // Rimuove "Primo"

// Verificare se contiene
boolean presente = lista.contains("Secondo"); // true

// Iterare
for (String s : lista) {
    System.out.println(s);
}
```

**Quando usarlo:**
- Quando hai bisogno di una lista ordinata
- Quando il numero di elementi cambia spesso
- Quando devi accedere rapidamente per indice

### HashMap

**Cos'è:** Una collezione che mappa chiavi a valori.

**Operazioni Comuni:**

```java
// Creazione
HashMap<String, Integer> mappa = new HashMap<>();

// Aggiungere coppie chiave-valore
mappa.put("Mario", 25);
mappa.put("Luigi", 30);

// Recuperare un valore
int eta = mappa.get("Mario"); // 25

// Verificare se contiene chiave
boolean haMario = mappa.containsKey("Mario"); // true

// Verificare se contiene valore
boolean ha25 = mappa.containsValue(25); // true

// Rimuovere
mappa.remove("Mario");

// Dimensione
int dimensione = mappa.size(); // 1

// Iterare
for (String chiave : mappa.keySet()) {
    int valore = mappa.get(chiave);
    System.out.println(chiave + ": " + valore);
}
```

**Quando usarlo:**
- Per associare dati (es. nome → età)
- Per lookup veloci per chiave
- Quando non ti importa dell'ordine

### File I/O

**Lettura da File:**

```java
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    System.err.println("Errore: " + e.getMessage());
}
```

**Scrittura su File:**

```java
try (BufferedWriter writer = new BufferedWriter(new FileWriter("file.txt"))) {
    writer.write("Prima riga");
    writer.newLine();
    writer.write("Seconda riga");
} catch (IOException e) {
    System.err.println("Errore: " + e.getMessage());
}
```

**Try-with-resources:**
- Chiude automaticamente il file
- Introdotto in Java 7
- Previene memory leak

### Stream API (Java 8+)

**Cos'è:** Modo funzionale di processare collezioni.

**Esempio Base:**

```java
List<String> lista = Arrays.asList("mela", "banana", "kiwi");

// Filtra e trasforma
List<String> risultato = lista.stream()
    .filter(s -> s.length() > 4)      // Solo stringhe > 4 caratteri
    .map(String::toUpperCase)         // Converti in maiuscolo
    .sorted()                          // Ordina alfabeticamente
    .collect(Collectors.toList());    // Raccogli in una List

// Risultato: ["BANANA", "MELA"]
```

**Nel Nostro Codice:**

```java
List<String> sortedTasks = tasks.stream()
    .sorted(Comparator.comparingInt(t -> priorities.get(t)))
    .collect(Collectors.toList());
```

Questo ordina le attività per priorità (dal valore più basso al più alto).

### Exception Handling

**Try-Catch:**

```java
try {
    // Codice che potrebbe generare eccezioni
    int risultato = 10 / 0;
} catch (ArithmeticException e) {
    // Gestione dell'eccezione
    System.out.println("Errore di divisione!");
} finally {
    // Eseguito sempre
    System.out.println("Pulizia...");
}
```

**Tipi di Eccezioni:**

- `IOException`: Errori di input/output
- `FileNotFoundException`: File non trovato
- `NumberFormatException`: Stringa non è un numero
- `InputMismatchException`: Input non corrisponde al tipo atteso

---

## ✏️ Esercizi Pratici

### Esercizio 1: Aggiungere una Categoria

**Obiettivo:** Aggiungi una categoria a ogni attività.

**Suggerimento:**
```java
// Modifica le strutture dati
private static HashMap<String, String> categories = new HashMap<>();

// Nel metodo addTask()
System.out.print("Categoria (STUDIO, LAVORO, PERSONALE): ");
String category = scanner.nextLine();
categories.put(task, category);
```

### Esercizio 2: Implementa "Completa Attività"

**Obiettivo:** Permetti di segnare un'attività come completata.

```java
private static void completeTask() {
    // Implementa questo metodo
}
```

### Esercizio 3: Statistiche

**Obiettivo:** Mostra quante attività ci sono per priorità.

```java
private static void showStatistics() {
    // Conta attività ALTA, MEDIA, BASSA
}
```

### Esercizio 4: Ricerca

**Obiettivo:** Cerca attività per parola chiave.

```java
private static void searchTasks(String keyword) {
    // Filtra e mostra attività che contengono la keyword
}
```

### Esercizio 5: Modifica Priorità

**Obiettivo:** Permetti di cambiare la priorità di un'attività esistente.

```java
private static void updatePriority() {
    // Implementa questo metodo
}
```

---

## 🐛 Risoluzione Problemi

### Problema: "javac non è riconosciuto"

**Soluzione:**
1. Verifica che Java sia installato: `java -version`
2. Aggiungi Java al PATH di sistema
3. Riavvia il terminale

### Problema: "Compilation error"

**Soluzione:**
```bash
# Compila con dettagli
javac -Xlint:all TodoListApp.java

# Verifica encoding
javac -encoding UTF-8 TodoListApp.java
```

### Problema: "NoSuchElementException"

**Causa:** Scanner consuma input non volutamente.

**Soluzione:**
```java
int choice = scanner.nextInt();
scanner.nextLine(); // Consuma il newline
```

### Problema: File non viene salvato

**Soluzione:**
1. Verifica permessi di scrittura
2. Controlla il percorso corrente
3. Usa path assoluti se necessario

### Problema: Caratteri strani (UTF-8)

**Soluzione:**
```bash
# Compila con encoding specifico
javac -encoding UTF-8 TodoListApp.java
```

---

## 📚 Risorse Utili

### Documentazione Ufficiale
- [Oracle Java Tutorial](https://docs.oracle.com/javase/tutorial/)
- [Java Collections Framework](https://docs.oracle.com/javase/8/docs/technotes/guides/collections/)
- [Java I/O Streams](https://docs.oracle.com/javase/tutorial/essential/io/)

### Tutorial Interattivi
- [W3Schools Java](https://www.w3schools.com/java/)
- [Baeldung Java Tutorial](https://www.baeldung.com/java-tutorial)

### Strumenti
- [Visual Studio Code](https://code.visualstudio.com/) con Extension Pack for Java
- [IntelliJ IDEA Community](https://www.jetbrains.com/idea/download/) (gratuito)

---

## 🎓 Prossimi Passi

Dopo aver completato questo progetto, studia:

1. **Programmazione Orientata agli Oggetti**
   - Classi e oggetti
   - Ereditarietà
   - Polimorfismo
   - Interfacce

2. **Java Avanzato**
   - Generics
   - Lambda Expressions
   - Optional
   - Nuove feature Java

3. **Sviluppo Applicazioni**
   - GUI con Swing o JavaFX
   - Database con JDBC
   - Sviluppo Web

---

**Buono studio e buon coding!** 🚀

*Tutti i grandi programmatori sono iniziati da qui.*
