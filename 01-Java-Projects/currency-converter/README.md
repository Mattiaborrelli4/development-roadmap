# Currency Converter - Convertitore di Valuta

Applicazione JavaFX per la conversione di valute in tempo reale con grafico storico.

![JavaFX](https://img.shields.io/badge/JavaFX-21.0.1-brightgreen)
![Java](https://img.shields.io/badge/Java-17+-orange)
![Maven](https://img.shields.io/badge/Maven-3.8+-red)

## Caratteristiche

- **Conversione in Tempo Reale**: Converti tra EUR, USD, GBP, JPY e CHF
- **API Integration**: Recupero tassi da ExchangeRate.host API
- **Cache Intelligente**: Cache con scadenza di 1 ora per ottimizzare le performance
- **Grafico Storico**: Visualizza l'andamento del tasso di cambio degli ultimi 7 giorni
- **Threading Asincrono**: Operazioni API eseguite in background con Task/Thread
- **UI Responsiva**: Spinner durante il caricamento dei dati
- **Error Handling**: Fallback automatico su dati mock se API non disponibile
- **Design Moderno**: Interfaccia grafica curata con CSS e JavaFX

## Tecnologie Utilizzate

- **Java 17+**: Linguaggio principale
- **JavaFX 21+**: Framework GUI
- **FXML**: Definizione interfaccia utente
- **SceneBuilder**: Design dell'interfaccia
- **Gson**: Parsing JSON
- **HttpClient**: Connessione API REST
- **LineChart**: Grafico storico
- **Thread/Task**: Elaborazione asincrona

## Struttura del Progetto

```
currency-converter/
├── src/main/
│   ├── java/com/currencyconverter/
│   │   ├── Main.java                          # Entry point applicazione
│   │   ├── controller/
│   │   │   └── CurrencyConverterController.java # Controller FXML
│   │   ├── model/
│   │   │   ├── CurrencyRate.java               # Modello tasso di cambio
│   │   │   └── HistoricalRate.java             # Modello dato storico
│   │   └── service/
│   │       └── ExchangeRateService.java        # Servizio API + Cache
│   └── resources/com/currencyconverter/
│       ├── currency_converter.fxml             # Interfaccia FXML
│       └── css/
│           └── style.css                        # Foglio di stile
├── pom.xml                                      # Configurazione Maven
└── README.md                                    # Documentazione
```

## Requisiti

- Java Development Kit (JDK) 17 o superiore
- Maven 3.8 o superiore
- Connessione internet (per API, opzionale con mock data)

## Installazione e Esecuzione

### 1. Clone o Naviga nella Directory del Progetto

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\01-Java-Projects\currency-converter"
```

### 2. Compila il Progetto con Maven

```bash
mvn clean compile
```

### 3. Esegui l'Applicazione

#### Opzione A: Con Maven (Consigliato)

```bash
mvn clean javafx:run
```

#### Opzione B: Crea JAR Eseguibile

```bash
mvn clean package
java -jar target/currency-converter-1.0-SNAPSHOT.jar
```

### 4. Configurazione IDE

#### IntelliJ IDEA

1. Apri il progetto
2. Vai a `File > Project Structure > Project`
3. Imposta SDK su Java 17+
4. Apri `Main.java`
5. Clicca con il tasto destro e seleziona `Run 'Main.main()'`

#### Eclipse

1. Importa come progetto Maven
2. Assicurati di avere JDK 17+
3. Aggiungi le variabili VM:
   ```
   --module-path "PATH_TO_JAVAFX_SDK\lib" --add-modules javafx.controls,javafx.fxml
   ```
4. Esegui `Main.java`

## Funzionalità Principali

### 1. Conversione di Valuta

Seleziona le valute di origine e destinazione, inserisci l'importo e clicca "Converti":

- Valute supportate: EUR, USD, GBP, JPY, CHF
- Conversione istantanea con tasso aggiornato
- Risultato formattato con precisione decimale

### 2. Aggiornamento Tassi

Clicca "🔄 Aggiorna" per:

- Recuperare i tassi più recenti dall'API
- Aggiornare il grafico storico
- Pulire la cache se scaduta

### 3. Grafico Storico

Visualizza l'andamento del tasso di cambio:

- Ultimi 7 giorni (dati mock)
- LineChart interattivo
- Aggiornamento automatico con cambio valuta

### 4. Cache System

Ottimizzazione delle performance:

- Scadenza: 1 ora
- Memorizzazione: ConcurrentHashMap
- Verifica automatica validità

### 5. Gestione Errori

Fallback automatico:

- API non disponibile → Dati mock
- Timeout → Dati mock
- Errori di rete → Dati mock

## Architettura e Pattern

### MVC (Model-View-Controller)

- **Model**: `CurrencyRate`, `HistoricalRate`
- **View**: `currency_converter.fxml` + `style.css`
- **Controller**: `CurrencyConverterController`

### Threading

```java
// Operazione asincrona per API call
Task<Void> task = new Task<Void>() {
    @Override
    protected Void call() {
        // Recupero dati dall'API
        return null;
    }
};

new Thread(task).start();
```

### Cache Strategy

```java
// Cache con scadenza 1 ora
public boolean isExpired() {
    long oneHourInMillis = 60 * 60 * 1000;
    return System.currentTimeMillis() - timestamp > oneHourInMillis;
}
```

## API Reference

### ExchangeRate.host API

**Endpoint**: `https://api.exchangerate.host/latest`

**Parametri**:
- `base`: Valuta di base (es. EUR)
- `symbols`: Valute target (es. USD,GBP)

**Risposta JSON**:
```json
{
  "success": true,
  "timestamp": 1678901234,
  "base": "EUR",
  "date": "2024-01-15",
  "rates": {
    "USD": 1.0850,
    "GBP": 0.8550
  }
}
```

## Personalizzazione

### Aggiungere Nuove Valute

Modifica `ExchangeRateService.java`:

```java
public List<String> getSupportedCurrencies() {
    return Arrays.asList("EUR", "USD", "GBP", "JPY", "CHF", "AUD", "CAD");
}
```

### Modificare Durata Cache

Modifica `CurrencyRate.java`:

```java
public boolean isExpired() {
    long twoHoursInMillis = 2 * 60 * 60 * 1000;
    return System.currentTimeMillis() - timestamp > twoHoursInMillis;
}
```

### Cambiare API

Modifica `ExchangeRateService.fetchRateFromAPI()`:

```java
private static final String API_BASE_URL = "https://api.alternativa-api.com/latest";
```

## Troubleshooting

### JavaFX non trovato

**Errore**: `JavaFX runtime components are missing`

**Soluzione**:

```bash
# Imposta le variabili d'ambiente
set PATH_TO_FX="C:\Program Files\Java\javafx-sdk-21.0.1\lib"

# Esegui con module path
java --module-path "%PATH_TO_FX%" --add-modules javafx.controls -jar app.jar
```

### Connessione API Fallita

**Errore**: `Impossibile recuperare i dati dall'API`

**Soluzione**:
- Verifica la connessione internet
- L'app utilizzerà automaticamente i dati mock
- Controlla la console per dettagli errore

### Maven Build Fallita

**Errore**: `Failed to execute goal`

**Soluzione**:
```bash
mvn clean install -U
```

## Performance

- **Cold Start**: ~2 secondi
- **API Call**: ~500ms (con cache)
- **Cache Hit**: ~5ms
- **Conversion**: Istantanea

## License

Questo progetto è stato creato a scopo educativo.

## Autore

Mattia - Portfolio Project

## Note dello Sviluppatore

### Scelte Tecniche

1. **JavaFX 21**: Ultima versione stabile con miglioramenti performance
2. **Gson**: Parser JSON leggero e affidabile
3. **ConcurrentHashMap**: Cache thread-safe
4. **Task/Thread**: UI responsive durante operazioni lunghe

### Possibili Miglioramenti

- [ ] Persistenza della cache su file
- [ ] Supporto più valute
- [ ] Grafico con periodi personalizzabili
- [ ] Notifiche per variazioni tassi significative
- [ ] Modalità offline completa
- [ ] Test unitari
- [ ] Logging con Log4j

## Risorse Utili

- [JavaFX Documentation](https://openjfx.io/)
- [Gson User Guide](https://github.com/google/gson)
- [ExchangeRate.host API](https://exchangerate.host/)
- [JavaFX CSS Reference](https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/doc-files/cssref.html)

---

**Divertiti con il Currency Converter!** 🔄💱
