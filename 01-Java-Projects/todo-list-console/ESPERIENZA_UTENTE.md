# 📖 Esempio di Esperienza Utente

Questo documento mostra come appare e funziona l'applicazione TodoListApp.

## 💡 Sessione Esempio

### Avvio dell'Applicazione

```
===========================================
   BENVENUTO NELLA LISTA ATTIVITA'
===========================================

===========================================
                MENU PRINCIPALE
===========================================
1. Aggiungi nuova attivita'
2. Rimuovi attivita'
3. Visualizza tutte le attivita'
4. Visualizza attivita' per priorita'
5. Salva attivita' su file
6. Esci e salva
7. Ricarica attivita' dal file
===========================================

La tua scelta:
```

### Aggiunta di Attività

```
La tua scelta: 1

--- AGGIUNGI NUOVA ATTIVITA' ---
Descrizione attivita': Studiare per l'esame di programmazione
Priorita' (1=ALTA, 2=MEDIA, 3=BASSA): 1

[OK] Attivita' aggiunta con successo!
    Attivita': Studiare per l'esame di programmazione
    Priorita': ALTA
```

### Aggiunta di Altre Attività

```
La tua scelta: 1

--- AGGIUNGI NUOVA ATTIVITA' ---
Descrizione attivita': Comprare il latte
Priorita' (1=ALTA, 2=MEDIA, 3=BASSA): 3

[OK] Attivita' aggiunta con successo!
    Attivita': Comprare il latte
    Priorita': BASSA
```

```
La tua scelta: 1

--- AGGIUNGI NUOVA ATTIVITA' ---
Descrizione attivita': Inviare email al professore
Priorita' (1=ALTA, 2=MEDIA, 3=BASSA): 2

[OK] Attivita' aggiunta con successo!
    Attivita': Inviare email al professore
    Priorita': MEDIA
```

### Visualizzazione Tutte le Attività

```
La tua scelta: 3

--- TUTTE LE ATTIVITA' (3) ---
------------------------------------------------
N.    ATTIVITA'                      PRIORITA'
------------------------------------------------
1     Studiare per l'esame di progra ALTA
2     Comprare il latte                BASSA
3     Inviare email al professore     MEDIA
------------------------------------------------
```

### Visualizzazione per Priorità

```
La tua scelta: 4

--- ATTIVITA' ORDINATE PER PRIORITA' ---
------------------------------------------------
N.    ATTIVITA'                      PRIORITA'
------------------------------------------------
1     Studiare per l'esame di progra ALTA
2     Inviare email al professore     MEDIA
3     Comprare il latte                BASSA
------------------------------------------------
```

### Rimozione di un'Attività

```
La tua scelta: 2

--- RIMUOVI ATTIVITA' ---
--- TUTTE LE ATTIVITA' (3) ---
------------------------------------------------
N.    ATTIVITA'                      PRIORITA'
------------------------------------------------
1     Studiare per l'esame di progra ALTA
2     Comprare il latte                BASSA
3     Inviare email al professore     MEDIA
------------------------------------------------

Numero dell'attivita' da rimuovere: 2

[OK] Attivita' rimossa: Comprare il latte
```

### Salvataggio su File

```
La tua scelta: 5

Attivita' salvate con successo!
```

### Uscita dall'Applicazione

```
La tua scelta: 6

Attivita' salvate con successo!

Arrivederci! Alla prossima!
```

## 📄 Contenuto di tasks.txt

Dopo l'esecuzione precedente, il file `tasks.txt` conterrà:

```
Studiare per l'esame di programmazione|1
Inviare email al professore|2
```

Formato: `descrizione_attivita|priorita`

## ⚠️ Gestione degli Errori

### Input Non Valido

```
La tua scelta: abc

[!] Errore: Inserisci un numero valido.
```

### Attività Già Esistente

```
--- AGGIUNGI NUOVA ATTIVITA' ---
Descrizione attivita': Studiare per l'esame di programmazione
Priorita' (1=ALTA, 2=MEDIA, 3=BASSA): 1

[!] Questa attivita' esiste gia'!
```

### Descrizione Vuota

```
--- AGGIUNGI NUOVA ATTIVITA' ---
Descrizione attivita':
[!] La descrizione non puo' essere vuota.
```

### Priorità Non Valida

```
--- AGGIUNGI NUOVA ATTIVITA' ---
Descrizione attivita': Nuova attività
Priorita' (1=ALTA, 2=MEDIA, 3=BASSA): 5

[!] Priorita' non valida. Usa 1, 2 o 3.
```

### Indice Non Valido

```
--- RIMUOVI ATTIVITA' ---
Numero dell'attivita' da rimuovere: 99

[!] Numero non valido.
```

### Lista Vuota

```
La tua scelta: 3

--- TUTTE LE ATTIVITA' (0) ---
Nessuna attivita' presente.
```

## 🔄 Workflow Tipico

1. **Avvio** → L'applicazione carica automaticamente le attività salvate
2. **Aggiungi** → Inserisci nuove attività con priorità
3. **Visualizza** → Controlla le attività in ordine o per priorità
4. **Rimuovi** → Elimina attività completate
5. **Salva** → Salva periodicamente per non perdere dati
6. **Esci** → Salva automaticamente e chiudi

## 💪 Suggerimenti per l'Uso

- Usa priorità **1 (ALTA)** per scadenze urgenti
- Usa priorità **2 (MEDIA)** per attività importanti ma non urgenti
- Usa priorità **3 (BASSA)** per attività da fare quando possibile
- Salva frequentemente (opzione 5) durante lunghe sessioni
- Usa la visualizzazione per priorità (opzione 4) per pianificare la giornata

---

**Divertiti a organizzare le tue attività!** 📋
