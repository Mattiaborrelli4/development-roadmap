# Blog Platform Database - MongoDB

Progetto di database MongoDB per una piattaforma di blog moderna con supporto multi-utente, categorie gerarchiche, tag, commenti e funzionalità SEO avanzate.

## Indice

- [Caratteristiche](#caratteristiche)
- [Tecnologia](#tecnologia)
- [Struttura del Database](#struttura-del-database)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Documentazione](#documentazione)
- [Schema Design](#schema-design)
- [Query Esempi](#query-esempi)

## Caratteristiche

- **Multi-utente**: Supporto per autori, editor e admin
- **Categorie Gerarchiche**: Sistema di categorie nidificate infinite
- **Tag System**: Tag cloud con aggregazione automatica
- **Commenti Embedding**: Commenti integrati nei post per performance ottimali
- **SEO Friendly**: Metadata SEO integrati per ogni post
- **Full-Text Search**: Ricerca testuale avanzata con scoring
- **Views Tracking**: Tracciamento visualizzazioni post
- **Draft System**: Gestione stati (bozza, pubblicato, archiviato)
- **Featured Posts**: Post in evidenza

## Tecnologia

- **Database**: MongoDB 6.0+
- **Query Language**: MQL (MongoDB Query Language)
- **Language**: JavaScript (Node.js / MongoDB Shell)

## Struttura del Database

### Collections

1. **users** - Utenti della piattaforma
2. **posts** - Articoli del blog con commenti embedded
3. **categories** - Categorie gerarchiche
4. **tags** - Tag con aggregazione post count

### Schema Relationships

```
users (1) ----< (N) posts
       |
       +--------< comments

categories (1) ----< (N) posts
        |
        +----< (N) categories (parent-child)

tags (1) ----< (N) posts (denormalized as array)
```

## Installazione

### Prerequisiti

1. MongoDB installato e in esecuzione
2. MongoDB Shell (mongosh) o Node.js con driver MongoDB

### Passi di Installazione

1. **Clona o scarica il progetto**
   ```bash
   cd blog-mongodb
   ```

2. **Avvia MongoDB**
   ```bash
   mongod
   ```

3. **Esegui lo script di setup**
   ```bash
   # Nella shell MongoDB
   mongosh
   use blog_platform
   load('setup.js')
   ```

   Questo creerà tutte le collections e gli indici necessari.

4. **Popola il database con dati di esempio**
   ```bash
   load('sample_data.js')
   ```

   Questo inserirà:
   - 25+ utenti
   - 60+ post con commenti
   - 13 categorie (alcune nidificate)
   - 50+ tag

5. **Verifica l'installazione**
   ```javascript
   db.users.countDocuments()  // Dovrebbe mostrare 25+
   db.posts.countDocuments()   // Dovrebbe mostrare 60+
   db.categories.countDocuments()  // Dovrebbe mostrare 13
   db.tags.countDocuments()    // Dovrebbe mostrare 50+
   ```

## Utilizzo

### Connessione al Database

```bash
# MongoDB Shell
mongosh
use blog_platform
```

### Query di Base

#### Trova Tutti i Post Pubblicati

```javascript
db.posts.find({ status: 'published' })
  .sort({ publishedAt: -1 })
  .limit(10)
```

#### Trova Post per Categoria

```javascript
db.posts.find({ 'category.slug': 'tecnologia' })
  .sort({ publishedAt: -1 })
```

#### Ricerca Full-Text

```javascript
db.posts.find(
  { $text: { $search: 'mongodb tutorial' } },
  { score: { $meta: 'textScore' } }
)
.sort({ score: { $meta: 'textScore' } })
```

### Caricare le Query Helper

```bash
load('queries.js')
```

Questo caricherà funzioni helper per query comuni:

```javascript
// Ultimi post
findLatestPosts(10)

// Post per categoria
findPostsByCategory('tecnologia', 5)

// Ricerca testuale
textSearch('javascript')

// Tag cloud
generateTagCloud(20)

// Gerarchia categorie
getCategoryHierarchy()

// Classifica autori
getAuthorLeaderboard()
```

## Documentazione

### File del Progetto

- **`schema_design.md`** - Documentazione completa dello schema
  - Decisioni di design (embedding vs referencing)
  - Struttura di ogni collection
  - Indici e ottimizzazioni
  - Considerazioni di scalabilità

- **`setup.js`** - Script di inizializzazione database
  - Creazione collections
  - Configurazione indici (unique, compound, text)
  - Validatori JSON Schema
  - Funzioni utility

- **`sample_data.js`** - Generatore dati di esempio
  - Utenti con profili
  - Post con commenti
  - Categorie gerarchiche
  - Tag con post counts
  - Funzioni helper

- **`queries.js`** - Raccolta query esempio
  - Query di base
  - Aggregation pipelines
  - Full-text search
  - Filtri avanzati
  - Statistiche

## Schema Design

### Decisioni Chiave

#### 1. Users - Profile Embedding

Il profilo utente è embedded perché:
- Letto sempre insieme all'utente
- Non cresce eccessivamente
- Performance migliori (no join)

#### 2. Posts - Commenti Embedding

I commenti sono embedded nei post perché:
- La maggior parte dei blog ha < 100 commenti
- Letti in ordine cronologico
- Performance migliori per pagination
- Operazioni atomiche

#### 3. Categories - Self-Referencing

Le categorie referenziano sé stesse per:
- Gerarchia nidificata infinita
- Query bidirezionali
- Semplicità di gestione

#### 4. Tags - Denormalizzazione

I tag esistono come:
- Array di stringhe nei posts (query veloci)
- Documenti separati in collection tags (statistiche)

### Indici

#### Unique Indexes
- `users.email`
- `users.username`
- `posts.slug`
- `categories.slug`
- `tags.slug`

#### Compound Indexes
- `{ status: 1, publishedAt: -1 }` - Post per data
- `{ 'author.id': 1, createdAt: -1 }` - Post per autore
- `{ 'category._id': 1, status: 1 }` - Post per categoria
- `{ featured: -1, status: 1, publishedAt: -1 }` - Featured posts
- `{ views: -1, status: 1 }` - Popolari

#### Text Indexes
- `posts`: title, content, excerpt, keywords
- `categories`: name, description
- `tags`: name

## Query Esempi

### 1. Post Pubblicati Recenti

```javascript
db.posts.find({ status: 'published' })
  .sort({ publishedAt: -1 })
  .limit(10)
```

### 2. Post per Categoria

```javascript
db.posts.find({
  'category.slug': 'tecnologia',
  status: 'published'
})
.sort({ publishedAt: -1 })
```

### 3. Full-Text Search

```javascript
db.posts.find(
  { $text: { $search: 'mongodb tutorial' } }
)
.sort({ score: { $meta: 'textScore' } })
```

### 4. Post per Tag

```javascript
db.posts.find({
  tags: 'javascript',
  status: 'published'
})
```

### 5. Aggregation: Post per Categoria

```javascript
db.posts.aggregate([
  { $match: { status: 'published' } },
  { $group: {
    _id: '$category.name',
    count: { $sum: 1 }
  }},
  { $sort: { count: -1 } }
])
```

### 6. Post di un Autore

```javascript
db.posts.find({
  'author.username': 'marirossi123',
  status: 'published'
})
.sort({ publishedAt: -1 })
```

### 7. Post in Evidenza

```javascript
db.posts.find({
  featured: true,
  status: 'published'
})
.sort({ publishedAt: -1 })
```

### 8. Post con Commenti

```javascript
db.posts.findOne({
  slug: 'mio-post'
}, {
  comments: 1
})
```

### 9. Post per Range di Date

```javascript
db.posts.find({
  status: 'published',
  publishedAt: {
    $gte: ISODate('2024-01-01'),
    $lte: ISODate('2024-12-31')
  }
})
```

### 10. Tag Cloud (Aggregation)

```javascript
db.posts.aggregate([
  { $match: { status: 'published' } },
  { $unwind: '$tags' },
  { $group: {
    _id: '$tags',
    count: { $sum: 1 }
  }},
  { $sort: { count: -1 } },
  { $limit: 30 }
])
```

### 11. Gerarchia Categorie

```javascript
db.categories.aggregate([
  { $match: { parentCategory: null } },
  { $lookup: {
    from: 'categories',
    localField: '_id',
    foreignField: 'parentCategory',
    as: 'subcategories'
  }}
])
```

## Performance e Scalabilità

### Limiti Documenti
- **Max documento**: 16MB (MongoDB)
- **Max commenti consigliati**: ~100 per post
- **Tags**: Senza limite pratico

### Ottimizzazioni
- Indici compound per query comuni
- Text search con weights
- Denormalizzazione per performance
- Embedded documents per ridurre join

### Sharding (se necessario)
- **Shard Key consigliata**: `posts.category._id` o `posts.author.id`
- Distribuisce i post per categoria/autore
- Mantiene i post correlati insieme

## Funzioni Helper

### Setup Utility

```javascript
// Mostra tutti gli indici
showIndexes()

// Elimina tutti gli indici (tranne _id)
dropAllIndexes()

// Statistiche database
dbStats()
```

### Sample Data Utility

```javascript
// Mostra statistiche dettagliate
showStats()

// Reset del database
resetDatabase()
```

### Query Functions

Vedi `queries.js` per la lista completa delle funzioni disponibili:

- `findPostsByCategory(slug, limit)`
- `textSearch(searchTerm, limit)`
- `findPostsByTag(tagName, limit)`
- `postsPerCategory()`
- `findUserPosts(username, includeDrafts)`
- `findLatestPosts(limit)`
- `findFeaturedPosts(limit)`
- `findPostWithComments(slug)`
- `findPostsByDateRange(startDate, endDate)`
- `generateTagCloud(limit)`
- `getCategoryHierarchy()`
- `findPopularPosts(limit)`
- `findRelatedPosts(postId, limit)`
- `getAuthorLeaderboard()`
- `searchWithFilters(filters)`
- `getMonthlyArchive()`

## Considerazioni di Produzione

### Security
- Usare password hash forte (bcrypt, argon2)
- Implementare autenticazione JWT
- Validare tutti gli input
- Sanitizzare i commenti

### Backup
- Abilitare replica set
- Configurare automatic backup
- Export regolare con `mongodump`

### Monitoring
- Monitorare query lente con `db.setProfilingLevel()`
- Utilizzare MongoDB Atlas o tools di monitoring
- Metriche: operazioni/sec, memoria, CPU

### Miglioramenti Futuri
- **Redis**: Per caching sessioni e contatori
- **Elasticsearch**: Per full-text search avanzata
- **GridFS**: Per media files (immagini, video)
- **Change Streams**: Per realtime updates
- **Time Series**: Per analytics e views

## Troubleshooting

### Errore: "Index already exists"
```javascript
// Droppa l'indice prima di ricrearlo
db.posts.dropIndex('index_name')
```

### Errore: "Document too large"
```javascript
// Limita i commenti embedded
db.posts.updateOne(
  { _id: postId },
  { $push: { comments: { $each: [], $slice: -100 } } }
)
```

### Query lenta
```javascript
// Controlla execution plan
db.posts.find({...}).explain('executionStats')

// Aggiungi indice se necessario
db.posts.createIndex({ field: 1 })
```

## License

Questo progetto è a scopo educativo. Sentiti libero di utilizzarlo e modificarlo secondo le tue esigenze.

## Autore

Progetto creato come portfolio per database design e query optimization con MongoDB.

---

**Note**:
- Questo progetto utilizza MongoDB 6.0+
- Per problemi o domande, consulta la documentazione ufficiale MongoDB: https://docs.mongodb.com/
