# Design dello Schema - Real-time Analytics MongoDB

## Panoramica

Questo progetto implementa un sistema di analisi in tempo reale utilizzando MongoDB, ottimizzato per alti volumi di scrittura e query di aggregazione complesse.

## Collezioni

### 1. Collection `events`

Memorizza i eventi grezzi provenienti da diverse fonti (web, mobile, API).

#### Struttura del Documento

```javascript
{
  _id: ObjectId,
  eventType: String,        // 'pageview', 'click', 'purchase', 'signup', etc.
  sessionId: String,        // Identificatore unico della sessione
  userId: ObjectId,         // Optional (null per utenti anonimi)
  timestamp: Date,          // Quando l'evento è ocorso
  properties: {
    // Proprietà dinamiche dell'evento
    page: String,
    url: String,
    referrer: String,
    userAgent: String,
    ip: String,
    device: String,
    browser: String,
    // ... altre proprietà
  },
  pattern: String,          // 'web', 'mobile', 'api'
  environment: String       // 'production', 'staging'
}
```

#### Indici

- **Indice composto su timestamp e eventType**: Ottimizza le query time-series
  ```javascript
  { timestamp: -1, eventType: 1 }
  ```

- **Indice su sessionId**: Per recuperare tutti gli eventi di una sessione
  ```javascript
  { sessionId: 1 }
  ```

- **Indice su userId**: Per analizzare il comportamento degli utenti
  ```javascript
  { userId: 1, timestamp: -1 }
  ```

- **Indice TTL**: Per eliminare automaticamente i vecchi eventi (es. 90 giorni)
  ```javascript
  { timestamp: 1 }, { expireAfterSeconds: 7776000 }
  ```

- **Indice su environment**: Per separare dati di produzione e staging
  ```javascript
  { environment: 1, timestamp: -1 }
  ```

### 2. Collection `sessions`

Memorizza informazioni aggregate sulle sessioni utente.

#### Struttura del Documento

```javascript
{
  _id: ObjectId,
  sessionId: String,        // Identificatore unico
  userId: ObjectId,         // Optional (null per anonimi)
  startTime: Date,          // Inizio sessione
  endTime: Date,            // Fine sessione
  duration: Number,         // Durata in secondi
  pageViews: Number,        // Numero di page views
  events: [String],         // Array di tipi di eventi
  device: String,
  browser: String,
  location: {
    country: String,
    city: String
  },
  exitPage: String,         // Ultima pagina visitata
  entryPage: String         // Prima pagina visitata
}
```

#### Indici

- **Indice unico su sessionId**: Per evitare duplicati
  ```javascript
  { sessionId: 1 }, { unique: true }
  ```

- **Indice su userId**: Per recuperare tutte le sessioni di un utente
  ```javascript
  { userId: 1, startTime: -1 }
  ```

- **Indice su startTime**: Per analisi temporali delle sessioni
  ```javascript
  { startTime: -1 }
  ```

- **Indice su duration**: Per analizzare la durata delle sessioni
  ```javascript
  { duration: -1 }
  ```

- **Indice geografico**: Per analisi per località
  ```javascript
  { "location.country": 1, "location.city": 1 }
  ```

### 3. Collection `daily_stats`

Memorizza statistiche pre-aggregate per query veloci.

#### Struttura del Documento

```javascript
{
  _id: ObjectId,
  date: Date,              // Data (senza ora)
  eventType: String,       // Tipo di evento
  count: Number,           // Numero totale di eventi
  uniqueUsers: Number,     // Numero di utenti unici
  uniqueSessions: Number   // Numero di sessioni uniche
}
```

#### Indici

- **Indice unico su date e eventType**: Per evitare duplicati
  ```javascript
  { date: 1, eventType: 1 }, { unique: true }
  ```

- **Indice su date**: Per recuperare statistiche di un periodo
  ```javascript
  { date: -1 }
  ```

- **Indice su eventType**: Per confrontare tipi di eventi
  ```javascript
  { eventType: 1, date: -1 }
  ```

- **Indice su count**: Per trovare gli eventi più frequenti
  ```javascript
  { count: -1 }
  ```

## Strategie di Ottimizzazione

### 1. Time-Series Optimization

MongoDB è ottimo per dati time-series. Le strategie includono:

- **Indici complessi su timestamp**: Per query veloci su intervalli di tempo
- **Partitioning implicito**: Usare il campo `environment` per separare dati
- **TTL indexes**: Per eliminare automaticamente i vecchi dati

### 2. Write Optimization

Per alti volumi di scrittura:

- **Write Concern**: Usare `{ w: 1 }` per bilanciare performance e sicurezza
- **Bulk Operations**: Inserire più documenti in una singola operazione
- **Indici minimi**: Solo gli indici necessari per evitare overhead in scrittura
- **Sharding**: Per scalabilità orizzontale (chiave di shard: `timestamp` + `environment`)

### 3. Read Optimization

Per query di aggregazione veloci:

- **Pre-aggregazione**: La collection `daily_stats` pre-calcola statistiche comuni
- **Pipeline ottimizzate**: Ordinare le operazioni nella pipeline ($match prima di $group)
- **Covered queries**: Indici che contengono tutti i campi necessari
- **Projection**: Recuperare solo i campi necessari

### 4. Memory Management

- **Working Set**: Mantenere l'indice e i documenti più recenti in RAM
- **Capped Collections**: Considerare per log o streaming data
- **Compression**: Usare la compressione di MongoDB (snappy o zlib)

## Pattern di Accesso Comuni

### 1. Real-time Dashboard

```javascript
// Eventi degli ultimi 5 minuti
db.events.find({
  timestamp: { $gte: new Date(Date.now() - 5*60*1000) },
  environment: 'production'
}).sort({ timestamp: -1 })
```

### 2. Analisi Sessioni

```javascript
// Sessioni di un utente
db.sessions.find({ userId: ObjectId(...) })
  .sort({ startTime: -1 })
  .limit(10)
```

### 3. Statistiche Giornaliere

```javascript
// Statistiche per gli ultimi 30 giorni
db.daily_stats.find({
  date: { $gte: new Date(Date.now() - 30*24*60*60*1000) }
}).sort({ date: -1 })
```

## Scalabilità

### Sharding Strategy

Per grandi volumi di dati:

1. **Shard Key**: `{ environment: 1, timestamp: 1 }`
   - Distribuisce i dati per environment
   - Mantiene i dati time-series localizzati

2. **Chunk Size**: Configurare in base al volume di scrittura

3. **Tag Awareness**: Separare production e staging su diversi shard

### Replica Set

- **Primary**: Gestisce tutte le operazioni di scrittura
- **Secondaries**: Gestiscono le letture (read preference: secondary)
- **Arbiter**: Per votazione in caso di failover

## Considerazioni sulla Modifica dello Schema

### Quando Modificare

1. **Nuovi tipi di eventi**: Aggiungere valori a `eventType`
2. **Nuove proprietà**: Aggiungere campi a `properties` (schema flessibile)
3. **Nuove metriche**: Aggiungere campi a `daily_stats`

### Migrazioni

- Uso di MongoDB Change Streams per monitorare le modifiche
- Migrazioni graduali per evitare downtime
- Backup prima di modifiche strutturali

## Best Practices

1. **Indici**: Creare solo gli indici necessari
2. **Query**: Sempre usare $match per primo nella pipeline
3. **Projection**: Limitare i campi restituiti
4. **Batching**: Usare bulk operations per inserimenti massivi
5. **Monitoring**: Monitorare query lente con MongoDB Profiler
6. **Backup**: Backup regolari, specialmente prima di modifiche
