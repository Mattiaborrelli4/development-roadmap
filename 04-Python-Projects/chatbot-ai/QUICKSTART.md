# GUIDA RAPIDA - Chatbot AI

## Come Avviare il Chatbot

### Metodo 1: Esecuzione Diretta
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\chatbot-ai"
python chatbot.py
```

### Metodo 2: Esegui i Test
```bash
python test_chatbot.py
```

### Metodo 3: Vedi la Demo
```bash
python demo.py
```

## Comandi During Conversazione

| Comando | Descrizione |
|---------|-------------|
| `ciao` | Saluta il chatbot |
| `come ti chiami` | Chiede il nome del chatbot |
| `raccontami una barzelletta` | Ricevi una barzelletta |
| `che tempo fa` | Chiedi informazioni meteo |
| `ultime notizie` | Chiedi notizie |
| `grazie` | Ringrazia il chatbot |
| `aiuto` | Mostra aiuto |
| `statistiche` | Mostra statistiche conversazione |
| `impara` | Insegna nuovi pattern |
| `esci` | Termina conversazione |

## Esempio di Sessione

```
Chatbot: Ciao! Sono il tuo assistente virtuale. Come posso aiutarti?

Tu: ciao
Chatbot: Ciao! Come posso aiutarti oggi?

Tu: raccontami una barzelletta
Chatbot: Perché i programmatori preferiscono il mode scuro?
         Perché la luce attira i bug!

Tu: impara
[Modalità apprendimento attivata]
```

## Modalità Apprendimento

Quando usi il comando `impara`:

1. Inserisci il pattern (es: "qual è la capitale")
2. Inserisci l'intento (es: "geografia")
3. Inserisci la risposta (es: "La capitale dell'Italia è Roma!")

Il chatbot impara e salva automaticamente!

## File Generati

- `training_data.json` - Dati di training
- `learned_data.json` - Nuovi pattern appresi (creato dopo primo apprendimento)

## Troubleshooting

### Problema: Il chatbot non risponde
- Verifica che `training_data.json` esista
- Il file viene creato automaticamente alla prima esecuzione

### Problema: Errori di codifica
- Assicurati che i file siano salvati in UTF-8

### Problema: Pattern non riconosciuti
- Usa la modalità `impara` per aggiungere nuovi pattern
- Più pattern aggiungi, più intelligente diventa!

## Personalizzazione

### Aggiungere Intenti nel JSON

Modifica `training_data.json`:

```json
{
  "mio_intent": {
    "patterns": ["\\b(parola1|parola2)\\b.*"],
    "responses": ["Risposta 1", "Risposta 2"]
  }
}
```

### Modificare Stopword

Nel file `chatbot.py`, modifica la lista `stopword`:

```python
stopword = {"il", "la", "di", "a", ...}
```

## Suggerimenti per Studenti

1. **Sperimenta**: Prova diversi input per vedere come risponde
2. **Impara**: Usa la modalità apprendimento per insegnare al chatbot
3. **Analizza**: Studia il codice per capire come funziona
4. **Modifica**: Aggiungi nuovi intenti e risposte
5. **Testa**: Usa `test_chatbot.py` per verificare le modifiche

## Concetti Chiave

- **Pattern Matching**: Regex per riconoscere gli intenti
- **Confidenza**: Punteggio di quanto bene il pattern corrisponde
- **Contesto**: Memoria degli ultimi 3 messaggi
- **Entità**: Parole chiave estratte dall'input
- **Apprendimento**: Aggiunta dinamica di nuovi pattern

## Risorse Online

- [Python Regex](https://docs.python.org/3/library/re.html)
- [JSON in Python](https://docs.python.org/3/library/json.html)
- [Python OOP](https://docs.python.org/3/tutorial/classes.html)

Buon divertimento con il chatbot!
