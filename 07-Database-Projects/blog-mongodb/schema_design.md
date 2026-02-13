# Design dello Schema - Blog Platform MongoDB

## Panoramica del Progetto

Questo database MongoDB è progettato per una piattaforma di blog moderne con supporto per utenti multipli, categorie gerarchiche, tag, commenti e funzionalità SEO avanzate.

## Decisioni di Design: Embedding vs Referencing

### 1. Collection `users` - Documento Embedding

**Struttura:**
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  password_hash: String,
  profile: {
    firstName: String,
    lastName: String,
    bio: String,
    avatar: String
  },
  role: String,
  status: String,
  createdAt: Date,
  lastLogin: Date
}
```

**Scelta di Design: Embedded Profile**
- **Perché embedding:** Il profilo utente è dati che:
  - Viene sempre letto insieme all'utente
  - Non cresce indefinitamente
  - Non viene modificato frequentemente da altri utenti
  - Ha una relazione 1-a-1 con l'utente

**Vantaggi:**
- Query più veloci (un solo documento)
- Nessun join necessario
- Atomicy nelle operazioni di scrittura

---

### 2. Collection `posts` - Ibrido (Embedding Selezionato)

**Struttura:**
```javascript
{
  _id: ObjectId,
  title: String,
  slug: String,
  content: String,
  excerpt: String,
  author: {
    id: ObjectId,
    username: String,
    avatar: String
  },
  category: {
    _id: ObjectId,
    name: String,
    slug: String
  },
  tags: [String],
  status: String,
  featured: Boolean,
  views: Number,
  metadata: {
    seoTitle: String,
    seoDescription: String,
    keywords: [String]
  },
  comments: [{
    _id: ObjectId,
    user: {id, username, avatar},
    content: String,
    createdAt: Date,
    status: String
  }],
  createdAt: Date,
  updatedAt: Date,
  publishedAt: Date
}
```

**Scelte di Design:**

#### Author (Partial Embedding)
- **Cosa embedded:** `id`, `username`, `avatar`
- **Perché:**
  - Username e avatar servono sempre nella visualizzazione
  - Riduce la necessità di lookup nella collection users
  - Manteniamo l'id per riferimenti completi se necessario

#### Category (Partial Embedding)
- **Cosa embedded:** `_id`, `name`, `slug`
- **Perché:**
  - Il nome della categoria viene mostrato sempre
  - Evita lookup per operazioni comuni
  - Slug utile per URL

#### Tags (Array di String)
- **Struttura:** `tags: ["javascript", "mongodb", "nodejs"]`
- **Perché:**
  - Tag sono semplici stringhe
  - Facilita ricerche e indicizzazioni
  - Query più veloci senza array di oggetti
- **Note:** Esiste anche collection `tags` separata per statistiche e conteggi

#### Comments (Full Embedding)
- **Perché embedding:**
  - La maggior parte dei blog ha < 100 commenti per post
  - I commenti vengono letti in ordine cronologico insieme al post
  - Performance migliori per pagination dei commenti
  - Operazioni atomiche (post + commenti)

**Limitazioni e Considerazioni:**
- **Massimo ~100 commenti per post** per evitare documenti > 16MB
- Per blog con migliaia di commenti, considerare referendum in collection separata
- Se i commenti diventano troppi, archiviare i vecchi in collection storica

#### Metadata SEO (Embedded)
- **Perché:**
  - Dati piccoli e statici
  - Sempre necessari per la visualizzazione della pagina
  - Non richiedono query separate

---

### 3. Collection `categories` - Self-Referencing

**Struttura:**
```javascript
{
  _id: ObjectId,
  name: String,
  slug: String,
  description: String,
  parentCategory: ObjectId, // Riferimento a se stessa
  order: Number,
  postCount: Number
}
```

**Scelta di Design: Referencing**
- **Perché riferimento a `parentCategory`:**
  - Gerarchia potenzialmente infinita (nested categories)
  - Permette navigazione bidirezionale
  - Evita documenti nidificati complessi
  - Facilita query di alberi completi

**Vantaggi:**
- Flessibilità nella gerarchia
- Query efficienti per sottocategorie
- Facile implementare drag-and-drop di categorie

---

### 4. Collection `tags` - Denormalizzazione

**Struttura:**
```javascript
{
  _id: ObjectId,
  name: String,
  slug: String,
  postCount: Number
}
```

**Scelta di Design: Denormalizzazione**
- **Duplicazione intenzionale:** I tag esistono sia come:
  1. Array di stringhe nei posts
  2. Documenti separati in questa collection

**Perché:**
- **Array in posts:** Query veloci e semplici per post con tag specifici
- **Collection separata:** Statistiche, conteggi, e pagine di tag
- **postCount:** Campo denormalizzato per performance (evita aggregate counts)

**Trade-off:**
- **Sincronizzazione necessaria:** Aggiornare `postCount` quando si aggiunge/rimuove tag
- **Performance vs Consistenza:** Scelto performance per lettura (molto più frequente)

---

## Indici e Performance

### Indici Primary
- Tutti i `_id` sono automaticamente indicizzati da MongoDB

### Indici Unique
- `users.email` - Unicità email
- `users.username` - Unicità username
- `posts.slug` - Unicità slug (per URL unici)
- `categories.slug` - Unicità slug categoria
- `tags.slug` - Unicità slug tag

### Indici Compound
- `posts.status + posts.publishedAt` - Query post pubblicati ordinati per data
- `posts.author.id + posts.createdAt` - Post per autore ordinati
- `posts.category._id + posts.status` - Post per categoria

### Indici Text
- `posts.title + posts.content + posts.excerpt` - Full-text search
- `categories.name + categories.description` - Ricerca categorie

### Indici Single Field
- `posts.tags` - Per query di tag
- `posts.featured` - Post in evidenza
- `posts.views` - Ordinamento per popolarità
- `categories.parentCategory` - Gerarchia categorie
- `tags.postCount` - Tag cloud ordinati

---

## Scalabilità e Limiti

### Limiti MongoDB Considerati
1. **Documento massimo: 16MB**
   - Commenti embedding: Limitare a ~100 commenti
   - Content post: Considerare GridFS per post > 10MB

2. **Nesting massimo: 100 livelli**
   - Non un problema per la nostra struttura

3. **Array massimo: Non c'è limite pratico**
   - Tags possono essere molti senza problemi

### Strategie di Scalabilità

#### Sharding (Se necessario)
- **Shard Key consigliata:** `posts.category._id` o `posts.author.id`
- Distribuisce i post per categoria/autore
- Mantiene i post correlati insieme

#### Replica Set
- Secondaries per letture
- Automatic failover
- Consistency tuning (write concern)

---

## Relazioni tra Collection

```
users (1) ----< (N) posts
       |
       +--------< comments

categories (1) ----< (N) posts
        |
        +----< (N) categories (parent-child)

tags (1) ----< (N) posts (denormalized as array)
```

---

## Ottimizzazioni Query

### Query Comuni e Indici

1. **Post per slug (URL)**
   ```javascript
   db.posts.findOne({ slug: "mio-post" })
   ```
   - Indice: Unique su `slug`

2. **Post pubblicati recenti**
   ```javascript
   db.posts.find({ status: "published" })
     .sort({ publishedAt: -1 })
     .limit(10)
   ```
   - Indice: Compound `{ status: 1, publishedAt: -1 }`

3. **Full-text search**
   ```javascript
   db.posts.find({ $text: { $search: "mongodb tutorial" } })
   ```
   - Indice: Text su `title`, `content`, `excerpt`

4. **Post per tag**
   ```javascript
   db.posts.find({ tags: "javascript" })
   ```
   - Indice: Single field su `tags`

5. **Post per autore**
   ```javascript
   db.posts.find({ "author.id": userId })
   ```
   - Indice: Compound su `author.id`

---

## Considerazioni Finali

### Vantaggi di Questo Design
1. **Performance di lettura:** Embedding riduce join
2. **Query semplici:** Struttura piatta e naturale
3. **Flessibilità:** Schema-less di MongoDB permette evoluzione
4. **SEO-friendly:** Metadata integrati nei post

### Potenziali Miglioramenti Futuri
1. **Caching layer:** Redis per sessioni e contatori
2. **Full-text search engine:** Elasticsearch per ricerca avanzata
3. **Analytics:** Collection separata per views/engagement
4. **Versioning:** Post history con versioni precedenti
5. **Media:** GridFS per immagini e allegati

Questo schema è ottimizzato per un blog con traffico medio-alto, con focus su performance di lettura e flessibilità per future espansioni.
