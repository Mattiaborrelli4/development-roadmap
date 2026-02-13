# Task Manager Desktop

Applicazione Desktop Java per il monitoraggio e la gestione dei processi di sistema.

![Java Version](https://img.shields.io/badge/Java-11%2B-orange)
![Build](https://img.shields.io/badge/Maven-4.0.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Caratteristiche

### Funzionalità Principali

- **Monitoraggio Processi Real-Time**
  - Lista processi con aggiornamento automatico ogni 2 secondi
  - Visualizzazione PID, nome, utente, comando, memoria e CPU
  - Utilizzo della ProcessHandle API (Java 9+)

- **Gestione Processi**
  - Terminazione normale dei processi
  - Terminazione forzata (kill) dei processi
  - Conferma di sicurezza prima dell'azione
  - Gestione errori con feedback visivo

- **Filtri e Ricerca**
  - Filtro processi in tempo reale per nome
  - Sorting su tutte le colonne
  - Ricerca case-insensitive

- **Performance Graphs**
  - Grafico real-time CPU e Memoria
  - Powered by JFreeChart
  - Mantenimento ultimi 60 secondi di dati
  - Zoom e pan interattivi

- **System Tray Integration**
  - Icona nella system tray
  - Minimizzazione nella tray
  - Menu contestuale per azioni rapide
  - Riapertura con doppio click

- **UI Responsiva**
  - Multi-threading con ScheduledExecutorService
  - Operazioni di lunga durata in background
  - Aggiornamenti UI thread-safe con SwingUtilities.invokeLater()

## Tecnologiche Utilizzate

- **Java 11+**: Linguaggio principale
- **Swing**: Framework GUI
- **ProcessHandle API**: Monitoraggio processi (Java 9+)
- **JFreeChart**: Grafici performance
- **Maven**: Build automation
- **ScheduledExecutorService**: Threading e scheduling

## Struttura del Progetto

```
task-manager-desktop/
├── pom.xml                                    # Maven configuration
├── README.md                                  # Documentazione
└── src/main/java/com/taskmanager/
    ├── TaskManagerApp.java                    # Main entry point
    ├── model/
    │   └── ProcessInfo.java                   # Data model processo
    ├── service/
    │   └── ProcessMonitorService.java         # Servizio monitoraggio
    └── gui/
        ├── TaskManagerFrame.java              # Finestra principale
        ├── ProcessTableModel.java             # TableModel per JTable
        └── PerformanceChartPanel.java        # Pannello grafici
```

## Requisiti di Sistema

- **Java Development Kit (JDK) 11** o superiore
- **Maven 3.6+** per il build
- **Sistema Operativo**: Windows, macOS, Linux
- **Memoria**: 256 MB RAM minima
- **Spazio Disco**: 50 MB

## Installazione e Build

### 1. Clone il Repository

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\01-Java-Projects\task-manager-desktop"
```

### 2. Build con Maven

```bash
mvn clean package
```

Questo creerà il JAR eseguibile:
```
target/task-manager-desktop-1.0.0.jar
```

## Esecuzione

### Opzione 1: Esecuzione con Maven

```bash
mvn exec:java -Dexec.mainClass="com.taskmanager.TaskManagerApp"
```

### Opzione 2: Esecuzione JAR

```bash
java -jar target/task-manager-desktop-1.0.0.jar
```

### Opzione 3: Specificando classpath (dipendenze)

```bash
java -cp "target/task-manager-desktop-1.0.0.jar;target/dependency/*" com.taskmanager.TaskManagerApp
```

## Guida all'Uso

### Interfaccia Principale

L'applicazione si presenta con una finestra principale divisa in sezioni:

#### 1. Pannello Filtro (Superiore)
- Campo di testo per filtrare i processi per nome
- Il filtro è case-insensitive e si aggiorna in tempo reale
- Bottone "Pulisci" per rimuovere il filtro

#### 2. Tabella Processi (Centrale)
Colonne:
- **PID**: Identificativo univoco del processo
- **Nome**: Nome del processo
- **Utente**: Utente che ha avviato il processo
- **Comando**: Linea di comando completa
- **Memoria**: Utilizzo memoria formattato (B/KB/MB/GB)
- **CPU %**: Percentuale utilizzo CPU

Funzionalità:
- **Click singolo**: Seleziona processo
- **Doppio click**: Mostra dettagli processo
- **Click destro**: Menu contestuale azioni
- **Header colonna**: Ordinamento ascending/descending

#### 3. Azioni (Inferiore)
- **Aggiorna**: Refresh manuale della lista processi
- **Termina Processo Selezionato**: Terminazione normale (SIGTERM)
- **Forza Terminazione**: Terminazione forzata (SIGKILL)

#### 4. Performance (Destra)
- Grafico real-time CPU (linea rossa)
- Grafico real-time Memoria (linea blu)
- Asse X: tempo (ultimi 60 secondi)
- Zoom e pan con mouse

#### 5. Status Bar (Inferiore)
- Numero processi attivi (sinistra)
- Utilizzo CPU corrente (centro)
- Utilizzo Memoria corrente (destra)

### System Tray

Quando si minimizza la finestra:
- L'applicazione si riduce a icona nella system tray
- Icona blu con etichetta "TM"

Menu contestuale (click destro):
- **Mostra**: Riapre la finestra principale
- **Esci**: Termina l'applicazione

Double-click sull'icona:
- Riapre la finestra principale

### Terminazione Processi

#### Terminazione Normale
1. Selezionare il processo dalla tabella
2. Click su "Termina Processo Selezionato"
3. Confermare nella dialog box
4. Il processo riceve SIGTERM (può pulire risorse)

#### Terminazione Forzata
1. Selezionare il processo dalla tabella
2. Click su "Forza Terminazione"
3. Confermare nella dialog box (con warning)
4. Il processo riceve SIGKILL (terminazione immediata)

**Note Importanti:**
- Alcuni processi di sistema potrebbero richiedere permessi elevati
- La terminazione forzata può causare perdita di dati
- Processi critici di sistema non possono essere terminati

## Architettura Tecnica

### Threading Model

L'applicazione utilizza un approccio multi-threaded per mantenere l'UI responsiva:

```
┌─────────────────────────────────────────────┐
│           Event Dispatch Thread (EDT)       │
│         (Swing UI Operations)               │
└─────────────────────────────────────────────┘
                      ↕
┌─────────────────────────────────────────────┐
│      ScheduledExecutorService (2 threads)   │
│  Thread 1: Process Monitoring (every 2s)    │
│  Thread 2: Performance Update (every 1s)    │
└─────────────────────────────────────────────┘
```

### Componenti principali

#### ProcessMonitorService
- Gestisce il monitoraggio dei processi
- ScheduledExecutorService per aggiornamenti periodici
- Callbacks per notificare la GUI
- Metodi per terminare i processi

#### TaskManagerFrame
- Finestra principale Swing
- Gestisce tutti i componenti UI
- System Tray integration
- Event handling

#### PerformanceChartPanel
- Wrapper JFreeChart
- TimeSeries per CPU e Memoria
- Limitazione a 60 data points

#### ProcessTableModel
- AbstractTableModel per JTable
- Gestione lista ProcessInfo
- Formattazione colonne

### Sicurezza

- **Conferma obbligata** prima di terminare processi
- **Warning aggiuntivo** per terminazione forzata
- **Gestione errori** con feedback appropriato
- **Permessi elevati** necessari per alcuni processi di sistema

## Risoluzione Problemi

### Problema: "Impossibile terminare il processo"

**Cause:**
- Processo di sistema protetto
- Permessi insufficienti

**Soluzioni:**
- Eseguire l'applicazione come administrator/root
- Verificare che il processo non sia critico per il sistema

### Problema: La GUI non si aggiorna

**Cause:**
- ScheduledExecutorService non avviato
- Eccezione nel thread di monitoraggio

**Soluzioni:**
- Controllare console per errori
- Riavviare l'applicazione
- Verificare memoria disponibile

### Problema: Grafico non mostra dati

**Cause:**
- JFreeChart non nel classpath
- Eccezione nel rendering

**Soluzioni:**
- Verificare build Maven completato
- Controllare dipendenze nel classpath

## Performance e Ottimizzazioni

### Ottimizzazioni Implementate

1. **Limitazione Data Points**: Solo ultimi 60 secondi nel grafico
2. **Lazy Updates**: Aggiornamento solo ogni 1-2 secondi
3. **Table Sorting**: Native Swing sorting (ottimizzato)
4. **Thread Pool**: Riutilizzo thread per operazioni periodiche

### Suggerimenti

- Chiudere l'applicazione quando non in uso
- Evitare di filtrare su liste molto grandi
- Utilizzare terminazione normale quando possibile

## Sviluppo Futuro

Possibili miglioramenti:

- [ ] Tree view per processi padre/figlio
- [ ] Export lista processi in CSV/JSON
- [ ] Configurazione intervallo aggiornamento
- [ ] Dark mode theme
- [ ] Metriche avanzate (I/O, Network)
- [ ] Grafici storici
- [ ] Notifiche per processi specifici
- [ ] Filtri multipli (nome, utente, memoria)

## Licenza

Questo progetto è creato a scopo educativo. É libero di essere utilizzato e modificato.

## Contributi

Contributi, suggerimenti e bug report sono benvenuti!

## Autori

Progetto sviluppato come parte del portfolio di progetti Java.

---

**Versione**: 1.0.0
**Data**: Febbraio 2026
**Java**: 11+
