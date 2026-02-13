# Guida Rapida al Task Manager Desktop

## Prima Esecuzione

### Passo 1: Build dell'applicazione

Doppio click su `build.bat` o esegui da terminale:

```bash
build.bat
```

Questo scaricherà le dipendenze e compilerà l'applicazione.

### Passo 2: Esecuzione

Doppio click su `run.bat` o esegui da terminale:

```bash
run.bat
```

## Utilizzo Base

### Visualizzare i Processi

1. All'avvio, vedrai la lista completa dei processi attivi
2. La lista si aggiorna automaticamente ogni 2 secondi
3. Ordina per qualsiasi colonna cliccando sull'header

### Cercare un Processo

1. Digita il nome nel campo "Filtra Processi"
2. La lista si aggiorna in tempo reale
3. Clicca "Pulisci" per rimuovere il filtro

### Terminare un Processo

1. Seleziona il processo dalla tabella
2. Clicca "Termina Processo Selezionato"
3. Conferma nella dialog
4. Il processo verrà chiuso gentilmente

### Forzare Terminazione

1. Seleziona il processo dalla tabella
2. Clicca "Forza Terminazione"
3. Conferma con attenzione (attenzione: dati persi!)
4. Il processo verrà terminato immediatamente

### Vedere i Dettagli

- **Doppio click** su un processo per vedere i dettagli
- **Click destro** per menu contestuale

### Monitorare Performance

- Il grafico a destra mostra CPU (rosso) e Memoria (blu)
- Si aggiorna ogni secondo
- Mostra gli ultimi 60 secondi

### System Tray

- **Minimizza** la finestra per andare nella tray
- **Doppio click** sull'icona per riaprire
- **Click destro** per menu (Mostra/Esci)

## Troubleshooting

### L'applicazione non parte

Verifica:
1. Java 11+ installato: `java -version`
2. Maven 3.6+ installato: `mvn -version`
3. Esegui `build.bat` prima di `run.bat`

### Impossibile terminare processi

Alcuni processi richiedono permessi elevati:
- Su Windows: esegui come Administrator
- Su Linux/Mac: esegui con sudo

### Grafico non funziona

Verifica che JFreeChart sia stato scaricato:
```bash
mvn dependency:resolve
```

## Comandi Maven Utili

```bash
# Compila senza package
mvn compile

# Compila e package
mvn package

# Esegui direttamente
mvn exec:java -Dexec.mainClass="com.taskmanager.TaskManagerApp"

# Pulisci tutto
mvn clean

# Scarica dipendenze
mvn dependency:resolve
```

## Requisiti

- **Java**: JDK 11 o superiore
- **Maven**: 3.6 o superiore
- **RAM**: 256 MB minima
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

---

Buon monitoraggio! 🚀
