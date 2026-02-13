# Guida Rapida - Quick Start Guide

## Installazione Veloce - Quick Installation

### 1. Installa le Dipendenze - Install Dependencies
```bash
pip install -r requirements.txt
```

Oppure manualmente - Or manually:
```bash
pip install pygame requests
```

### 2. Esegui il Programma - Run the Program
```bash
python music_player.py
```

## Primi Passi - First Steps

### Se hai file musicali - If you have music files:

1. **Avvia il programma** - Start the program
   ```bash
   python music_player.py
   ```

2. **Scansiona la tua musica** - Scan your music
   - Premi `1` nel menu
   - Inserisci il percorso della tua cartella musicale
   - Esempio: `C:/Utenti/Nome/Musica`

3. **Riproduci** - Play
   - Premi `5` per i controlli
   - Premi `1` per play

4. **Mostra i testi** - Show lyrics
   - Premi `6` mentre riproduci una canzone

### Se NON hai file musicali - If you DON'T have music files:

1. **Avvia il programma** - Start the program
   ```bash
   python music_player.py
   ```

2. **Attiva Demo Mode** - Activate Demo Mode
   - Premi `9` nel menu

3. **Testa le funzionalita** - Test features
   - Usa il menu per navigare
   - Prova a recuperare i testi (funziona davvero!)

## Comandi Principali - Main Commands

| Numero | Comando - Command | Descrizione - Description |
|--------|-------------------|---------------------------|
| 1 | Scan Directory | Scansiona cartella musicale |
| 2 | Show Playlist | Mostra canzoni nella playlist |
| 3 | Load Playlist | Carica playlist salvata |
| 4 | Save Playlist | Salva playlist corrente |
| 5 | Playback Controls | Play, pause, stop, next, prev |
| 6 | Show Lyrics | Mostra testi canzone |
| 7 | Volume | Regola volume |
| 8 | Song Info | Info canzone corrente |
| 9 | Demo Mode | Modalita demo |
| 0 | Exit | Esci dal programma |

## Scorciatoie da Tastiera - Keyboard Shortcuts

Nel menu dei controlli (opzione 5):
- `1` = Play
- `2` = Pause
- `3` = Resume
- `4` = Stop
- `5` = Next
- `6` = Previous
- `0` = Torna al menu principale

## Testare l'API Lyrics - Testing Lyrics API

Per testare il recupero dei testi senza file audio:

1. Avvia il programma
2. Premi `9` (Demo Mode)
3. Premi `6` (Show Lyrics)
4. Il sistema cerchera i testi delle canzoni demo

Le canzoni demo sono:
- Queen - Bohemian Rhapsody
- John Lennon - Imagine
- Eagles - Hotel California

## Problemi Comuni - Common Issues

### "Nessun file audio trovato"
**Soluzione**: Specifica il percorso corretto con l'opzione 1, oppure usa Demo Mode (opzione 9)

### "Impossibile inizializzare pygame"
**Soluzione**: Installa pygame: `pip install pygame`

### "Impossibile recuperare i testi"
**Causa**: API non ha i testi o artista/titolo non corretto
**Soluzione**: Prova canzoni piu famose

### Il programma non si avvia
**Soluzione**: Assicurati di avere Python 3.7+ e tutte le dipendenze installate

## Struttura File - File Structure

```
music-player/
├── music_player.py      # Programma principale - Main program
├── example_usage.py     # Esempi di utilizzo - Usage examples
├── requirements.txt     # Dipendenze - Dependencies
├── config.json         # Configurazione - Configuration
├── README.md           # Documentazione completa - Full docs
├── playlists/          # Playlist salvate - Saved playlists
└── QUICKSTART.md       # Questo file - This file
```

## Per Saperne di Piu - Learn More

Leggi il README.md completo per:
- Dettagli tecnici
- Spiegazione delle funzioni
- Personalizzazione
- Troubleshooting avanzato
- Progetti di espansione

## Divertimento - Have Fun!

Questo progetto e stato creato per scopi educativi.
Sentiti libero di modificarlo e migliorarlo!

This project was created for educational purposes.
Feel free to modify and improve it!

Buon ascolto! - Enjoy your music!
