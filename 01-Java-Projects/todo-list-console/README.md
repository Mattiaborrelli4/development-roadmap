# 📋 Lista Attività Console (To-Do List)

Applicazione console Java per gestire attività con priorità. Progetto educativo per studenti universitari principianti.

## 🎯 Obiettivi Didattici

Questo progetto insegna i concetti fondamentali di Java:

- **ArrayList**: Gestione dinamica di liste ordinate
- **HashMap**: Associazione chiave-valore per le priorità
- **File I/O**: Persistenza dei dati su file
- **Collections Framework**: Ordinamento e manipolazione dati
- **Stream API**: Operazioni funzionali su collezioni (Java 8+)
- **Exception Handling**: Gestione degli errori
- **Control Flow**: Cicli, condizioni e switch

## 🚀 Come Eseguire

### Prerequisiti
- Java Development Kit (JDK) 8 o superiore
- Un terminale o command prompt

### Compilazione
```bash
cd todo-list-console
javac TodoListApp.java
```

### Esecuzione
```bash
java TodoListApp
```

## 📚 Funzionalità

### 1. Aggiungi Attività
Inserisci nuove attività con priorità:
- **1** = ALTA
- **2** = MEDIA
- **3** = BASSA

### 2. Rimuovi Attività
Elimina attività esistenti selezionando il numero

### 3. Visualizza Tutte
Mostra tutte le attività in ordine di inserimento

### 4. Visualizza per Priorità
Mostra le attività ordinate dalla priorità più alta alla più bassa

### 5. Salva su File
Salva permanentemente le attività in `tasks.txt`

### 6. Esci e Salva
Esce dall'applicazione dopo aver salvato

### 7. Ricarica dal File
Ricarica le attività dal file `tasks.txt`

## 🏗️ Struttura del Codice

### Classi e Metodi Principali

```java
public class TodoListApp {
    // Strutture dati
    private static ArrayList<String> tasks;
    private static HashMap<String, Integer> priorities;

    // Metodo principale
    public static void main(String[] args)

    // Gestione attività
    private static void addTask()
    private static void removeTask()
    private static void viewTasks()
    private static void viewTasksByPriority()

    // Persistenza
    private static void saveTasksToFile()
    private static void loadTasksFromFile()

    // Utilità
    private static void displayMenu()
    private static String getPriorityLabel(int priority)
}
```

## 📖 Concetti Chiave

### ArrayList vs HashMap

**ArrayList** (`tasks`)
```java
// Mantiene l'ordine di inserimento
tasks.add("Studiare Java");
tasks.get(0);  // "Studiare Java"
tasks.remove(0);
```

**HashMap** (`priorities`)
```java
// Associa attività → priorità
priorities.put("Studiare Java", 1);
int p = priorities.get("Studiare Java");  // 1
priorities.remove("Studiare Java");
```

### File I/O

**Scrittura (BufferedWriter)**
```java
try (BufferedWriter writer = new BufferedWriter(new FileWriter("tasks.txt"))) {
    writer.write("attivita|priorita");
    writer.newLine();
}
```

**Lettura (BufferedReader)**
```java
try (BufferedReader reader = new BufferedReader(new FileReader("tasks.txt"))) {
    String line = reader.readLine();
}
```

### Stream API (Java 8+)

```java
// Ordina per priorità
List<String> sorted = tasks.stream()
    .sorted(Comparator.comparingInt(t -> priorities.get(t)))
    .collect(Collectors.toList());
```

## 📁 Formato del File

`tasks.txt`:
```
Studiare per l'esame|1
Comprare il pane|3
Chiamare il dottore|2
```

Formato: `descrizione_attività|priorità`

## 🛠️ Esempio di Utilizzo

```
===========================================
   BENVENUTO NELLA LISTA ATTIVITA'
===========================================

===========================================
                MENU PRINCIPALE
===========================================
1. Aggiungi nuova attivita'
2. Rimuovi attivita'
3. Visualizza tutte le attivita'
4. Visualizza attivita' per priorita'
5. Salva attivita' su file
6. Esci e salva
7. Ricarica attivita' dal file
===========================================

La tua scelta: 1

--- AGGIUNGI NUOVA ATTIVITA' ---
Descrizione attivita': Studiare per l'esame di Java
Priorita' (1=ALTA, 2=MEDIA, 3=BASSA): 1

[OK] Attivita' aggiunta con successo!
    Attivita': Studiare per l'esame di Java
    Priorita': ALTA
```

## 🎓 Suggerimenti per lo Studio

1. **Modifica il codice**: Aggiungi funzionalità come categorie o date
2. **Sperimenta**: Prova altri tipi di Set e Map
3. **Debug**: Usa un debugger per capire il flusso
4. **Documentazione**: Consulta la documentazione Oracle Java

## 🔍 Estensioni Possibili

- [ ] Aggiungere date di scadenza
- [ ] Implementare filtri per categoria
- [ ] Aggiungere ricerca di attività
- [ ] Creare statistiche (attività completate)
- [ ] Implementare il marcare come completato
- [ ] Aggiungere import/export CSV

## 📝 Note per l'Insegnante

Questo progetto è progettato per:
- Studenti del primo anno di corso universitario
- Durata stimata: 2-3 ore di lavoro
- Prerequisiti: Concetti base di programmazione

Punti di insegnamento chiave:
1. Strutture dati del Collection Framework
2. Gestione file in Java
3. Programmazione orientata agli oggetti di base
4. Gestione eccezioni
5. Best practice (try-with-resources)

## 📜 Licenza

Progetto educativo - Libero utilizzo per scopi didattici.

---

**Creato per studenti universitari** 🎓
