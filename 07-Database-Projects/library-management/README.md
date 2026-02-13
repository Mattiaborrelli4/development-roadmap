# Sistema di Gestione Bibliotecaria

## Panoramica del Progetto

Questo progetto è un sistema completo di gestione di una biblioteca implementato come database relazionale PostgreSQL. Il sistema permette di gestire libri, autori, editori, membri e prestiti, fornendo un'infrastruttura solida per tracciare tutte le operazioni di una biblioteca moderna.

## Diagramma ER (Entity-Relationship)

Il database è composto dalle seguenti entità principali:

### Tabelle Principali

1. **editori** - Case editrici che pubblicano i libri
2. **categorie** - Categorie/Geni letterari
3. **autori** - Autori dei libri
4. **libri** - Catalogo dei libri della biblioteca
5. **membri** - Membri registrati alla biblioteca
6. **prestiti** - Registro dei prestiti
7. **libri_autori** - Tabella di giunzione molti-a-molti (libri ↔ autori)

### Relazioni

```
editori (1) ──────< (N) libri
  |
  └── published_by

categorie (1) ──────< (N) libri
  |
  └── categorized_by

libri (1) ──────< (N) prestiti
  |
  └── borrowed_in

membri (1) ──────< (N) prestiti
  |
  └── borrowed_by

autori (M) ──────< (N) libri_autori (M:N) ──────> (N) libri
  |                                          |
  └── written_by                            └── has_author
```

### Dettaglio delle Relazioni

- **libri → editori**: molti-a-uno (ogni libro ha un editore)
- **libri → categorie**: molti-a-uno (ogni libro appartiene a una categoria)
- **libri → autori**: molti-a-molti (un libro può avere più autori, un autore può scrivere più libri)
- **libri → prestiti**: uno-a-molti (un libro può essere prestato più volte)
- **membri → prestiti**: uno-a-molti (un membro può fare più prestiti)

## Struttura del Progetto

```
library-management/
├── schema.sql          # Definizione dello schema del database
├── sample_data.sql     # Dati di esempio per il testing
├── queries.sql         # Query di esempio e documentazione
└── README.md           # Questo file
```

## Installazione e Configurazione

### Prerequisiti

- PostgreSQL 12 o superiore
- Accesso come amministratore o utente con permessi CREATE DATABASE

### Passo 1: Creazione del Database

```bash
# Accedi a PostgreSQL
psql -U postgres

# Crea il database
CREATE DATABASE biblioteca;

# Esci da psql
\q
```

### Passo 2: Esecuzione dello Schema

```bash
# Connessione al database
psql -U postgres -d biblioteca

# Esegui lo schema
\i schema.sql

# Verifica la creazione delle tabelle
\dt
```

### Passo 3: Inserimento dei Dati di Esempio

```bash
# Esegui lo script dei dati di esempio
\i sample_data.sql

# Verifica i dati inseriti
SELECT COUNT(*) FROM libri;
SELECT COUNT(*) FROM membri;
SELECT COUNT(*) FROM prestiti;
```

## Spiegazione delle Tabelle

### 1. editori

Contiene le informazioni sulle case editrici.

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| id | SERIAL | Chiave primaria |
| nome | VARCHAR(100) | Nome della casa editrice |
| indirizzo | VARCHAR(255) | Indirizzo fisico |
| telefono | VARCHAR(20) | Numero di telefono |
| email | VARCHAR(100) | Email di contatto |
| created_at | TIMESTAMP | Timestamp di creazione |

### 2. categorie

Classificazione dei libri per genere.

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| id | SERIAL | Chiave primaria |
| nome | VARCHAR(50) | Nome della categoria (UNIQUE) |
| descrizione | TEXT | Descrizione dettagliata |
| created_at | TIMESTAMP | Timestamp di creazione |

**Categorie incluse:**
- Romanzo
- Thriller
- Fantascienza
- Fantasy
- Storia
- Filosofia
- Scienza
- Poesia
- Bambini
- Saggistica

### 3. autori

Informazioni sugli autori dei libri.

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| id | SERIAL | Chiave primaria |
| nome | VARCHAR(100) | Nome completo dell'autore |
| anno_nascita | INTEGER | Anno di nascita |
| anno_morte | INTEGER | Anno di morte (NULL se vivo) |
| biografia | TEXT | Biografia breve |
| nazionalita | VARCHAR(50) | Nazionalità dell'autore |
| created_at | TIMESTAMP | Timestamp di creazione |

**Vincolo:** `anno_morte >= anno_nascita`

### 4. membri

Anagrafica dei membri della biblioteca.

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| id | SERIAL | Chiave primaria |
| nome | VARCHAR(50) | Nome |
| cognome | VARCHAR(50) | Cognome |
| email | VARCHAR(100) | Email (UNIQUE) |
| telefono | VARCHAR(20) | Telefono di contatto |
| data_iscrizione | DATE | Data di registrazione |
| stato | VARCHAR(20) | Stato: attivo, sospeso, inattivo |
| note | TEXT | Note aggiuntive |
| created_at | TIMESTAMP | Timestamp di creazione |

**Vincoli:**
- Email deve essere valida (regex check)
- Stato può essere solo: 'attivo', 'sospeso', 'inattivo'

### 5. libri

Catalogo completo dei libri.

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| id | SERIAL | Chiave primaria |
| titolo | VARCHAR(255) | Titolo del libro |
| isbn | VARCHAR(20) | ISBN (UNIQUE) |
| anno_pubblicazione | INTEGER | Anno di pubblicazione |
| editore_id | INTEGER | FK → editori(id) |
| categoria_id | INTEGER | FK → categorie(id) |
| copie_totali | INTEGER | Numero totale di copie |
| copie_disponibili | INTEGER | Copie attualmente disponibili |
| descrizione | TEXT | Sinossi del libro |
| lingua | VARCHAR(20) | Lingua (default: Italiano) |
| created_at | TIMESTAMP | Timestamp di creazione |

**Vincoli:**
- `copie_disponibili <= copie_totali`
- `anno_pubblicazione` tra 1000 e anno corrente + 1
- Foreign Keys con ON DELETE RESTRICT (non cancella se ci sono prestiti)

### 6. libri_autori

Tabella di giunzione per la relazione molti-a-molti tra libri e autori.

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| libro_id | INTEGER | FK → libri(id), ON DELETE CASCADE |
| autore_id | INTEGER | FK → autori(id), ON DELETE CASCADE |
| created_at | TIMESTAMP | Timestamp di creazione |

**Primary Key:** (libro_id, autore_id)

### 7. prestiti

Registro di tutti i prestiti effettuati.

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| id | SERIAL | Chiave primaria |
| libro_id | INTEGER | FK → libri(id), ON DELETE RESTRICT |
| membro_id | INTEGER | FK → membri(id), ON DELETE RESTRICT |
| data_prestito | DATE | Data inizio prestito |
| data_scadenza | DATE | Data restituzione prevista |
| data_restituzione | DATE | Data effettiva restituzione (NULL se in corso) |
| stato | VARCHAR(20) | Stato: in_corso, restituito, in_ritardo, perso |
| note | TEXT | Note sul prestito |
| created_at | TIMESTAMP | Timestamp di creazione |

**Vincoli:**
- `data_restituzione >= data_prestito` (se non NULL)
- `data_scadenza >= data_prestito`
- Stato può essere solo: 'in_corso', 'restituito', 'in_ritardo', 'perso'

## Indici e Performance

Il database include diversi indici per ottimizzare le query più comuni:

### Indici principali

- **libri**: titolo, isbn, categoria, editore, anno_pubblicazione
- **membri**: cognome, email, stato, nome+cognome
- **autori**: nome, nazionalità
- **prestiti**: libro, membro, stato, date (prestito, scadenza, restituzione)
- **Full-text search**: indice su titolo libri in lingua italiana

### Viste predefinite

1. **vista_libri_dettagli**: Informazioni complete dei libri con autori
2. **vista_prestiti_attuali**: Prestiti in corso con stato ritardo
3. **vista_statistiche_categorie**: Statistiche aggregate per categoria

## Query di Esempio

### Query di Base

#### 1. Elencare tutti i libri disponibili
```sql
SELECT titolo, isbn, copie_disponibili
FROM libri
WHERE copie_disponibili > 0
ORDER BY titolo;
```

#### 2. Trovare libri per autore
```sql
SELECT l.titolo, a.nome AS autore
FROM libri l
JOIN libri_autori la ON l.id = la.libro_id
JOIN autori a ON la.autore_id = a.id
WHERE a.nome = 'Umberto Eco';
```

#### 3. Mostrare i prestiti attuali di un membro
```sql
SELECT l.titolo, p.data_prestito, p.data_scadenza
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
WHERE p.membro_id = 1
  AND p.stato IN ('in_corso', 'in_ritardo');
```

#### 4. Contare i libri per categoria
```sql
SELECT c.nome AS categoria, COUNT(l.id) AS numero_libri
FROM categorie c
LEFT JOIN libri l ON c.id = l.categoria_id
GROUP BY c.nome
ORDER BY numero_libri DESC;
```

#### 5. Trovare i prestiti in ritardo
```sql
SELECT
    l.titolo,
    m.cognome,
    p.data_scadenza,
    CURRENT_DATE - p.data_scadenza AS giorni_ritardo
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
JOIN membri m ON p.membro_id = m.id
WHERE p.stato = 'in_ritardo'
ORDER BY giorni_ritardo DESC;
```

### Query Avanzate

#### 6. Libri più popolari (più prestati)
```sql
SELECT
    l.titolo,
    COUNT(p.id) AS numero_prestiti
FROM libri l
JOIN prestiti p ON l.id = p.libro_id
GROUP BY l.id, l.titolo
ORDER BY numero_prestiti DESC
LIMIT 10;
```

#### 7. Libri da restituire questa settimana
```sql
SELECT
    l.titolo,
    m.nome,
    m.cognome,
    p.data_scadenza
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
JOIN membri m ON p.membro_id = m.id
WHERE p.data_scadenza BETWEEN CURRENT_DATE AND CURRENT_DATE + 7
  AND p.stato IN ('in_corso', 'in_ritardo')
ORDER BY p.data_scadenza;
```

#### 8. Storico dei prestiti di un membro
```sql
SELECT
    l.titolo,
    p.data_prestito,
    p.data_restituzione,
    p.stato,
    CASE
        WHEN p.data_restituzione > p.data_scadenza THEN 'In ritardo'
        WHEN p.data_restituzione <= p.data_scadenza THEN 'In orario'
        ELSE 'Non restituito'
    END AS stato_restituzione
FROM prestiti p
JOIN libri l ON p.libro_id = l.id
WHERE p.membro_id = 1
ORDER BY p.data_prestito DESC;
```

#### 9. Statistiche annuali
```sql
SELECT
    EXTRACT(YEAR FROM data_prestito) AS anno,
    COUNT(*) AS totale_prestiti,
    COUNT(*) FILTER (WHERE stato = 'restituito') AS restituiti,
    COUNT(*) FILTER (WHERE stato = 'in_ritardo') AS in_ritardo
FROM prestiti
GROUP BY EXTRACT(YEAR FROM data_prestito)
ORDER BY anno DESC;
```

## Funzionalità Implementate

### Vincoli di Integrità

- **Primary Keys** su tutte le tabelle
- **Foreign Keys** con regole CASCADE adeguate
- **Check Constraints** per validare i dati
- **Unique Constraints** su ISBN, email, nome categoria

### Trigger e Funzioni

- `aggiorna_stato_prestiti()`: Aggiorna automaticamente i prestiti in ritardo

### Validazioni

- Email con regex pattern
- Stati predefiniti (enum-like via CHECK)
- Coerenza date (restituzione ≥ prestito, scadenza ≥ prestito)
- Coerenza copie (disponibili ≤ totali)
- Anno di pubblicazione ragionevole

### Gestione Copie

Il sistema traccia automaticamente le copie:
- `copie_totali`: numero di copie possedute
- `copie_disponibili`: copie attualmente disponibili
- Aggiornamento automatico tramite query

## Possibili Estensioni

### Funzionalità Aggiuntive da Implementare

1. **Sistema di Prenotazioni**
   - Tabella `prenotazioni` per prenotare libri non disponibili
   - Coda di attenta automatica

2. **Sistema di Sanzioni**
   - Tabella `sanzioni` per tracciare multe e sospensioni
   - Calcolo automatico sanzioni per ritardi

3. **Sistema di Recensioni**
   - Tabella `recensioni` con valutazioni (1-5 stelle)
   - Commenti testuali

4. **Gestione Magazzino**
   - Tabella `posizioni` per tracciare posizione fisica
   - Scaffold/stanza/scaffale

5. **Acquisizioni**
   - Tabella `acquisizioni` per tracciare acquisti
   - Date e costi di acquisto

6. **Statistiche Avanzate**
   - Report mensili/annuali
   - Analisi trend di lettura
   - Libri mai prestati

7. **Sistema di Notifiche**
   - Email automatiche per scadenze
   - Promemoria restituzioni

8. **Integrazione API**
   - REST API per accesso esterno
   - App mobile per membri

9. **Multi-tenant**
   - Supporto per multiple biblioteche
   - Condivisione catalogo

10. **Import/Export**
    - Importazione da MARC21
    - Esportazione statistiche in CSV/Excel

### Miglioramenti del Database

1. **Partitioning** della tabella `prestiti` per anno
2. **Materialized Views** per reportistica
3. **Full-text search** avanzata su descrizioni
4. **Audit trail** per modifiche ai dati
5. **Soft delete** invece di DELETE fisici
6. **Optimistic locking** per gestione concorrente

### Prestazioni

1. **Connection pooling** con PgBouncer
2. **Caching query** con Redis
3. **Read replicas** per query di lettura
4. **Archiviazione** prestiti storici su tabella separata

## Note Tecniche

### Best Practices Implementate

- **Nomi tabelle in italiano**: Coerente con il contesto
- **Commenti**: Ogni tabella e colonna documentata
- **Indici**: Ottimizzati per query comuni
- **Viste**: Per query frequenti e complesse
- **Constraint**: Per garantire integrità dati
- **Convenzioni**: Nome singolare per tabelle, snake_case per colonne

### Consigli per lo Sviluppo

1. **Testing**: Usare sempre transazioni per i test
   ```sql
   BEGIN;
   -- query di test
   ROLLBACK;
   ```

2. **Backup**: Implementare backup regolari
   ```bash
   pg_dump biblioteca > backup_$(date +%Y%m%d).sql
   ```

3. **Monitoring**: Monitorare query lente
   ```sql
   SELECT * FROM pg_stat_statements ORDER BY mean_exec_time DESC;
   ```

4. **Maintenance**: Eseguire regolarmente
   ```sql
   VACUUM ANALYZE;
   ```

## Autore e Licenza

Questo progetto è stato creato come esempio educativo per dimostrare le capacità di un sistema di gestione bibliotecaria implementato con PostgreSQL.

---

**Data di creazione:** Febbraio 2026
**Versione:** 1.0.0
**Database:** PostgreSQL 12+