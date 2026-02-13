# Architettura Currency Converter

## Diagramma dei Componenti

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  HEADER (VBox)                                           │  │
│  │  ┌─────────────────────┐  ┌─────────────────────────┐   │  │
│  │  │ Currency Converter  │  │ Convertitore di Valuta   │   │  │
│  │  │      (Title)       │  │      (Subtitle)         │   │  │
│  │  └─────────────────────┘  └─────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  CONVERSION PANEL (GridPane)                            │  │
│  │  ┌────────┐ ┌────────────┐ ┌─────┐                    │  │
│  │  │  Da:   │ │ [ComboBox] │ │ ⇄   │                    │  │
│  │  ├────────┤ ├────────────┤ ├─────┤                    │  │
│  │  │  A:    │ │ [ComboBox] │      │                    │  │
│  │  ├────────┤ ├────────────┤      │                    │  │
│  │  │Importo:│ │ [TextField]│Convert│                    │  │
│  │  ├────────┤ ├────────────┤──────┤                    │  │
│  │  │Risult: │ │ [Label]    │      │                    │  │
│  │  └────────┘ └────────────┘      │                    │  │
│  └────────────────────────────────────┘                    │  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  RATE INFO (HBox)                                      │  │
│  │  ┌──────────────┐ ┌───────────────┐ ┌────┐ ┌────────┐  │  │
│  │  │ Tasso: ...  │ │ Aggiornamento │ │Refresh│Spinner │  │  │
│  │  └──────────────┘ └───────────────┘ └────┘ └────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  CHART (LineChart)                                      │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │  ┌───┐                                          │    │  │
│  │  │  │   │  /─\                                    │    │  │
│  │  │  │   │─    ─\     /─\                          │    │  │
│  │  │  │   │        \─/     ─\                       │    │  │
│  │  │  └───┘                 ──\                    │    │  │
│  │  │  Data ───────────────────────────────►        │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  FOOTER (HBox)                                          │  │
│  │  Dati forniti da ExchangeRate.host | Cache: 1 ora       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Pattern MVC

```
┌─────────────────────────────────────────────────────────────┐
│                        MODEL                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CurrencyRate                    HistoricalRate             │
│  ┌─────────────────────┐        ┌──────────────────┐      │
│  │ from: String        │        │ date: String     │      │
│  │ to: String          │        │ rate: double     │      │
│  │ rate: double        │        └──────────────────┘      │
│  │ timestamp: long      │                                   │
│  │ isExpired()         │                                   │
│  └─────────────────────┘                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ Uses
                              │
┌─────────────────────────────┴──────────────────────────────┐
│                      CONTROLLER                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CurrencyConverterController                                │
│  ┌─────────────────────────────────────────────────┐      │
│  │ @FXML Components                               │      │
│  │  - ComboBox fromCurrencyCombo                   │      │
│  │  - ComboBox toCurrencyCombo                     │      │
│  │  - TextField amountTextField                    │      │
│  │  - Label resultLabel                            │      │
│  │  - Label rateLabel                              │      │
│  │  - LineChart historyChart                       │      │
│  │  - ProgressIndicator loadingIndicator            │      │
│  └─────────────────────────────────────────────────┘      │
│                                                             │
│  Methods:                                                   │
│  ┌─────────────────────────────────────────────────┐      │
│  │ + initialize()                                  │      │
│  │ + handleConvert()                               │      │
│  │ + handleRefresh()                               │      │
│  │ + handleSwap()                                  │      │
│  │ - performConversion(from, to, amount)           │      │
│  │ - fetchRatesAndChart()                          │      │
│  │ - updateChart(historicalRates)                  │      │
│  │ - showLoading(boolean)                          │      │
│  │ - showAlert(title, message)                     │      │
│  └─────────────────────────────────────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              │ Binds
                              │
┌─────────────────────────────┴──────────────────────────────┐
│                         VIEW                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  currency_converter.fxml + style.css                        │
│                                                             │
│  BorderPane                                                 │
│  ├── top: Header (VBox)                                    │
│  ├── center: Main Content (VBox)                           │
│  │   ├── Conversion Panel (GridPane)                       │
│  │   ├── Rate Info (HBox)                                 │
│  │   └── Chart (LineChart)                                │
│  └── bottom: Footer (HBox)                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Flusso dei Dati

### 1. Conversion Flow

```
User Input (Amount)
      │
      ▼
[Button Click / Enter]
      │
      ▼
handleConvert()
      │
      ├─→ Validate Input
      │       │
      │       └─→ Error? → showAlert()
      │
      └─→ Valid? → performConversion()
                       │
                       ▼
                  [Create Task]
                       │
                       ├─→ [Worker Thread]
                       │       │
                       │       ├─→ rateService.getCurrentRate()
                       │       │       │
                       │       │       ├─→ Check Cache
                       │       │       │       │
                       │       │       │       ├─→ Valid? → Return
                       │       │       │       │
                       │       │       │       └─→ Expired? → Fetch API
                       │       │       │                       │
                       │       │       │                       ├─→ Success → Cache It
                       │       │       │                       │
                       │       │       │                       └─→ Fail → Mock Data
                       │       │       │
                       │       │       └─→ Return Rate
                       │       │
                       │       └─→ Calculate Result
                       │
                       └─→ [Platform.runLater]
                                 │
                                 └─→ Update UI
                                         │
                                         ├─→ resultLabel
                                         ├─→ rateLabel
                                         ├─→ lastUpdateLabel
                                         └─→ hideLoading()
```

### 2. Cache Flow

```
Request Rate
     │
     ▼
Check Cache (ConcurrentHashMap)
     │
     ├─→ Hit + Valid?
     │       │
     │       └─→ Yes → Return Cached Rate
     │
     └─→ Miss OR Expired?
             │
             ├─→ Fetch from API
             │       │
             │       ├─→ Success?
             │       │       │
             │       │       └─→ Yes → Store in Cache
             │       │               │
             │       │               └─→ Return
             │       │
             │       └─→ Fail?
             │               │
             │               └─→ Return Mock Rate
             │
             └─→ Return
```

### 3. Chart Update Flow

```
User Action (Refresh / Change Currency)
      │
      ▼
fetchRatesAndChart()
      │
      ├─→ showLoading(true)
      │
      └─→ [Create Task]
               │
               ├─→ [Worker Thread]
               │       │
               │       ├─→ rateService.getHistoricalRates()
               │       │       │
               │       │       └─→ Generate 7 Days Mock Data
               │       │
               │       ├─→ rateService.getCurrentRate()
               │       │
               │       └─→ Return Data
               │
               └─→ [Platform.runLater]
                        │
                        ├─→ updateChart()
                        │       │
                        │       └─→ Populate LineChart
                        │
                        ├─→ Update Labels
                        │
                        └─→ showLoading(false)
```

## Threading Model

```
┌─────────────────────────────────────────────────────────┐
│           JavaFX Application Thread (UI)                │
│  - User Input Handling                                 │
│  - UI Updates                                          │
│  - Event Dispatch                                      │
└────────────┬────────────────────────────────────────────┘
             │
             │ Platform.runLater()
             │
┌────────────▼────────────────────────────────────────────┐
│              Task<T> (Bridge)                           │
│  - Manages Worker Thread                                │
│  - Handles Exceptions                                   │
│  - Updates Value Property                               │
└────────────┬────────────────────────────────────────────┘
             │
             │ new Thread(task).start()
             │
┌────────────▼────────────────────────────────────────────┐
│           Worker Thread (Background)                    │
│  - API Calls (HTTP)                                     │
│  - JSON Parsing                                         │
│  - Cache Operations                                     │
│  - Data Generation                                      │
└─────────────────────────────────────────────────────────┘
```

## Service Layer

```
ExchangeRateService
├─ Constants
│   ├─ API_BASE_URL
│   ├─ MOCK_RATES (Map)
│   └─ cache (ConcurrentHashMap)
│
├─ Methods
│   ├─ getCurrentRate(from, to)
│   │      ├─→ Check Cache
│   │      ├─→ Fetch API (if needed)
│   │      └─→ Return Mock (fallback)
│   │
│   ├─ fetchRateFromAPI(from, to)
│   │      ├─→ HttpURLConnection
│   │      ├─→ Parse JSON (Gson)
│   │      └─→ Return CurrencyRate
│   │
│   ├─ getMockRate(from, to)
│   │      ├─→ Lookup MOCK_RATES
│   │      ├─→ Calculate Inverse (if needed)
│   │      └─→ Return CurrencyRate
│   │
│   ├─ getHistoricalRates(from, to)
│   │      ├─→ Generate 7 Days Data
│   │      ├─→ Apply ±2% Variation
│   │      └─→ Return List<HistoricalRate>
│   │
│   ├─ clearCache()
│   └─ getSupportedCurrencies()
```

## Component Diagram

```
┌────────────────────────────────────────────────────────┐
│                        Main                           │
│  ┌────────────────────────────────────────────────┐  │
│  │ + main(args: String[]): void                   │  │
│  │   - Loads FXML                                 │  │
│  │   - Creates Scene                              │  │
│  │   - Shows Stage                                │  │
│  └────────────────────────────────────────────────┘  │
└────────────┬───────────────────────────────────────────┘
             │ FXMLLoader
             │
┌────────────▼───────────────────────────────────────┐
│         CurrencyConverterController                  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │           ExchangeRateService                 │  │
│  │  - API Integration                            │  │
│  │  - Cache Management                          │  │
│  │  - Mock Data Generation                      │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │         Models                               │  │
│  │  - CurrencyRate                             │  │
│  │  - HistoricalRate                           │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

## Package Structure

```
com.currencyconverter/
├── Main.java                    # Entry Point
├── model/                       # Data Models
│   ├── CurrencyRate.java
│   └── HistoricalRate.java
├── service/                     # Business Logic
│   └── ExchangeRateService.java
└── controller/                  # UI Controllers
    └── CurrencyConverterController.java

Resources/
└── com/currencyconverter/
    ├── currency_converter.fxml  # UI Layout
    └── css/
        └── style.css           # Styling
```

## Data Flow Diagram

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
│  User  │────▶│ Controller│────▶│ Service  │────▶│   API   │
└────────┘     └──────────┘     └──────────┘     └─────────┘
                    │                  │
                    │                  │
                    ▼                  ▼
               ┌──────────┐     ┌──────────┐
               │   View   │◀────│  Cache   │
               └──────────┘     └──────────┘
                    │
                    ▼
               ┌──────────┐
               │   User   │
               └──────────┘
```

## Error Handling Flow

```
┌─────────────┐
│   Action   │
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ Try API     │
└──────┬───────┘
       │
       ├─→ Success?
       │       │
       │       └─→ Yes ──→ Return Data
       │
       └─→ No
               │
               ▼
         ┌──────────┐
         │ Log Error│
         └─────┬────┘
               │
               ▼
         ┌──────────┐
         │ Mock Data│
         └─────┬────┘
               │
               ▼
         ┌──────────┐
         │  Alert   │
         └──────────┘
```

## State Management

```
Application States:
├─ INITIALIZING
│  └─→ Loading FXML, Setup UI
│
├─ IDLE
│  └─→ Waiting for user input
│
├─ LOADING
│  ├─→ Fetching rates from API
│  ├─→ Show spinner
│  └─→ Disable controls
│
├─ READY
│  ├─→ Display results
│  ├─→ Hide spinner
│  └─→ Enable controls
│
└─ ERROR
   ├─→ Show alert
   ├─→ Use mock data
   └─→ Return to IDLE
```

---

**Convenzioni**
- `→` : Flusso dati
- `├─` : Branching
- `└─` : Continuation
- `◀─` : Return/Feedback
