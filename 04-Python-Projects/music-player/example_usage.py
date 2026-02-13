#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esempio di Utilizzo del Riproduttore Musicale
==============================================

Script dimostrativo che mostra come usare le classi del music player.

Example Usage Script for Music Player
======================================

Demo script showing how to use the music player classes.
"""

from pathlib import Path
from music_player import MusicPlayer


def example_basic_usage():
    """
    Esempio di utilizzo base del music player.

    Example of basic music player usage.
    """
    print("=" * 70)
    print("  ESEMPIO 1: Inizializzazione e Configurazione")
    print("  EXAMPLE 1: Initialization and Configuration")
    print("=" * 70)

    # Crea istanza del player - Create player instance
    player = MusicPlayer()

    # Mostra configurazione corrente - Show current configuration
    print("\nConfigurazione attuale - Current configuration:")
    for key, value in player.config.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 70)


def example_scan_directory():
    """
    Esempio di scansione directory musicale.

    Example of scanning music directory.
    """
    print("\n" + "=" * 70)
    print("  ESEMPIO 2: Scansione Directory")
    print("  EXAMPLE 2: Directory Scanning")
    print("=" * 70)

    player = MusicPlayer()

    # Usa la directory musicale dell'utente - Use user's music directory
    music_dir = str(Path.home() / 'Music')

    print(f"\nScansione di: {music_dir}")
    print(f"Scanning: {music_dir}")

    files = player.scan_music_directory(music_dir)

    if files:
        print(f"\nTrovati {len(files)} file audio!")
        print(f"Found {len(files)} audio files!")

        # Mostra primi 5 file - Show first 5 files
        print("\nPrimi 5 file - First 5 files:")
        for i, file in enumerate(files[:5], 1):
            print(f"  {i}. {file['artist']} - {file['title']}")
    else:
        print("\nNessun file trovato. Prova con Demo Mode!")
        print("No files found. Try Demo Mode!")

    print("\n" + "=" * 70)


def example_playlist_operations():
    """
    Esempio di operazioni sulle playlist.

    Example of playlist operations.
    """
    print("\n" + "=" * 70)
    print("  ESEMPIO 3: Gestione Playlist")
    print("  EXAMPLE 3: Playlist Management")
    print("=" * 70)

    player = MusicPlayer()

    # Crea playlist demo - Create demo playlist
    demo_songs = [
        {
            'path': 'demo/song1.mp3',
            'filename': 'song1.mp3',
            'title': 'Imagine',
            'artist': 'John Lennon',
            'album': 'Imagine'
        },
        {
            'path': 'demo/song2.mp3',
            'filename': 'song2.mp3',
            'title': 'Hotel California',
            'artist': 'Eagles',
            'album': 'Hotel California'
        }
    ]

    playlist = player.create_playlist("Demo Playlist", demo_songs)

    print(f"\nPlaylist creata: {playlist['name']}")
    print(f"Playlist created: {playlist['name']}")
    print(f"Canzoni - Songs: {len(playlist['songs'])}")

    # Salva playlist - Save playlist
    player.save_playlist(playlist)

    # Carica playlist - Load playlist
    player.load_playlist("Demo Playlist")

    # Mostra playlist - Display playlist
    player.display_current_playlist()

    print("\n" + "=" * 70)


def example_lyrics_fetching():
    """
    Esempio di recupero dei testi.

    Example of lyrics fetching.
    """
    print("\n" + "=" * 70)
    print("  ESEMPIO 4: Recupero Testi")
    print("  EXAMPLE 4: Lyrics Fetching")
    print("=" * 70)

    player = MusicPlayer()

    # Esempio con canzone famosa - Example with famous song
    artist = "Queen"
    title = "Bohemian Rhapsody"

    print(f"\nRicerca testi per: {artist} - {title}")
    print(f"Searching lyrics for: {artist} - {title}")

    lyrics = player.fetch_lyrics(artist, title)

    if lyrics:
        print("\n[SUCCESSO] Testi recuperati!")
        print("[SUCCESS] Lyrics retrieved!")

        # Mostra prime righe - Show first lines
        lines = lyrics.split('\n')[:10]
        print("\nPrime righe - First lines:")
        for line in lines:
            print(f"  {line}")

        print("\n...")
        print(f"\nTotale caratteri: {len(lyrics)}")
        print(f"Total characters: {len(lyrics)}")
    else:
        print("\n[ATTENZIONE] Testi non trovati")
        print("[WARNING] Lyrics not found")

    print("\n" + "=" * 70)


def example_metadata_extraction():
    """
    Esempio di estrazione metadati.

    Example of metadata extraction.
    """
    print("\n" + "=" * 70)
    print("  ESEMPIO 5: Estrazione Metadati")
    print("  EXAMPLE 5: Metadata Extraction")
    print("=" * 70)

    player = MusicPlayer()

    # Crea file di test finto - Create fake test file
    test_file = "C:/Music/Artist_-_Album_-_Song.mp3"

    print(f"\nFile di test - Test file: {test_file}")

    metadata = player.get_metadata(test_file)

    print("\nMetadati estratti - Extracted metadata:")
    print(f"  Titolo - Title:   {metadata['title']}")
    print(f"  Artista - Artist: {metadata['artist']}")
    print(f"  Album - Album:    {metadata['album']}")

    print("\n" + "=" * 70)


def example_playback_controls():
    """
    Esempio di controlli di riproduzione (senza audio reale).

    Example of playback controls (without actual audio).
    """
    print("\n" + "=" * 70)
    print("  ESEMPIO 6: Controlli Riproduzione (Demo)")
    print("  EXAMPLE 6: Playback Controls (Demo)")
    print("=" * 70)

    player = MusicPlayer()

    # Crea playlist demo - Create demo playlist
    demo_songs = [
        {
            'path': 'demo/song1.mp3',
            'filename': 'song1.mp3',
            'title': 'Test Song',
            'artist': 'Test Artist',
            'album': 'Test Album'
        }
    ]

    player.current_playlist = demo_songs
    player.current_index = 0

    print("\nControlli disponibili - Available controls:")
    print("  1. play_song()      - Riproduci canzone - Play song")
    print("  2. pause_song()     - Metti in pausa - Pause")
    print("  3. resume_song()    - Riprendi - Resume")
    print("  4. stop_song()      - Ferma - Stop")
    print("  5. next_song()      - Prossima - Next")
    print("  6. previous_song()  - Precedente - Previous")
    print("  7. adjust_volume(x) - Regola volume - Adjust volume")

    print("\n[NOTA] Questi controlli funzionano solo con file audio reali")
    print("[NOTE] These controls only work with real audio files")

    # Esempio regolazione volume - Volume adjustment example
    print("\nEsempio: Regolazione Volume - Example: Volume Adjustment")
    print(f"Volume iniziale - Initial volume: {int(player.config['volume'] * 100)}%")

    player.adjust_volume(0.1)
    print(f"Dopo aumento - After increase: {int(player.config['volume'] * 100)}%")

    player.adjust_volume(-0.05)
    print(f"Dopo diminuzione - After decrease: {int(player.config['volume'] * 100)}%")

    print("\n" + "=" * 70)


def main():
    """
    Funzione principale che esegue tutti gli esempi.

    Main function that runs all examples.
    """
    print("\n" + "#" * 70)
    print("#  ESEMPI DI UTILIZZO RIPRODUTTORE MUSICALE")
    print("#  MUSIC PLAYER USAGE EXAMPLES")
    print("#" * 70)

    try:
        # Esegui esempi - Run examples
        example_basic_usage()
        input("\nPremi INVIO per continuare - Press ENTER to continue")

        example_scan_directory()
        input("\nPremi INVIO per continuare - Press ENTER to continue")

        example_playlist_operations()
        input("\nPremi INVIO per continuare - Press ENTER to continue")

        example_lyrics_fetching()
        input("\nPremi INVIO per continuare - Press ENTER to continue")

        example_metadata_extraction()
        input("\nPremi INVIO per continuare - Press ENTER to continue")

        example_playback_controls()

        print("\n" + "#" * 70)
        print("#  ESEMPI COMPLETATI!")
        print("#  EXAMPLES COMPLETED!")
        print("#" * 70)
        print("\nPer usare il player completo, esegui: python music_player.py")
        print("To use the full player, run: python music_player.py\n")

    except KeyboardInterrupt:
        print("\n\n[INTERRUPT] Esempi interrotti dall'utente")
        print("[INTERRUPT] Examples interrupted by user\n")
    except Exception as e:
        print(f"\n\n[ERROR] Errore durante gli esempi: {e}")
        print(f"[ERROR] Error during examples: {e}\n")


if __name__ == "__main__":
    main()
