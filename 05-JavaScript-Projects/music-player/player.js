// ===== Music Player Class =====
class MusicPlayer {
    constructor() {
        // DOM Elements
        this.audio = document.getElementById('audio');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.shuffleBtn = document.getElementById('shuffleBtn');
        this.repeatBtn = document.getElementById('repeatBtn');
        this.muteBtn = document.getElementById('muteBtn');
        this.progressBar = document.getElementById('progressBar');
        this.progressHandle = document.getElementById('progressHandle');
        this.volumeBar = document.getElementById('volumeBar');
        this.progressContainer = document.querySelector('.progress-bar-wrapper');
        this.volumeContainer = document.querySelector('.volume-bar-wrapper');
        this.currentTimeEl = document.getElementById('currentTime');
        this.durationEl = document.getElementById('duration');
        this.volumeValueEl = document.getElementById('volumeValue');
        this.trackTitle = document.getElementById('trackTitle');
        this.trackArtist = document.getElementById('trackArtist');
        this.trackImage = document.getElementById('trackImage');
        this.playlistContainer = document.getElementById('playlist');

        // Player State
        this.state = {
            isPlaying: false,
            currentTrackIndex: 0,
            isShuffle: false,
            repeatMode: 'none', // none, one, all
            isMuted: false,
            previousVolume: 0.8,
            currentVolume: 0.8
        };

        // Sample Playlist with free audio files
        this.playlist = [
            {
                title: "Summer Breeze",
                artist: "Artist Name 1",
                src: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                cover: "https://picsum.photos/seed/track1/300/300",
                duration: "6:19"
            },
            {
                title: "Midnight Dreams",
                artist: "Artist Name 2",
                src: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                cover: "https://picsum.photos/seed/track2/300/300",
                duration: "7:05"
            },
            {
                title: "Electric Vibes",
                artist: "Artist Name 3",
                src: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
                cover: "https://picsum.photos/seed/track3/300/300",
                duration: "5:42"
            },
            {
                title: "Ocean Waves",
                artist: "Artist Name 4",
                src: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
                cover: "https://picsum.photos/seed/track4/300/300",
                duration: "6:58"
            },
            {
                title: "City Lights",
                artist: "Artist Name 5",
                src: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
                cover: "https://picsum.photos/seed/track5/300/300",
                duration: "5:30"
            }
        ];

        // Initialize the player
        this.init();
    }

    // ===== Initialize Player =====
    init() {
        this.setupEventListeners();
        this.renderPlaylist();
        this.loadTrack(this.state.currentTrackIndex);
        this.updateVolumeUI();
    }

    // ===== Setup Event Listeners =====
    setupEventListeners() {
        // Play/Pause
        this.playPauseBtn.addEventListener('click', () => this.togglePlay());

        // Next/Previous
        this.nextBtn.addEventListener('click', () => this.nextTrack());
        this.prevBtn.addEventListener('click', () => this.prevTrack());

        // Shuffle
        this.shuffleBtn.addEventListener('click', () => this.toggleShuffle());

        // Repeat
        this.repeatBtn.addEventListener('click', () => this.toggleRepeat());

        // Mute
        this.muteBtn.addEventListener('click', () => this.toggleMute());

        // Progress Bar
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('loadedmetadata', () => this.updateDuration());
        this.audio.addEventListener('ended', () => this.handleTrackEnd());
        this.progressContainer.addEventListener('click', (e) => this.seek(e));

        // Volume Control
        this.volumeContainer.addEventListener('click', (e) => this.setVolume(e));

        // Keyboard Controls
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    // ===== Load Track =====
    loadTrack(index) {
        if (index < 0 || index >= this.playlist.length) return;

        this.state.currentTrackIndex = index;
        const track = this.playlist[index];

        this.audio.src = track.src;
        this.audio.load();

        // Update UI
        this.trackTitle.textContent = track.title;
        this.trackArtist.textContent = track.artist;
        this.trackImage.src = track.cover;

        // Update playlist active item
        this.updatePlaylistActiveItem();
    }

    // ===== Toggle Play/Pause =====
    togglePlay() {
        if (this.state.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    // ===== Play =====
    play() {
        this.audio.play()
            .then(() => {
                this.state.isPlaying = true;
                this.updatePlayPauseBtn();
                document.querySelector('.music-player').classList.add('playing');
            })
            .catch(error => console.error('Errore di riproduzione:', error));
    }

    // ===== Pause =====
    pause() {
        this.audio.pause();
        this.state.isPlaying = false;
        this.updatePlayPauseBtn();
        document.querySelector('.music-player').classList.remove('playing');
    }

    // ===== Update Play/Pause Button =====
    updatePlayPauseBtn() {
        const icon = this.playPauseBtn.querySelector('i');
        if (this.state.isPlaying) {
            icon.className = 'fas fa-pause';
        } else {
            icon.className = 'fas fa-play';
        }
    }

    // ===== Next Track =====
    nextTrack() {
        let nextIndex;

        if (this.state.isShuffle) {
            // Random track (excluding current)
            do {
                nextIndex = Math.floor(Math.random() * this.playlist.length);
            } while (nextIndex === this.state.currentTrackIndex && this.playlist.length > 1);
        } else {
            // Next track in order
            nextIndex = (this.state.currentTrackIndex + 1) % this.playlist.length;
        }

        this.loadTrack(nextIndex);
        if (this.state.isPlaying) {
            this.play();
        }
    }

    // ===== Previous Track =====
    prevTrack() {
        const prevIndex = (this.state.currentTrackIndex - 1 + this.playlist.length) % this.playlist.length;
        this.loadTrack(prevIndex);
        if (this.state.isPlaying) {
            this.play();
        }
    }

    // ===== Toggle Shuffle =====
    toggleShuffle() {
        this.state.isShuffle = !this.state.isShuffle;
        this.shuffleBtn.classList.toggle('active', this.state.isShuffle);
    }

    // ===== Toggle Repeat =====
    toggleRepeat() {
        const modes = ['none', 'all', 'one'];
        const currentModeIndex = modes.indexOf(this.state.repeatMode);
        this.state.repeatMode = modes[(currentModeIndex + 1) % modes.length];

        // Update UI
        this.repeatBtn.classList.toggle('active', this.state.repeatMode !== 'none');

        const icon = this.repeatBtn.querySelector('i');
        if (this.state.repeatMode === 'one') {
            icon.className = 'fas fa-redo';
            this.repeatBtn.innerHTML = '<i class="fas fa-redo"></i><span>1</span>';
            this.repeatBtn.style.position = 'relative';
        } else {
            icon.className = 'fas fa-redo';
            this.repeatBtn.innerHTML = '<i class="fas fa-redo"></i>';
            this.repeatBtn.style.position = '';
        }
    }

    // ===== Toggle Mute =====
    toggleMute() {
        if (this.state.isMuted) {
            this.audio.volume = this.state.previousVolume;
            this.state.isMuted = false;
            this.state.currentVolume = this.state.previousVolume;
        } else {
            this.state.previousVolume = this.state.currentVolume;
            this.audio.volume = 0;
            this.state.isMuted = true;
            this.state.currentVolume = 0;
        }
        this.updateVolumeUI();
    }

    // ===== Set Volume =====
    setVolume(event) {
        const rect = this.volumeContainer.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const width = rect.width;
        const volume = Math.max(0, Math.min(1, x / width));

        this.state.currentVolume = volume;
        this.audio.volume = volume;
        this.state.isMuted = volume === 0;
        this.updateVolumeUI();
    }

    // ===== Update Volume UI =====
    updateVolumeUI() {
        const percentage = Math.round(this.state.currentVolume * 100);
        this.volumeBar.style.width = `${percentage}%`;
        this.volumeValueEl.textContent = `${percentage}%`;

        const icon = this.muteBtn.querySelector('i');
        if (this.state.currentVolume === 0 || this.state.isMuted) {
            icon.className = 'fas fa-volume-mute';
        } else if (this.state.currentVolume < 0.5) {
            icon.className = 'fas fa-volume-down';
        } else {
            icon.className = 'fas fa-volume-up';
        }
    }

    // ===== Update Progress =====
    updateProgress() {
        const { currentTime, duration } = this.audio;
        if (isNaN(duration)) return;

        const progressPercent = (currentTime / duration) * 100;
        this.progressBar.style.width = `${progressPercent}%`;
        this.progressHandle.style.left = `${progressPercent}%`;
        this.currentTimeEl.textContent = this.formatTime(currentTime);
    }

    // ===== Update Duration =====
    updateDuration() {
        this.durationEl.textContent = this.formatTime(this.audio.duration);
    }

    // ===== Seek =====
    seek(event) {
        const rect = this.progressContainer.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const width = rect.width;
        const duration = this.audio.duration;

        if (isNaN(duration)) return;

        const seekTime = (x / width) * duration;
        this.audio.currentTime = seekTime;
    }

    // ===== Handle Track End =====
    handleTrackEnd() {
        if (this.state.repeatMode === 'one') {
            this.audio.currentTime = 0;
            this.play();
        } else if (this.state.repeatMode === 'all' || this.state.currentTrackIndex < this.playlist.length - 1) {
            this.nextTrack();
        } else {
            this.pause();
            this.audio.currentTime = 0;
        }
    }

    // ===== Format Time =====
    formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';

        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    // ===== Render Playlist =====
    renderPlaylist() {
        this.playlistContainer.innerHTML = this.playlist.map((track, index) => `
            <div class="playlist-item ${index === this.state.currentTrackIndex ? 'active' : ''}"
                 data-index="${index}">
                <div class="playlist-item-info">
                    <div class="playlist-item-title">${track.title}</div>
                    <div class="playlist-item-artist">${track.artist}</div>
                </div>
                <div class="playlist-item-duration">${track.duration}</div>
            </div>
        `).join('');

        // Add click listeners to playlist items
        document.querySelectorAll('.playlist-item').forEach(item => {
            item.addEventListener('click', () => {
                const index = parseInt(item.dataset.index);
                this.loadTrack(index);
                this.play();
            });
        });
    }

    // ===== Update Playlist Active Item =====
    updatePlaylistActiveItem() {
        document.querySelectorAll('.playlist-item').forEach((item, index) => {
            item.classList.toggle('active', index === this.state.currentTrackIndex);
        });
    }

    // ===== Handle Keyboard Controls =====
    handleKeyboard(event) {
        // Ignore if user is typing in an input
        if (event.target.tagName === 'INPUT') return;

        switch (event.code) {
            case 'Space':
                event.preventDefault();
                this.togglePlay();
                break;
            case 'ArrowRight':
                this.audio.currentTime = Math.min(this.audio.duration, this.audio.currentTime + 5);
                break;
            case 'ArrowLeft':
                this.audio.currentTime = Math.max(0, this.audio.currentTime - 5);
                break;
            case 'ArrowUp':
                event.preventDefault();
                this.audio.volume = Math.min(1, this.audio.volume + 0.1);
                this.state.currentVolume = this.audio.volume;
                this.updateVolumeUI();
                break;
            case 'ArrowDown':
                event.preventDefault();
                this.audio.volume = Math.max(0, this.audio.volume - 0.1);
                this.state.currentVolume = this.audio.volume;
                this.updateVolumeUI();
                break;
            case 'KeyN':
                this.nextTrack();
                break;
            case 'KeyP':
                this.prevTrack();
                break;
            case 'KeyM':
                this.toggleMute();
                break;
        }
    }
}

// ===== Initialize Music Player when DOM is ready =====
document.addEventListener('DOMContentLoaded', () => {
    const player = new MusicPlayer();
    console.log('🎵 Music Player inizializzato con successo!');
    console.log('📋 Controlli disponibili:');
    console.log('   Spazio: Play/Pausa');
    console.log('   ← / →: Indietro/Avanti 5 secondi');
    console.log('   ↑ / ↓: Aumenta/Abbassa volume');
    console.log('   N: Next track');
    console.log('   P: Previous track');
    console.log('   M: Mute/Unmute');
});
