# ⚡ Guida Rapida - TodoListApp

## 🚀 Avvio Veloce

```bash
# Windows
run.bat

# Linux/macOS
chmod +x run.sh
./run.sh

# Manuale
javac TodoListApp.java
java TodoListApp
```

## 📋 Comandi del Menu

| # | Comando | Descrizione |
|---|---------|-------------|
| 1 | Aggiungi | Crea nuova attività con priorità (1=ALTA, 2=MEDIA, 3=BASSA) |
| 2 | Rimuovi | Elimina un'attività esistente |
| 3 | Visualizza Tutte | Mostra attività in ordine di inserimento |
| 4 | Visualizza per Priorità | Ordina dalla più alta alla più bassa |
| 5 | Salva | Scrive su `tasks.txt` |
| 6 | Esci | Salva e chiude |
| 7 | Ricarica | Legge da `tasks.txt` |

## 📁 File Generati

- **TodoListApp.class** - File compilato (generato automaticamente)
- **tasks.txt** - Database delle attività (creato al primo salvataggio)

## 🏗️ Struttura Dati

```java
// ArrayList: mantiene l'ordine di inserimento
ArrayList<String> tasks = ["Attività 1", "Attività 2", "Attività 3"];

// HashMap: associa priorità alle attività
HashMap<String, Integer> priorities = {
    "Attività 1" -> 1,  // ALTA
    "Attività 2" -> 2,  // MEDIA
    "Attività 3" -> 3   // BASSA
};
```

## 🔑 Concetti Chiave

### ArrayList
- Lista dinamica (cresce automaticamente)
- Mantiene l'ordine di inserimento
- Accesso rapido per indice: `get(i)`

### HashMap
- Mappa chiave → valore
- Lookup veloce per chiave
- Non mantiene ordine

### File I/O
- **BufferedWriter**: Scrive testo su file
- **BufferedReader**: Legge testo da file
- **try-with-resources**: Chiude automaticamente

### Stream API
```java
tasks.stream()
    .sorted(Comparator.comparingInt(t -> priorities.get(t)))
    .collect(Collectors.toList());
```
Ordina per priorità usando funzioni lambda.

## 🐛 Troubleshooting

| Problema | Soluzione |
|----------|-----------|
| `javac: command not found` | Installa Java JDK |
| `ClassNotFoundException` | Ricompila con `javac` |
| Caratteri strani | Compila con `-encoding UTF-8` |
| File non salvato | Verifica permessi directory |

## 📚 Percorso di Studio

1. ✅ Comprendi il metodo `main()`
2. ✅ Studia `ArrayList` e `HashMap`
3. ✅ Pratica con `Scanner` per input
4. ✅ Impara File I/O
5. ✅ Sperimenta con Stream API
6. ✅ Aggiungi nuove funzionalità

## 💡 Modifiche Suggerite

```java
// Aggiungi data di scadenza
private static HashMap<String, String> deadlines = new HashMap<>();

// Aggiungi categorie
private static HashMap<String, String> categories = new HashMap<>();

// Aggiungi stato completato
private static HashMap<String, Boolean> completed = new HashMap<>();
```

---

**Progetto completato?** Prova a:
1. Aggiungere filtri per categoria
2. Implementare ricerca
3. Creare statistiche
4. Aggiungere import/export CSV

🎓 **Buono studio!**
