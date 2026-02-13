# Architettura Task Manager Desktop

## Diagramma dei Package

```
com.taskmanager
│
├── TaskManagerApp.java          [Entry Point]
│   └── Main: Inizializza GUI e MonitorService
│
├── model/
│   └── ProcessInfo.java         [Data Model]
│       └── Rappresenta un processo
│
├── service/
│   └── ProcessMonitorService.java [Business Logic]
│       ├── ProcessHandle API (Java 9+)
│       ├── ScheduledExecutorService (2 thread)
│       └── Callbacks per GUI
│
└── gui/
    ├── TaskManagerFrame.java    [Main Window]
    ├── ProcessTableModel.java   [Table Adapter]
    └── PerformanceChartPanel.java [Chart Component]
```

## Flusso Dati

```
┌──────────────────────────────────────────────────────────────┐
│                    Thread Principale (EDT)                  │
│                    TaskManagerApp                          │
└────────────────────┬─────────────────────────────────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌─────────────────────────┐
│ TaskManagerFrame│    │ ProcessMonitorService    │
│   (GUI)        │◄───┤   (Background)          │
└─────────────────┘    └─────────────────────────┘
         ▲                        │
         │                        │
    ┌────┴───────────────────────┴────┐
    │                                 │
    ▼                                 ▼
┌──────────────┐           ┌────────────────────┐
│ JTable       │           │ ScheduledExecutor  │
│ Processi    │           │   Service          │
├──────────────┤           │ Thread 1: Processi │
│ Performance  │           │   (ogni 2s)       │
│ Chart       │           │ Thread 2: Perf     │
└──────────────┘           │   (ogni 1s)       │
                          └────────────────────┘
```

## Componenti Principali

### 1. TaskManagerApp (Main)
**Responsabilità:**
- Entry point dell'applicazione
- Configura Look & Feel nativo
- Inizializza servizio di monitoraggio
- Crea e mostra GUI

**Tecnologie:**
- SwingUtilities.invokeLater() per EDT safety

### 2. ProcessMonitorService (Service Layer)
**Responsabilità:**
- Monitoraggio processi con ProcessHandle API
- Aggiornamento performance CPU/Memoria
- Gestione multi-threading con ScheduledExecutorService
- Callback per notificare la GUI

**Tecnologie:**
- ProcessHandle (Java 9+)
- ScheduledExecutorService (2 thread pool)
- ManagementFactory (OS & Memory MXBean)

**Metodi Chiave:**
```java
void startMonitoring()
void stopMonitoring()
boolean killProcess(long pid)
boolean terminateProcess(long pid)
```

### 3. TaskManagerFrame (View)
**Responsabilità:**
- Finestra principale Swing
- Layout componenti UI
- Event handling user actions
- System Tray integration

**Componenti:**
- JTable per lista processi
- PerformanceChartPanel per grafici
- JTextField per filtro
- JButton per azioni
- SystemTray integration

### 4. ProcessTableModel (Adapter)
**Responsabilità:**
- Adapter tra ProcessInfo e JTable
- Gestione colonne e tipi dati
- Aggiornamento tabella

**Implementa:**
- AbstractTableModel
- 6 colonne: PID, Nome, Utente, Comando, Memoria, CPU

### 5. PerformanceChartPanel (Chart Component)
**Responsabilità:**
- Grafico real-time CPU/Memoria
- Gestione TimeSeries JFreeChart
- Limitazione data points (60s)

**Tecnologie:**
- JFreeChart 1.5.4
- TimeSeriesCollection
- TimeSeries per CPU e Memoria

### 6. ProcessInfo (Domain Model)
**Responsabilità:**
- Data class per informazioni processo
- Formattazione memoria (B/KB/MB/GB)
- Formattazione CPU percentuale

**Campi:**
```java
long pid
String name
String command
long memoryUsage
double cpuUsage
String user
```

## Threading Model

### Thread 1: EDT (Event Dispatch Thread)
- Tutte le operazioni Swing UI
- Gestione eventi utente
- Rendering GUI

### Thread 2: Process Monitor (ScheduledExecutor)
- Frequenza: Ogni 2 secondi
- Compito:
  - Query ProcessHandle.allProcesses()
  - Creazione ProcessInfo objects
  - Callback → SwingUtilities.invokeLater()

### Thread 3: Performance Monitor (ScheduledExecutor)
- Frequenza: Ogni 1 secondo
- Compito:
  - Query OS & Memory MXBean
  - Calcolo CPU/Memory usage
  - Callback → SwingUtilities.invokeLater()

## Data Flow Diagram

```
ProcessHandle.allProcesses()
         │
         ▼
createProcessInfo()
         │
         ▼
processUpdateCallback.accept(List<ProcessInfo>)
         │
         ▼
SwingUtilities.invokeLater(() -> {
    tableModel.setProcesses()
    statusLabel.setText()
})
         │
         ▼
JTable repaint()
```

## Interazione Utente

### Terminazione Processo
```
User Click "Termina"
        │
        ▼
JOptionPane Confirm
        │
        ▼
monitorService.terminateProcess(pid)
        │
        ▼
ProcessHandle.of(pid).destroy()
        │
        ▼
JOptionPane Result
```

### Filtro Processi
```
User Type Filter
        │
        ▼
DocumentListener triggered
        │
        ▼
RowFilter.regexFilter()
        │
        ▼
JTable sort/filter
```

## Performance Considerations

### Ottimizzazioni Implementate
1. **Scheduled Updates**: Non polling continuo
2. **Data Points Limit**: 60 secondi max nel grafico
3. **SwingUtilities.invokeLater**: Thread safety
4. **Lazy Table Updates**: Solo quando necessario
5. **Immutable ProcessInfo**: Thread-safe by design

### Memoria
- Stima: ~50-100 MB per 500+ processi
- Grafico: ~1 KB per data point
- JTable: ~500 bytes per row

## Security Considerations

### Permessi
- Alcuni processi richiedono admin/root
- System process protection (OS level)
- User confirmation per kill

### Validazioni
- Confirm dialog prima di azioni distruttive
- Force kill con warning aggiuntivo
- Error handling con feedback utente

## Extensibility Points

### Possibili Estensioni
1. **Plugin System**: Carica monitor aggiuntivi
2. **Custom Filters**: Salva filtri frequenti
3. **Export Data**: CSV/JSON export
4. **Notifications**: Alert per processi specifici
5. **Historical Data**: Database per trend
6. **Remote Monitoring**: RMI/HTTP client

## Dipendenze

### Runtime
```
java.desktop ( Swing, AWT )
java.management ( MXBean )
java.base ( ProcessHandle - Java 9+ )
```

### Compile
```
org.jfree:jfreechart:1.5.4
```

---

**Versione Architettura**: 1.0
**Data**: Febbraio 2026
