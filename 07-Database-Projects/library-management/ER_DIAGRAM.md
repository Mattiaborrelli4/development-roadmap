# Diagramma ER - Sistema di Gestione Bibliotecaria

## Rappresentazione Testuale del Diagramma ER

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      SISTEMA DI GESTIONE BIBLIOTECA                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────┐
│   EDITORI       │
├─────────────────┤
│ *id (PK)       │────────────┐
│  nome          │            │
│  indirizzo     │            │
│  telefono      │            │
│  email         │            │
│  created_at    │            │
└─────────────────┘            │
                              │
                              │ published_by (N:1)
                              │
┌─────────────────────────────┴──────────────────────────────────┐
│                           LIBRI                               │
├────────────────────────────────────────────────────────────────┤
│ *id (PK)                                                   │  │
│  titolo                                                    │  │
│  isbn                                                      │  │
│  anno_pubblicazione                                        │  │
│  editore_id (FK) ────────────────────────────────────────┘  │
│  categoria_id (FK) ────────┐                                 │
│  copie_totali            │                                 │
│  copie_disponibili       │                                 │
│  descrizione             │                                 │
│  lingua                  │                                 │
│  created_at              │                                 │
└──────────────────────────┼─────────────────────────────────┘
                           │
                           │ categorized_by (N:1)
                           │
                           ▼
                 ┌─────────────────┐
                 │   CATEGORIE     │
                 ├─────────────────┤
                 │ *id (PK)       │
                 │  nome          │
                 │  descrizione   │
                 │  created_at    │
                 └─────────────────┘

┌─────────────────┐
│    AUTORI      │
├─────────────────┤
│ *id (PK)       │
│  nome          │
│  anno_nascita  │
│  anno_morte    │
│  biografia     │
│  nazionalita   │
│  created_at    │
└───────┬────────┘
        │
        │
        │ written_by (M:N)
        │
        │
┌───────┴──────────────────────────────┐
│        LIBRI_AUTORI (Junction)        │
├───────────────────────────────────────┤
│ *libro_id (FK → libri.id)            │
│ *autore_id (FK → autori.id)          │
│  created_at                          │
└───────────────────────────────────────┘

┌─────────────────┐
│    MEMBRI      │
├─────────────────┤
│ *id (PK)       │
│  nome          │
│  cognome       │
│  email         │
│  telefono      │
│  data_iscrizione│
│  stato         │
│  note          │
│  created_at    │
└───────┬────────┘
        │
        │ borrowed_by (1:N)
        │
        │
┌───────┴──────────────────────────────┐
│           PRESTITI                  │
├──────────────────────────────────────┤
│ *id (PK)                            │
│  libro_id (FK → libri.id)           │
│  membro_id (FK → membri.id)         │
│  data_prestito                      │
│  data_scadenza                      │
│  data_restituzione                  │
│  stato                              │
│  note                               │
│  created_at                         │
└──────────────────────────────────────┘
        │
        │ borrowed_in (N:1)
        │
        └──────────────────┐
                           │
                           ▼
                 (riferimento a LIBRI)
```

## Legenda

- `*` = Primary Key (Chiave Primaria)
- `FK` = Foreign Key (Chiave Esterna)
- `(1:N)` = Relazione uno-a-molti
- `(M:N)` = Relazione molti-a-molti
- `─→` = Direzione della relazione

## Relazioni Dettagliate

### 1. libri → editori (N:1)
**Descrizione:** Ogni libro è pubblicato da un solo editore, ma un editore può pubblicare molti libri.

**Foreign Key:** `libri.editore_id → editori.id`
**Regola:** ON DELETE RESTRICT (non cancellare se ci sono libri associati)

### 2. libri → categorie (N:1)
**Descrizione:** Ogni libro appartiene a una sola categoria, ma una categoria contiene molti libri.

**Foreign Key:** `libri.categoria_id → categorie.id`
**Regola:** ON DELETE RESTRICT (non cancellare se ci sono libri associati)

### 3. libri ↔ autori (M:N)
**Descrizione:** Un libro può avere più autori, e un autore può scrivere più libri.

**Tabella di Giunzione:** `libri_autori`
**Foreign Keys:**
- `libri_autori.libro_id → libri.id`
- `libri_autori.autore_id → autori.id`
**Regola:** ON DELETE CASCADE (cascata su entrambi i lati)

### 4. membri → prestiti (1:N)
**Descrizione:** Un membro può effettuare molti prestiti, ma ogni prestito appartiene a un solo membro.

**Foreign Key:** `prestiti.membro_id → membri.id`
**Regola:** ON DELETE RESTRICT (non cancellare se ci sono prestiti attivi)

### 5. libri → prestiti (1:N)
**Descrizione:** Un libro può essere prestato molte volte, ma ogni prestito riguarda un solo libro.

**Foreign Key:** `prestiti.libro_id → libri.id`
**Regola:** ON DELETE RESTRICT (non cancellare se ci sono prestiti attivi)

## Vincoli e Regole di Business

### Vincoli di Integrità

#### Tabella libri
```sql
-- Le copie disponibili non possono superare le copie totali
CHECK (copie_disponibili <= copie_totali)

-- Anno di pubblicazione ragionevole
CHECK (anno_pubblicazione >= 1000 AND anno_pubblicazione <= EXTRACT(YEAR FROM CURRENT_DATE) + 1)
```

#### Tabella autori
```sql
-- Anno di morte non precedente all'anno di nascita
CHECK (anno_morte IS NULL OR anno_morte >= anno_nascita)
```

#### Tabella membri
```sql
-- Email deve essere valida
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

-- Stato può essere solo uno dei valori specificati
CHECK (stato IN ('attivo', 'sospeso', 'inattivo'))
```

#### Tabella prestiti
```sql
-- Data restituzione non precedente al prestito
CHECK (data_restituzione IS NULL OR data_restituzione >= data_prestito)

-- Data scadenza non precedente al prestito
CHECK (data_scadenza >= data_prestito)

-- Stato può essere solo uno dei valori specificati
CHECK (stato IN ('in_corso', 'restituito', 'in_ritardo', 'perso'))
```

### Regole di Business

1. **Gestione Copie**
   - Quando si crea un prestito: `copie_disponibili--`
   - Quando si restituisce: `copie_disponibili++`
   - Non puoi creare un prestito se `copie_disponibili = 0`

2. **Stato Prestiti**
   - `in_corso`: Prestito attivo entro la data di scadenza
   - `in_ritardo`: Prestito attivo oltre la data di scadenza
   - `restituito`: Libro restituito
   - `perso`: Libro perso (da gestire manualmente)

3. **Stato Membri**
   - `attivo`: Può effettuare prestiti
   - `sospeso`: Non può effettuare prestiti (es. troppi ritardi)
   - `inattivo`: Membro disattivato

## Cardinalità

| Entità 1 | Relazione | Entità 2 | Cardinalità |
|----------|-----------|----------|-------------|
| libri | pubblicato da | editori | N:1 |
| libri | appartiene a | categorie | N:1 |
| libri | scritto da | autori | M:N |
| membri | prende in prestito | libri | M:N (tramite prestiti) |
| membri | effettua | prestiti | 1:N |
| libri | oggetto di | prestiti | 1:N |

## Normalizzazione

Il database è normalizzato fino alla **Terza Forma Normale (3NF)**:

1. **1NF:** Tutti i valori sono atomici
2. **2NF:** Tutti gli attributi non-chiave dipendono interamente dalla chiave primaria
3. **3NF:** Non ci sono dipendenze transitive

### Esempio di Normalizzazione

Invece di memorizzare l'autore direttamente nella tabella libri:

```
❌ NON NORMALIZZATO:
libri (id, titolo, autore1, autore2, editore, categoria, ...)

✅ NORMALIZZATO:
libri (id, titolo, editore_id, categoria_id, ...)
autori (id, nome, biografia, ...)
libri_autori (libro_id, autore_id)
```

## Indici per Performance

### Indici Primary Key
- Tutti gli id SERIAL hanno automaticamente un indice

### Indici Foreign Key
```sql
editori: nome
categorie: nome
autori: nome, nazionalita
membri: cognome, email, stato
libri: titolo, isbn, categoria_id, editore_id, copie_disponibili
prestiti: libro_id, membro_id, stato, data_prestito, data_scadenza
```

### Indici Composite
```sql
membri: (nome, cognome)
prestiti: (membro_id, stato) WHERE stato IN ('in_corso', 'in_ritardo')
```

### Full-Text Search
```sql
libri: titolo_fts (gin index su to_tsvector('italian', titolo))
```

## Query Pattern Comuni

### 1. Lista libri con autori (JOIN)
```sql
SELECT l.titolo, STRING_AGG(a.nome, ', ') AS autori
FROM libri l
LEFT JOIN libri_autori la ON l.id = la.libro_id
LEFT JOIN autori a ON la.autore_id = a.id
GROUP BY l.id;
```

### 2. Prestiti attuali (WHERE)
```sql
SELECT * FROM prestiti
WHERE stato IN ('in_corso', 'in_ritardo');
```

### 3. Libri per categoria (GROUP BY)
```sql
SELECT c.nome, COUNT(l.id)
FROM categorie c
LEFT JOIN libri l ON c.id = l.categoria_id
GROUP BY c.nome;
```

### 4. Libri più popolari (ORDER BY + COUNT)
```sql
SELECT l.titolo, COUNT(p.id)
FROM libri l
JOIN prestiti p ON l.id = p.libro_id
GROUP BY l.titolo
ORDER BY COUNT(p.id) DESC;
```

## Viste Materializzate Suggerite

Per ottimizzare le performance, potresti creare:

### 1. Statistiche Popolarità Libri
```sql
CREATE MATERIALIZED VIEW mv_libri_popolari AS
SELECT
    l.id,
    l.titolo,
    COUNT(p.id) AS numero_prestiti,
    AVG(p.data_restituzione - p.data_prestito) AS media_giorni
FROM libri l
LEFT JOIN prestiti p ON l.id = p.libro_id
GROUP BY l.id, l.titolo;
```

### 2. Report Mensile
```sql
CREATE MATERIALIZED VIEW mv_report_mensile AS
SELECT
    EXTRACT(YEAR FROM data_prestito) AS anno,
    EXTRACT(MONTH FROM data_prestito) AS mese,
    COUNT(*) AS prestiti,
    COUNT(DISTINCT membro_id) AS membri_attivi
FROM prestiti
GROUP BY anno, mese;
```

---

**Nota:** Ricorda di aggiornare le viste materializzate periodicamente:
```sql
REFRESH MATERIALIZED VIEW mv_libri_popolari;
```