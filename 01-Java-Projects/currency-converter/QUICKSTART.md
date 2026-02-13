# Quick Start - Currency Converter

Avvio rapido del Currency Converter JavaFX.

## Prerequisiti

### 1. Verifica Java
```bash
java -version
```
Deve mostrare: `java version "17.x.x"` o superiore

### 2. Verifica Maven
```bash
mvn -version
```
Deve mostrare: `Apache Maven 3.x.x`

## Installazione

### Windows
1. Apri PowerShell o Command Prompt
2. Naviga nella cartella del progetto:
   ```bash
   cd "C:\Users\matti\Desktop\Project Ideas Portfolio\01-Java-Projects\currency-converter"
   ```

### Linux/Mac
```bash
cd "C:\Users\matti\Desktop/Project Ideas Portfolio/01-Java-Projects/currency-converter"
```

## Avvio Rapido

### Opzione 1: Script (Consigliato)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

### Opzione 2: Maven
```bash
mvn clean javafx:run
```

## Prima Esecuzione

### 1. Scaricamento Dipendenze
Maven scaricherà automaticamente:
- JavaFX SDK (~50MB)
- Gson (JSON parser)
- Altre dipendenze

Tempo stimato: 1-3 minuti (dipende dalla connessione)

### 2. Compilazione
```bash
mvn clean compile
```

### 3. Esecuzione
L'applicazione si aprirà automaticamente dopo la compilazione.

## Utilizzo

### Convertire Valuta

1. **Seleziona Valuta di Partenza**
   - Menu "Da" (default: EUR)

2. **Seleziona Valuta di Destinazione**
   - Menu "A" (default: USD)

3. **Inserisci Importo**
   - Campo "Importo" (es: 100)

4. **Converti**
   - Clicca "Converti" o premi "Invio"

5. **Vedi Risultato**
   - Risultato appare nel campo "Risultato"

### Aggiornare Tassi

Clicca "🔄 Aggiorna" per:
- Recuperare tassi più recenti
- Aggiornare il grafico
- Ricaricare dall'API

### Scambiare Valute

Clicca "⇄" per:
- Invertire le valute selezionate
- Ricalcolare automaticamente (se presente un risultato)

### Visualizzare Grafico

Il grafico mostra:
- Andamento ultimi 7 giorni
- Tasso di cambio
- Aggiornamento automatico

## Funzioni Speciali

### Cache Automatica
- Durata: 1 ora
- Riduce chiamate API
- Migliora performance

### Offline Mode
- Se API non disponibile → Usa dati mock
- Applicazione sempre funzionante
- Tassi approssimativi

### Validazione
- Input controllati
- Messaggi di errore chiari
- Prevent crash

## Troubleshooting

### "JavaFX runtime components are missing"

**Soluzione:**
```bash
mvn clean javafx:run
```

### "Failed to download dependencies"

**Soluzione:**
```bash
mvn clean install -U
```

### "Port already in use"

**Soluzione:**
Nessuna azione richiesta - l'app non usa porte locali.

### Grafico non appare

**Soluzione:**
1. Verifica connessione internet
2. Clicca "🔄 Aggiorna"
3. Cambia valuta e ritorna

## Comandi Maven Utili

### Compilare
```bash
mvn clean compile
```

### Eseguire
```bash
mvn javafx:run
```

### Creare JAR
```bash
mvn clean package
```

### Pulire
```bash
mvn clean
```

### Eseguire Test (quando implementati)
```bash
mvn test
```

## File Importanti

- `pom.xml` - Configurazione Maven
- `src/main/java/com/currencyconverter/Main.java` - Entry point
- `src/main/resources/com/currencyconverter/currency_converter.fxml` - UI
- `src/main/resources/com/currencyconverter/css/style.css` - Styling

## Riferimenti

- [README.md](README.md) - Documentazione completa
- [FEATURES.md](FEATURES.md) - Funzionalità dettagliate
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architettura tecnica

## Supporto

### Console Output
Controlla la terminale per:
- Messaggi di debug
- Errori API
- Info cache

### Log
L'app usa `System.out` per logging. Vedrai:
- "Tasso recuperato dalla cache"
- "Tasso recuperato dall'API"
- "Tasso mock utilizzato"

## Prossimi Passi

1. **Personalizza**
   - Modifica `style.css` per cambiare colori
   - Aggiungi valute in `ExchangeRateService.java`

2. **Estendi**
   - Aggiungi più periodi al grafico
   - Implementa salvataggio preferiti
   - Aggiungi notifiche

3. **Distribuisci**
   - Crea JAR eseguibile
   - Condividi con altri

---

**Buon divertimento con il Currency Converter!** 💱

**Tempo totale setup**: ~5 minuti
**Difficoltà**: Principiante
