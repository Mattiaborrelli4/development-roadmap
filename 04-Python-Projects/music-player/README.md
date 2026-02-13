# Riproduttore Musicale con Testi - Music Player with Lyrics

Un semplice ma completo riproduttore musicale in Python con supporto per playlist e recupero automatico dei testi delle canzoni.

A simple but complete music player in Python with playlist support and automatic lyrics fetching.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Caratteristiche - Features

### Core Features
- **Riproduzione Audio**: Supporto per MP3, WAV, OGG, FLAC tramite pygame
- **Gestione Playlist**: Crea, salva e carica playlist in formato JSON
- **Testi delle Canzoni**: Recupero automatico dei testi dall'API Lyrics.ovh (gratuita, senza chiave)
- **Metadati**: Estrazione automatica di artista, titolo e album dai tag ID3
- **Controlli di Riproduzione**: Play, pause, resume, stop, next, previous
- **Controllo Volume**: Regolazione volume con incremento/decremento o valore specifico

### Interface Features
- **Menu Testuale**: Interfaccia semplice e intuitiva in Italiano
- **ASCII-only**: Compatibile con Windows (nessun emoji)
- **Modalita Demo**: Testa l'interfaccia anche senza file musicali
- **Persistenza Configurazione**: Salva automaticamente le impostazioni
- **Gestione Errori**: Robusta gestione degli errori con messaggi chiari

## Requisiti - Requirements

### Librerie Python - Python Libraries
```bash
pip install pygame requests
```

### Opzionale - Optional (per metadati completi)
```bash
pip install mutagen
```

### Sistema Operativo
- Windows 10/11
- Linux
- macOS

## Installazione - Installation

1. **Clona o scarica il progetto**
   ```bash
   cd music-player
   ```

2. **Installa le dipendenze**
   ```bash
   pip install pygame requests
   ```

3. **Esegui il programma**
   ```bash
   python music_player.py
   ```

## Struttura del Progetto - Project Structure

```
music-player/
|-- music_player.py          # File principale del programma
|-- playlists/              # Directory per le playlist salvate
|-- config.json             # File di configurazione (generato automaticamente)
|-- README.md               # Questo file
```

## Utilizzo - Usage

### Menu Principale

```
1. Scansiona directory musica
   - Specifica una directory per cercare file musicali
   - Crea automaticamente una playlist con i file trovati

2. Mostra playlist corrente
   - Visualizza tutte le canzoni nella playlist corrente
   - Indica la canzone attualmente in riproduzione

3. Carica playlist salvata
   - Carica una playlist precedentemente salvata

4. Salva playlist corrente
   - Salva la playlist corrente su disco

5. Controlli riproduzione
   - Play: Avvia la riproduzione
   - Pause: Mette in pausa
   - Resume: Riprende dalla pausa
   - Stop: Ferma la riproduzione
   - Next: Prossima canzone
   - Previous: Canzone precedente

6. Mostra testi canzone
   - Recupera e mostra i testi della canzone corrente
   - Utilizza l'API gratuita Lyrics.ovh

7. Gestione volume
   - Aumenta/diminuisci volume
   - Imposta valore specifico (0-100)

8. Info canzone corrente
   - Mostra dettagli sulla canzone in riproduzione

9. Demo mode
   - Modalita demo con dati finti per testare l'interfaccia
   - Utile se non hai file musicali

0. Esci
   - Chiude il programma
```

### Esempio di Utilizzo

```
1. Avvia il programma
   >> python music_player.py

2. Scansiona la tua directory musicale
   >> Seleziona: 1
   >> Inserisci percorso: C:/Utenti/Nome/Musica

3. Riproduci una canzone
   >> Seleziona: 5 (Controlli riproduzione)
   >> Seleziona: 1 (Play)

4. Mostra i testi
   >> Seleziona: 6 (Mostra testi canzone)

5. Regola il volume
   >> Seleziona: 7 (Gestione volume)
   >> Seleziona: 1 (Aumenta)
```

## Funzioni Principali - Main Functions

### Classe MusicPlayer

#### Gestione File
- `scan_music_directory(path)` - Scansiona directory per file audio
- `get_metadata(file_path)` - Estrae metadati dai tag ID3

#### Controlli Riproduzione
- `play_song(file_path=None)` - Riproduce un file
- `pause_song()` - Mette in pausa
- `resume_song()` - Riprende la riproduzione
- `stop_song()` - Ferma tutto
- `next_song()` - Prossima canzone
- `previous_song()` - Canzone precedente

#### Gestione Playlist
- `create_playlist(name, files)` - Crea nuova playlist
- `save_playlist(playlist)` - Salva su disco
- `load_playlist(name)` - Carica da disco
- `display_current_playlist()` - Mostra playlist

#### Testi
- `fetch_lyrics(artist, title)` - Recupera testi da API
- `display_lyrics(lyrics)` - Mostra testi formattati

#### Configurazione
- `_load_config()` - Carica configurazione da JSON
- `_save_config()` - Salva configurazione

## API Lyrics

Il progetto utilizza l'API **Lyrics.ovh** che e:
- **Gratuita**: Nessun costo
- **Senza Registrazione**: Non necessita di API key
- **Semplice**: REST API con JSON response

Esempio di chiamata API:
```
GET https://api.lyrics.ovh/v1/{artist}/{title}
```

## Dettagli Tecnici - Technical Details

### Pygame Mixer
- Frequenza di campionamento: 44100 Hz
- Canali: 2 (stereo)
- Buffer: 512 samples
- Supporto formati: MP3, WAV, OGG, FLAC

### Gestione Errori
- Try-except su tutte le operazioni I/O
- Gestione errori di rete per API lyrics
- Validazione input utente
- Messaggi di errore in Italiano/Inglese

### Encoding
- UTF-8 per file JSON
- Supporto caratteri speciali nei nomi file
- Gestione sicura dei percorsi (Windows/Linux/Mac)

## Personalizzazione - Customization

### Modificare la Directory Musicale Predefinita

Modifica la costante `DEFAULT_CONFIG` in `music_player.py`:

```python
DEFAULT_CONFIG = {
    'volume': 0.7,
    'music_directory': 'C:/La/Tua/Directory/Musica',  # Modifica qui
    'current_playlist': None,
    'shuffle': False,
    'repeat': False
}
```

### Aggiungere Nuovi Formati Audio

Aggiungi alla lista `AUDIO_EXTENSIONS`:

```python
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']
```

## Troubleshooting

### Problema: "Nessun file audio trovato"
- **Soluzione**: Usa l'opzione 1 per specificare il percorso corretto della tua directory musicale
- **Alternativa**: Usa la modalita demo (opzione 9) per testare l'interfaccia

### Problema: "Impossibile inizializzare pygame"
- **Soluzione**: Installa pygame: `pip install pygame`
- **Nota**: Su alcuni sistemi potrebbe essere necessario installare i driver audio

### Problema: "Impossibile recuperare i testi"
- **Causa**: L'API Lyrics.ovh potrebbe non avere i testi per quella canzone
- **Soluzione**: Prova con canzoni piu famose o verifica artista/titolo

### Problema: I metadati non vengono letti correttamente
- **Soluzione**: Installa mutagen: `pip install mutagen`
- **Nota**: Senza mutagen, il programma usa il nome del file

## Concetti Educativi - Educational Concepts

Questo progetto insegna:

1. **Programmazione a Oggetti**: Uso di classi e metodi
2. **Gestione File**: Lettura/scrittura file e directory
3. **JSON**: Serializzazione e deserializzazione dati
4. **API REST**: Chiamate HTTP a servizi esterni
5. **Pygame**: Audio playback e gestione multimediale
6. **Gestione Errori**: Try-except e validazione
7. **Path Handling**: Percorsi cross-platform con pathlib
8. **Type Hints**: Type hints Python per migliore chiarezza
9. **Docstrings**: Documentazione codice in Italiano

## Progetti di Espansione - Expansion Projects

Idee per migliorare il player:

1. **Riproduzione Casuale**: Shuffle mode
2. **Ripetizione**: Loop su playlist/canzone
3. **Visualizzatore Audio**: Visualizzazione waveform in ASCII
4. **Radio Streaming**: Supporto stream online
5. **Database**: SQLite per salvare preferiti
6. **GUI**: Interfaccia grafica con Tkinter
7. **Hotkeys**: Controlli da tastiera globale
8. **Equalizzatore**: Controllo frequenze audio
9. **Download Testi**: Salvataggio testi localmente
10. **Search**: Ricerca canzoni per artista/titolo

## Licenza - License

Questo progetto e educational e open source. Sentiti libero di usarlo, modificarlo e condividerlo.

This is an educational and open-source project. Feel free to use, modify, and share it.

## Autore - Author

Creato per studenti universitari principianti come progetto educativo Python.

Created for beginner university students as an educational Python project.

## Supporto - Support

Per domande o problemi:
1. Controlla la sezione Troubleshooting
2. Leggi i commenti nel codice (tutti in Italiano)
3. Verifica di aver installato tutte le dipendenze

Buon divertimento con la musica! - Enjoy your music!
