# Guida Rapida - Sistema Bibliotecario

## Comandi PostgreSQL Essenziali

### Connessione al Database
```bash
psql -U postgres -d biblioteca
```

### Esecuzione Script
```sql
\i schema.sql
\i sample_data.sql
```

### Comandi Utili
```sql
-- Mostra tutte le tabelle
\dt

-- Descrivi una tabella
\d libri

-- Esci
\q

-- Mostra i primi 20 record
SELECT * FROM libri LIMIT 20;

-- Formatta output
\x on
```

## Query Più Richieste

### Libri Disponibili
```sql
SELECT titolo, autore, copie_disponibili
FROM vista_libri_dettagli
WHERE copie_disponibili > 0
ORDER BY titolo;
```

### Prestiti in Ritardo
```sql
SELECT * FROM vista_prestiti_attuali
WHERE stato_prestito = 'IN RITARDO';
```

### Libri per Autore
```sql
SELECT * FROM vista_libri_dettagli
WHERE autori ILIKE '%orwell%';
```

### Top 10 Libri Più Prestati
```sql
SELECT titolo, numero_prestiti FROM (
    SELECT
        l.titolo,
        COUNT(p.id) AS numero_prestiti,
        RANK() OVER (ORDER BY COUNT(p.id) DESC) AS rank
    FROM libri l
    JOIN prestiti p ON l.id = p.libro_id
    GROUP BY l.titolo
) t WHERE rank <= 10;
```

## Statistiche Veloci

```sql
-- Totale libri nel catalogo
SELECT COUNT(*) AS totale_libri FROM libri;

-- Totale membri attivi
SELECT COUNT(*) AS membri_attivi FROM membri WHERE stato = 'attivo';

-- Prestiti attivi
SELECT COUNT(*) AS prestiti_in_corso FROM prestiti WHERE stato = 'in_corso';

-- Prestiti in ritardo
SELECT COUNT(*) AS prestiti_in_ritardo FROM prestiti WHERE stato = 'in_ritardo';

-- Libri disponibili
SELECT SUM(copie_disponibili) AS copie_disponibili FROM libri;
```

## Operazioni Comuni

### Aggiungere un Nuovo Libro
```sql
INSERT INTO libri (titolo, isbn, anno_pubblicazione, editore_id, categoria_id, copie_totali, copie_disponibili)
VALUES ('Nuovo Libro', '9781234567890', 2024, 1, 1, 2, 2);

-- Aggiungi autori
INSERT INTO libri_autori (libro_id, autore_id) VALUES ((SELECT MAX(id) FROM libri), 1);
```

### Creare un Nuovo Prestito
```sql
INSERT INTO prestiti (libro_id, membro_id, data_scadenza)
VALUES (1, 1, CURRENT_DATE + 30);

-- Aggiorna copie disponibili
UPDATE libri SET copie_disponibili = copie_disponibili - 1 WHERE id = 1;
```

### Restituire un Libro
```sql
UPDATE prestiti
SET data_restituzione = CURRENT_DATE, stato = 'restituito'
WHERE id = 123;

-- Aggiorna copie disponibili
UPDATE libri SET copie_disponibili = copie_disponibili + 1 WHERE id = 1;
```

### Registrare un Nuovo Membro
```sql
INSERT INTO membri (nome, cognome, email, telefono)
VALUES ('Mario', 'Rossi', 'mario.rossi@email.com', '333 1234567');
```

## Risoluzione Problemi

### Trovare Libri senza Copie Disponibili
```sql
SELECT titolo, copie_totali FROM libri WHERE copie_disponibili = 0;
```

### Trovare Membri con Troppi Prestiti in Ritardo
```sql
SELECT
    m.nome,
    m.cognome,
    COUNT(*) AS prestiti_in_ritardo
FROM membri m
JOIN prestiti p ON m.id = p.membro_id
WHERE p.stato = 'in_ritardo'
GROUP BY m.id, m.nome, m.cognome
HAVING COUNT(*) >= 3;
```

### Libri Mai Prestati
```sql
SELECT titolo FROM libri
WHERE id NOT IN (SELECT DISTINCT libro_id FROM prestiti);
```

## Backup e Ripristino

### Backup del Database
```bash
pg_dump -U postgres biblioteca > backup_biblioteca.sql
```

### Ripristino del Database
```bash
psql -U postgres biblioteca < backup_biblioteca.sql
```

### Backup Solo Dati
```bash
pg_dump -U postgres -a biblioteca > backup_dati.sql
```

## Query di Manutenzione

### Aggiorna Stati Prestiti
```sql
SELECT aggiorna_stato_prestiti();
```

### Vacuum e Analyze
```sql
VACUUM ANALYZE;
```

### Reindex
```sql
REINDEX DATABASE biblioteca;
```

## Visualizzazioni Utili

### Statistiche Complete
```sql
SELECT * FROM vista_statistiche_categorie;
```

### Prestiti Attuali
```sql
SELECT * FROM vista_prestiti_attuali ORDER BY data_scadenza;
```

### Catalogo Completo
```sql
SELECT * FROM vista_libri_dettagli ORDER BY titolo;
```

---

**Tip:** Usa le viste (`vista_*`) invece delle tabelle per query più semplici e performanti!