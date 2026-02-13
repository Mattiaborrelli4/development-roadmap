#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Riproduttore Musicale con Testi - Music Player with Lyrics
=========================================================

Un semplice player musicale in Python con supporto per playlist e fetch dei testi.
Utilizza pygame per la riproduzione audio e l'API Lyrics.ovh per i testi.

A simple music player in Python with playlist support and lyrics fetching.
Uses pygame for audio playback and Lyrics.ovh API for lyrics.

Autore: Claude
Target: Studenti universitari principianti
Linguaggio: Python 3.7+
"""

import os
import sys
import json
import time
import pygame
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple


# ============================================================================
# COSTANTI E CONFIGURAZIONE - CONSTANTS AND CONFIGURATION
# ============================================================================

# Estensioni audio supportate - Supported audio extensions
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.flac']

# Percorsi di base - Base paths
BASE_DIR = Path(__file__).parent
PLAYLISTS_DIR = BASE_DIR / 'playlists'
CONFIG_FILE = BASE_DIR / 'config.json'

# API Lyrics - Lyrics API
LYRICS_API_BASE = "https://api.lyrics.ovh/v1"

# Configurazione predefinita - Default configuration
DEFAULT_CONFIG = {
    'volume': 0.7,
    'music_directory': str(Path.home() / 'Music'),
    'current_playlist': None,
    'shuffle': False,
    'repeat': False
}


# ============================================================================
# CLASSE PRINCIPALE - MAIN CLASS
# ============================================================================

class MusicPlayer:
    """
    Classe principale del riproduttore musicale.
    Gestisce la riproduzione, le playlist e i testi.

    Main music player class.
    Manages playback, playlists, and lyrics.
    """

    def __init__(self):
        """Inizializza il riproduttore musicale - Initialize the music player."""
        print("Inizializzazione del riproduttore musicale...")
        print("Initializing music player...\n")

        # Inizializza pygame mixer - Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            print("[OK] Pygame mixer inizializzato")
        except pygame.error as e:
            print(f"[ERRORE] Impossibile inizializzare pygame: {e}")
            print("[ERROR] Failed to initialize pygame: {e}")
            sys.exit(1)

        # Carica configurazione - Load configuration
        self.config = self._load_config()

        # Imposta volume iniziale - Set initial volume
        pygame.mixer.music.set_volume(self.config['volume'])

        # Stato del player - Player state
        self.current_playlist: List[Dict] = []  # Lista di canzoni - List of songs
        self.current_index: int = 0  # Indice canzone corrente - Current song index
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.current_file: Optional[str] = None

        # Crea directory playlist se non esiste - Create playlist directory if not exists
        PLAYLISTS_DIR.mkdir(exist_ok=True)

        print("[OK] Riproduttore pronto!\n")

    # ========================================================================
    # GESTIONE CONFIGURAZIONE - CONFIGURATION MANAGEMENT
    # ========================================================================

    def _load_config(self) -> Dict:
        """
        Carica la configurazione dal file JSON.
        Se non esiste, crea uno nuovo con la configurazione predefinita.

        Load configuration from JSON file.
        If it doesn't exist, create a new one with default configuration.

        Returns:
            Dict: Configurazione caricata - Loaded configuration
        """
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Assicura che tutte le chiavi esistano - Ensure all keys exist
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"[ATTENZIONE] Errore nel caricamento config: {e}")
                print("[WARNING] Error loading config: {e}")
                return DEFAULT_CONFIG.copy()
        else:
            return DEFAULT_CONFIG.copy()

    def _save_config(self) -> None:
        """
        Salva la configurazione corrente nel file JSON.

        Save current configuration to JSON file.
        """
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"[ERRORE] Impossibile salvare la configurazione: {e}")
            print("[ERROR] Failed to save configuration: {e}")

    # ========================================================================
    # SCANSIONE DIRECTORY - DIRECTORY SCANNING
    # ========================================================================

    def scan_music_directory(self, path: str) -> List[Dict]:
        """
        Scansiona una directory alla ricerca di file audio.
        Restituisce una lista di dizionari con informazioni sui file.

        Scan a directory for audio files.
        Returns a list of dictionaries with file information.

        Args:
            path: Percorso della directory da scansionare - Directory path to scan

        Returns:
            List[Dict]: Lista di file audio trovati - List of found audio files
        """
        music_files = []
        path_obj = Path(path)

        if not path_obj.exists():
            print(f"[ERRORE] La directory non esiste: {path}")
            print("[ERROR] Directory does not exist: {path}")
            return music_files

        print(f"\nScansione directory: {path}")
        print(f"Scanning directory: {path}")
        print("=" * 60)

        # Cammina ricorsivamente nella directory - Walk recursively through directory
        for root, dirs, files in os.walk(path):
            for file in files:
                # Controlla estensione - Check extension
                if any(file.lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
                    file_path = Path(root) / file
                    metadata = self.get_metadata(str(file_path))

                    music_files.append({
                        'path': str(file_path),
                        'filename': file,
                        'title': metadata.get('title', file),
                        'artist': metadata.get('artist', 'Sconosciuto'),
                        'album': metadata.get('album', 'N/A')
                    })

                    print(f"  [+] {metadata.get('artist', 'Sconosciuto')} - {metadata.get('title', file)}")

        print(f"\n[Trovati] {len(music_files)} file audio")
        print(f"[Found] {len(music_files)} audio files\n")

        return music_files

    # ========================================================================
    # GESTIONE METADATI - METADATA MANAGEMENT
    # ========================================================================

    def get_metadata(self, file_path: str) -> Dict[str, str]:
        """
        Estrae i metadati da un file audio.
        Cerca di leggere i tag ID3, altrimenti usa il nome del file.

        Extract metadata from an audio file.
        Tries to read ID3 tags, otherwise uses filename.

        Args:
            file_path: Percorso del file audio - Path to audio file

        Returns:
            Dict: Metadati del file (title, artist, album) - File metadata
        """
        metadata = {'title': '', 'artist': '', 'album': ''}

        # Prova a importare mutagen per leggere i tag ID3 - Try importing mutagen for ID3 tags
        try:
            from mutagen.easyid3 import EasyID3
            from mutagen import File

            audio = File(file_path, easy=True)

            if audio is not None:
                if 'title' in audio:
                    metadata['title'] = audio['title'][0]
                if 'artist' in audio:
                    metadata['artist'] = audio['artist'][0]
                if 'album' in audio:
                    metadata['album'] = audio['album'][0]

        except ImportError:
            # mutagen non installato, usa il nome del file - mutagen not installed, use filename
            pass
        except Exception as e:
            # Errore nella lettura dei tag - Error reading tags
            pass

        # Se non ha titolo, usa il nome del file senza estensione - If no title, use filename
        if not metadata['title']:
            filename = Path(file_path).stem
            # Rimuove numeri all'inizio (es. "01 - Canzone") - Remove leading numbers
            filename = filename.lstrip('0123456789.- ')
            metadata['title'] = filename

        # Se non ha artista, prova a estrarlo dal nome file - If no artist, try from filename
        if not metadata['artist']:
            filename = Path(file_path).stem
            if ' - ' in filename:
                parts = filename.split(' - ', 1)
                if len(parts) == 2:
                    metadata['artist'] = parts[0].strip()
                    if not metadata['title'] or metadata['title'] == filename:
                        metadata['title'] = parts[1].strip()

        return metadata

    # ========================================================================
    # CONTROLLI RIPRODUZIONE - PLAYBACK CONTROLS
    # ========================================================================

    def play_song(self, file_path: Optional[str] = None) -> bool:
        """
        Riproduce un file audio.
        Se non specificato, riproduce la canzone corrente della playlist.

        Play an audio file.
        If not specified, plays current song from playlist.

        Args:
            file_path: Percorso del file da riprodurre - Path to file to play

        Returns:
            bool: True se riproduzione avviata con successo - True if playback started successfully
        """
        # Se specificato un file, lo usa - If file specified, use it
        if file_path:
            self.current_file = file_path
        # Altrimenti, usa la canzone corrente della playlist - Otherwise, use current playlist song
        elif self.current_playlist and 0 <= self.current_index < len(self.current_playlist):
            self.current_file = self.current_playlist[self.current_index]['path']
        else:
            print("[ERRORE] Nessuna canzone selezionata")
            print("[ERROR] No song selected")
            return False

        if not Path(self.current_file).exists():
            print(f"[ERRORE] File non trovato: {self.current_file}")
            print("[ERROR] File not found: {self.current_file}")
            return False

        try:
            # Ferma la riproduzione corrente - Stop current playback
            pygame.mixer.music.stop()

            # Carica e riproduci il file - Load and play file
            pygame.mixer.music.load(self.current_file)
            pygame.mixer.music.play()

            self.is_playing = True
            self.is_paused = False

            # Mostra info canzone - Show song info
            song_info = self._get_current_song_info()
            print("\n" + "=" * 60)
            print(f"  RIPRODUZIONE - NOW PLAYING")
            print("=" * 60)
            print(f"  Titolo:   {song_info['title']}")
            print(f"  Title:    {song_info['title']}")
            print(f"  Artista:  {song_info['artist']}")
            print(f"  Artist:   {song_info['artist']}")
            print(f"  Album:    {song_info['album']}")
            print(f"  Volume:   {int(pygame.mixer.music.get_volume() * 100)}%")
            print("=" * 60 + "\n")

            return True

        except pygame.error as e:
            print(f"[ERRORE] Impossibile riprodurre il file: {e}")
            print("[ERROR] Cannot play file: {e}")
            return False

    def pause_song(self) -> None:
        """
        Mette in pausa la riproduzione.

        Pause the playback.
        """
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            print("\n[PAUSA] Riproduzione in pausa")
            print("[PAUSED] Playback paused\n")

    def resume_song(self) -> None:
        """
        Riprende la riproduzione.

        Resume the playback.
        """
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            print("\n[RIPRESA] Riproduzione ripresa")
            print("[RESUMED] Playback resumed\n")

    def stop_song(self) -> None:
        """
        Ferma la riproduzione.

        Stop the playback.
        """
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            print("\n[STOP] Riproduzione fermata")
            print("[STOP] Playback stopped\n")

    def next_song(self) -> bool:
        """
        Passa alla prossima canzone nella playlist.

        Skip to next song in playlist.

        Returns:
            bool: True se avviata con successo - True if started successfully
        """
        if not self.current_playlist:
            print("[ERRORE] Nessuna playlist caricata")
            print("[ERROR] No playlist loaded")
            return False

        self.current_index = (self.current_index + 1) % len(self.current_playlist)
        print(f"\n[NEXT] Prossima canzone ({self.current_index + 1}/{len(self.current_playlist)})")
        return self.play_song()

    def previous_song(self) -> bool:
        """
        Passa alla canzone precedente nella playlist.

        Skip to previous song in playlist.

        Returns:
            bool: True se avviata con successo - True if started successfully
        """
        if not self.current_playlist:
            print("[ERRORE] Nessuna playlist caricata")
            print("[ERROR] No playlist loaded")
            return False

        self.current_index = (self.current_index - 1) % len(self.current_playlist)
        print(f"\n[PREV] Canzone precedente ({self.current_index + 1}/{len(self.current_playlist)})")
        return self.play_song()

    def adjust_volume(self, change: float) -> None:
        """
        Regola il volume.
        Valore positivo: aumenta, negativo: diminuisce.

        Adjust the volume.
        Positive value: increase, negative: decrease.

        Args:
            change: Variazione del volume (es. 0.1 per +10%) - Volume change (e.g. 0.1 for +10%)
        """
        current_volume = pygame.mixer.music.get_volume()
        new_volume = max(0.0, min(1.0, current_volume + change))
        pygame.mixer.music.set_volume(new_volume)
        self.config['volume'] = new_volume
        self._save_config()

        print(f"\n[VOLUME] {int(new_volume * 100)}%")
        print(f"[VOLUME] {int(new_volume * 100)}%\n")

    # ========================================================================
    # GESTIONE TESTI - LYRICS MANAGEMENT
    # ========================================================================

    def fetch_lyrics(self, artist: str, title: str) -> Optional[str]:
        """
        Recupera i testi di una canzone dall'API Lyrics.ovh.

        Fetch lyrics for a song from Lyrics.ovh API.

        Args:
            artist: Nome dell'artista - Artist name
            title: Titolo della canzone - Song title

        Returns:
            Optional[str]: Testi della canzone o None se non trovati - Song lyrics or None if not found
        """
        # Pulisci artista e titolo - Clean artist and title
        artist = artist.strip()
        title = title.strip()

        print(f"\n[RICERCA] Recupero testi...")
        print(f"[SEARCH] Fetching lyrics...")

        try:
            # Costruisci URL API - Build API URL
            # Sostituisci spazi e caratteri speciali - Replace spaces and special characters
            artist_clean = requests.utils.quote(artist)
            title_clean = requests.utils.quote(title)
            url = f"{LYRICS_API_BASE}/{artist_clean}/{title_clean}"

            # Fai la richiesta API - Make API request
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                lyrics = data.get('lyrics', '')

                if lyrics:
                    print(f"[OK] Testi recuperati con successo!")
                    print(f"[OK] Lyrics retrieved successfully!")
                    return lyrics
                else:
                    print(f"[ATTENZIONE] Testi non trovati")
                    print(f"[WARNING] Lyrics not found")
                    return None
            else:
                print(f"[ATTENZIONE] API response: {response.status_code}")
                print(f"[WARNING] API response: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"[ERRORE] Errore nella richiesta API: {e}")
            print("[ERROR] API request error: {e}")
            return None
        except Exception as e:
            print(f"[ERRORE] Errore nel recupero dei testi: {e}")
            print("[ERROR] Error fetching lyrics: {e}")
            return None

    def display_lyrics(self, lyrics: str) -> None:
        """
        Mostra i testi formattati a schermo.

        Display formatted lyrics on screen.

        Args:
            lyrics: Testi da mostrare - Lyrics to display
        """
        print("\n" + "=" * 70)
        print("  TESTI - LYRICS")
        print("=" * 70)
        print(lyrics)
        print("=" * 70 + "\n")

    # ========================================================================
    # GESTIONE PLAYLIST - PLAYLIST MANAGEMENT
    # ========================================================================

    def create_playlist(self, name: str, files: List[Dict]) -> Dict:
        """
        Crea una nuova playlist.

        Create a new playlist.

        Args:
            name: Nome della playlist - Playlist name
            files: Lista di file audio - List of audio files

        Returns:
            Dict: La playlist creata - The created playlist
        """
        playlist = {
            'name': name,
            'created': time.strftime('%Y-%m-%d %H:%M:%S'),
            'songs': files
        }
        return playlist

    def save_playlist(self, playlist: Dict) -> bool:
        """
        Salva una playlist su disco.

        Save a playlist to disk.

        Args:
            playlist: Playlist da salvare - Playlist to save

        Returns:
            bool: True se salvato con successo - True if saved successfully
        """
        try:
            # Nome file sicuro - Safe filename
            safe_name = "".join(c for c in playlist['name'] if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = PLAYLISTS_DIR / f"{safe_name}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(playlist, f, indent=4, ensure_ascii=False)

            print(f"\n[OK] Playlist salvata: {filename}")
            print(f"[OK] Playlist saved: {filename}\n")
            return True

        except (IOError, TypeError) as e:
            print(f"[ERRORE] Impossibile salvare la playlist: {e}")
            print("[ERROR] Failed to save playlist: {e}\n")
            return False

    def load_playlist(self, name: str) -> bool:
        """
        Carica una playlist dal disco.

        Load a playlist from disk.

        Args:
            name: Nome della playlist - Playlist name

        Returns:
            bool: True se caricata con successo - True if loaded successfully
        """
        try:
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = PLAYLISTS_DIR / f"{safe_name}.json"

            if not filename.exists():
                print(f"[ERRORE] Playlist non trovata: {name}")
                print("[ERROR] Playlist not found: {name}")
                return False

            with open(filename, 'r', encoding='utf-8') as f:
                playlist = json.load(f)

            self.current_playlist = playlist['songs']
            self.current_index = 0
            self.config['current_playlist'] = name
            self._save_config()

            print(f"\n[OK] Playlist caricata: {name}")
            print(f"[OK] Playlist loaded: {name}")
            print(f"[INFO] {len(self.current_playlist)} canzoni\n")
            return True

        except (IOError, json.JSONDecodeError) as e:
            print(f"[ERRORE] Impossibile caricare la playlist: {e}")
            print("[ERROR] Failed to load playlist: {e}\n")
            return False

    def list_saved_playlists(self) -> List[str]:
        """
        Lista tutte le playlist salvate.

        List all saved playlists.

        Returns:
            List[str]: Nomi delle playlist salvate - Names of saved playlists
        """
        playlists = []
        for file in PLAYLISTS_DIR.glob('*.json'):
            playlists.append(file.stem)
        return playlists

    def display_current_playlist(self) -> None:
        """
        Mostra la playlist corrente.

        Display current playlist.
        """
        if not self.current_playlist:
            print("\n[INFO] Nessuna playlist caricata")
            print("[INFO] No playlist loaded\n")
            return

        print("\n" + "=" * 70)
        print(f"  PLAYLIST: {len(self.current_playlist)} canzoni")
        print("=" * 70)

        for i, song in enumerate(self.current_playlist, 1):
            # Indica la canzone corrente - Indicate current song
            marker = " >> " if i - 1 == self.current_index else "    "
            print(f"{marker}{i}. {song['artist']} - {song['title']}")

        print("=" * 70 + "\n")

    # ========================================================================
    # UTILITY - UTILITY FUNCTIONS
    # ========================================================================

    def _get_current_song_info(self) -> Dict[str, str]:
        """
        Restituisce informazioni sulla canzone corrente.

        Return information about current song.

        Returns:
            Dict: Info canzone corrente - Current song info
        """
        if self.current_playlist and 0 <= self.current_index < len(self.current_playlist):
            return self.current_playlist[self.current_index]
        elif self.current_file:
            return self.get_metadata(self.current_file)
        else:
            return {'title': 'N/A', 'artist': 'N/A', 'album': 'N/A'}

    def is_playing_music(self) -> bool:
        """
        Controlla se la musica sta suonando.

        Check if music is playing.

        Returns:
            bool: True se la musica sta suonando - True if music is playing
        """
        return pygame.mixer.music.get_busy() and not self.is_paused


# ============================================================================
# INTERFACCIA UTENTE - USER INTERFACE
# ============================================================================

class MusicPlayerUI:
    """
    Interfaccia utente del riproduttore musicale.
    Menu e interazione con l'utente.

    Music player user interface.
    Menus and user interaction.
    """

    def __init__(self, player: MusicPlayer):
        """
        Inizializza l'interfaccia utente.

        Initialize the user interface.

        Args:
            player: Istanza del riproduttore musicale - Music player instance
        """
        self.player = player
        self.demo_mode = False

    def clear_screen(self) -> None:
        """
        Pulisce lo schermo (compatibile Windows e Linux/Mac).

        Clear screen (compatible with Windows and Linux/Mac).
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_header(self) -> None:
        """
        Mostra l'intestazione del programma.

        Show program header.
        """
        print("\n" + "=" * 70)
        print("  *      *       *       *       *    RIPRODUTTORE MUSICALE")
        print("  *      *       *       *       *    MUSIC PLAYER")
        print("  con supporto playlist e testi - with playlist & lyrics support")
        print("=" * 70 + "\n")

    def show_main_menu(self) -> None:
        """
        Mostra il menu principale.

        Show main menu.
        """
        print("  MENU PRINCIPALE - MAIN MENU")
        print("  " + "-" * 66)
        print("  1. Scansiona directory musica - Scan music directory")
        print("  2. Mostra playlist corrente - Show current playlist")
        print("  3. Carica playlist salvata - Load saved playlist")
        print("  4. Salva playlist corrente - Save current playlist")
        print("  5. Controlli riproduzione - Playback controls")
        print("  6. Mostra testi canzone - Show song lyrics")
        print("  7. Gestione volume - Volume management")
        print("  8. Info canzone corrente - Current song info")
        print("  9. Demo mode (mock data) - Modalita demo")
        print("  0. Esci - Exit")
        print()

    # ========================================================================
    # MENU PRINCIPALE - MAIN MENU LOOP
    # ========================================================================

    def run(self) -> None:
        """
        Esegue il loop principale del programma.

        Run the main program loop.
        """
        while True:
            self.clear_screen()
            self.show_header()

            # Mostra stato corrente - Show current state
            if self.player.is_playing:
                status = "PLAYING" if not self.player.is_paused else "PAUSED"
                print(f"  STATUS: {status} | Volume: {int(self.player.config['volume'] * 100)}%")
                if self.player.current_playlist:
                    current = self.player._get_current_song_info()
                    print(f"  Current: {current['artist']} - {current['title']}")
                print()

            self.show_main_menu()

            choice = input("  Selezione - Selection: ").strip()

            # Gestione scelta - Handle choice
            if choice == '1':
                self._scan_directory()
            elif choice == '2':
                self.player.display_current_playlist()
            elif choice == '3':
                self._load_playlist_menu()
            elif choice == '4':
                self._save_playlist_menu()
            elif choice == '5':
                self._playback_controls()
            elif choice == '6':
                self._show_lyrics()
            elif choice == '7':
                self._volume_controls()
            elif choice == '8':
                self._show_current_song_info()
            elif choice == '9':
                self._demo_mode()
            elif choice == '0':
                print("\n  Arrivederci! - Goodbye!\n")
                self.player.stop_song()
                pygame.mixer.quit()
                break
            else:
                print("\n  [!] Scelta non valida - Invalid choice")
                input("\n  Premi INVIO per continuare - Press ENTER to continue")

    # ========================================================================
    # MENU SOTTOMENU - SUBMENU HANDLERS
    # ========================================================================

    def _scan_directory(self) -> None:
        """Menu per scansionare directory musica - Menu to scan music directory."""
        print("\n  Scansiona Directory - Scan Directory")
        print("  " + "-" * 66)

        default_dir = self.player.config['music_directory']
        path = input(f"\n  Percorso directory - Directory path [{default_dir}]: ").strip()

        if not path:
            path = default_dir

        files = self.player.scan_music_directory(path)

        if files:
            # Crea playlist temporanea - Create temporary playlist
            self.player.current_playlist = files
            self.player.current_index = 0
            print(f"\n  [OK] Playlist creata con {len(files)} canzoni!")
            print(f"  [OK] Playlist created with {len(files)} songs!")

            # Chiedi se salvare - Ask to save
            save = input("\n  Salvare questa playlist? - Save this playlist? (s/n): ").strip().lower()
            if save == 's' or save == 'y':
                name = input("  Nome playlist - Playlist name: ").strip()
                if name:
                    playlist = self.player.create_playlist(name, files)
                    self.player.save_playlist(playlist)
        else:
            print("\n  [!] Nessun file audio trovato")
            print("  [!] No audio files found")

        input("\n  Premi INVIO per continuare - Press ENTER to continue")

    def _load_playlist_menu(self) -> None:
        """Menu per caricare playlist - Menu to load playlist."""
        print("\n  Carica Playlist - Load Playlist")
        print("  " + "-" * 66)

        playlists = self.player.list_saved_playlists()

        if not playlists:
            print("\n  [!] Nessuna playlist salvata")
            print("  [!] No saved playlists")
        else:
            print("\n  Playlist disponibili - Available playlists:")
            for i, name in enumerate(playlists, 1):
                print(f"    {i}. {name}")

            print()
            choice = input("  Nome playlist o numero - Playlist name or number: ").strip()

            # Se è un numero, usa l'indice - If number, use index
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(playlists):
                    choice = playlists[idx]

            if choice:
                self.player.load_playlist(choice)

        input("\n  Premi INVIO per continuare - Press ENTER to continue")

    def _save_playlist_menu(self) -> None:
        """Menu per salvare playlist - Menu to save playlist."""
        print("\n  Salva Playlist - Save Playlist")
        print("  " + "-" * 66)

        if not self.player.current_playlist:
            print("\n  [!] Nessuna playlist corrente da salvare")
            print("  [!] No current playlist to save")
        else:
            name = input("\n  Nome playlist - Playlist name: ").strip()
            if name:
                playlist = self.player.create_playlist(name, self.player.current_playlist)
                self.player.save_playlist(playlist)

        input("\n  Premi INVIO per continuare - Press ENTER to continue")

    def _playback_controls(self) -> None:
        """Menu controlli riproduzione - Playback controls menu."""
        print("\n  Controlli Riproduzione - Playback Controls")
        print("  " + "-" * 66)

        if not self.player.current_playlist:
            print("\n  [!] Carica prima una playlist")
            print("  [!] Load a playlist first")
            input("\n  Premi INVIO per continuare - Press ENTER to continue")
            return

        while True:
            print("\n  1. Play - Riproduci")
            print("  2. Pause - Pausa")
            print("  3. Resume - Riprendi")
            print("  4. Stop - Ferma")
            print("  5. Next - Prossima")
            print("  6. Previous - Precedente")
            print("  0. Indietro - Back")

            choice = input("\n  Selezione - Selection: ").strip()

            if choice == '1':
                self.player.play_song()
            elif choice == '2':
                self.player.pause_song()
            elif choice == '3':
                self.player.resume_song()
            elif choice == '4':
                self.player.stop_song()
            elif choice == '5':
                self.player.next_song()
            elif choice == '6':
                self.player.previous_song()
            elif choice == '0':
                break
            else:
                print("\n  [!] Scelta non valida - Invalid choice")

            time.sleep(0.5)

    def _show_lyrics(self) -> None:
        """Mostra i testi della canzone corrente - Show current song lyrics."""
        print("\n  Testi Canzone - Song Lyrics")
        print("  " + "-" * 66)

        song_info = self.player._get_current_song_info()
        artist = song_info['artist']
        title = song_info['title']

        print(f"\n  Canzone - Song: {title}")
        print(f"  Artista - Artist: {artist}")

        lyrics = self.player.fetch_lyrics(artist, title)

        if lyrics:
            self.player.display_lyrics(lyrics)
        else:
            print("\n  [!] Impossibile recuperare i testi")
            print("  [!] Cannot fetch lyrics")

        input("\n  Premi INVIO per continuare - Press ENTER to continue")

    def _volume_controls(self) -> None:
        """Menu gestione volume - Volume management menu."""
        print("\n  Gestione Volume - Volume Management")
        print("  " + "-" * 66)

        current = int(self.player.config['volume'] * 100)
        print(f"\n  Volume attuale - Current volume: {current}%")

        print("\n  1. Aumenta - Increase (+10%)")
        print("  2. Diminuisci - Decrease (-10%)")
        print("  3. Imposta valore - Set value (0-100)")
        print("  0. Indietro - Back")

        choice = input("\n  Selezione - Selection: ").strip()

        if choice == '1':
            self.player.adjust_volume(0.1)
        elif choice == '2':
            self.player.adjust_volume(-0.1)
        elif choice == '3':
            try:
                value = int(input("  Volume (0-100): ").strip())
                self.player.config['volume'] = max(0, min(100, value)) / 100
                pygame.mixer.music.set_volume(self.player.config['volume'])
                self.player._save_config()
                print(f"\n  Volume impostato a {self.player.config['volume'] * 100}%")
            except ValueError:
                print("\n  [!] Valore non valido - Invalid value")

        input("\n  Premi INVIO per continuare - Press ENTER to continue")

    def _show_current_song_info(self) -> None:
        """Mostra info canzone corrente - Show current song info."""
        print("\n  Info Canzone Corrente - Current Song Info")
        print("  " + "-" * 66)

        song_info = self.player._get_current_song_info()

        print(f"\n  Titolo - Title:   {song_info['title']}")
        print(f"  Artista - Artist: {song_info['artist']}")
        print(f"  Album - Album:    {song_info['album']}")

        if self.player.current_file:
            print(f"\n  File: {self.player.current_file}")

        print(f"\n  Volume: {int(self.player.config['volume'] * 100)}%")
        print(f"  Status: {'PLAYING' if self.player.is_playing_music() else 'STOPPED'}")

        input("\n  Premi INVIO per continuare - Press ENTER to continue")

    def _demo_mode(self) -> None:
        """Attiva modalità demo con dati finti - Activate demo mode with mock data."""
        print("\n  Modalita Demo - Demo Mode")
        print("  " + "-" * 66)

        # Crea dati finti - Create mock data
        demo_songs = [
            {
                'path': 'demo/song1.mp3',
                'filename': 'song1.mp3',
                'title': 'Bohemian Rhapsody',
                'artist': 'Queen',
                'album': 'A Night at the Opera'
            },
            {
                'path': 'demo/song2.mp3',
                'filename': 'song2.mp3',
                'title': 'Imagine',
                'artist': 'John Lennon',
                'album': 'Imagine'
            },
            {
                'path': 'demo/song3.mp3',
                'filename': 'song3.mp3',
                'title': 'Hotel California',
                'artist': 'Eagles',
                'album': 'Hotel California'
            }
        ]

        self.player.current_playlist = demo_songs
        self.player.current_index = 0
        self.demo_mode = True

        print("\n  [OK] Modalita demo attivata!")
        print("  [OK] Demo mode activated!")
        print("\n  Playlist demo caricata con 3 canzoni:")
        for i, song in enumerate(demo_songs, 1):
            print(f"    {i}. {song['artist']} - {song['title']}")

        print("\n  [NOTA] I file non esistono realmente.")
        print("  [NOTE] Files don't actually exist.")
        print("  Puoi testare l'interfaccia e il recupero testi.")
        print("  You can test the interface and lyrics fetching.")

        input("\n  Premi INVIO per continuare - Press ENTER to continue")


# ============================================================================
# FUNZIONE PRINCIPALE - MAIN FUNCTION
# ============================================================================

def main():
    """
    Funzione principale del programma.
    Inizializza il player e l'interfaccia utente.

    Main program function.
    Initialize player and user interface.
    """
    # Controlla dipendenze - Check dependencies
    print("Verifica dipendenze - Checking dependencies...")

    missing = []

    try:
        import pygame
        print(f"[OK] pygame {pygame.version.ver}")
    except ImportError:
        missing.append("pygame")

    try:
        import requests
        print("[OK] requests")
    except ImportError:
        missing.append("requests")

    if missing:
        print(f"\n[ERRORE] Mancano le seguenti librerie:")
        print("[ERROR] Missing libraries:")
        for lib in missing:
            print(f"  - {lib}")
        print(f"\nInstalla con: pip install {' '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        input("\nPremi INVIO per uscire - Press ENTER to exit")
        return

    # Crea il player - Create player
    player = MusicPlayer()

    # Controlla se ci sono file musicali - Check for music files
    music_dir = player.config['music_directory']
    print(f"\nControllo directory musica: {music_dir}")
    print(f"Checking music directory: {music_dir}")

    has_music = False
    if Path(music_dir).exists():
        audio_files = list(Path(music_dir).rglob('*.mp3')) + \
                     list(Path(music_dir).rglob('*.wav'))
        has_music = len(audio_files) > 0
        print(f"[TROVATI] {len(audio_files)} file audio")
        print(f"[FOUND] {len(audio_files)} audio files")
    else:
        print("[ATTENZIONE] Directory musica non trovata")
        print("[WARNING] Music directory not found")

    if not has_music:
        print("\n[Nessun file audio trovato - No audio files found]")
        print("Puoi usare la Modalita Demo (opzione 9) per testare l'interfaccia.")
        print("You can use Demo Mode (option 9) to test the interface.")
        print("\nOppure specifica una directory diversa nel menu (opzione 1).")
        print("Or specify a different directory in the menu (option 1).")

    input("\nPremi INVIO per continuare - Press ENTER to continue")

    # Avvia interfaccia utente - Start user interface
    ui = MusicPlayerUI(player)
    ui.run()


if __name__ == "__main__":
    main()
