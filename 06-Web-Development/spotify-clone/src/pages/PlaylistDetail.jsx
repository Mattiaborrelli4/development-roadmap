import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { playlists, tracks } from '../data';
import TrackList from '../components/TrackList';
import { useMusic } from '../contexts/MusicContext';
import { FiPlayCircle, FiHeart, FiMoreHorizontal } from 'react-icons/fi';

const PlaylistDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { userPlaylists, playTrack, isLiked, deletePlaylist } = useMusic();

  const allPlaylists = [...playlists, ...userPlaylists];
  const playlist = allPlaylists.find(p => p.id === parseInt(id));

  if (!playlist) {
    return (
      <div className="main-content">
        <div className="empty-state">
          <div className="empty-state-icon">🎵</div>
          <h3 className="empty-state-title">Playlist non trovata</h3>
          <p className="empty-state-desc">
            La playlist che stai cercando non esiste.
          </p>
        </div>
      </div>
    );
  }

  const playlistTracks = playlist.tracks
    .map(trackId => tracks.find(t => t.id === trackId))
    .filter(Boolean);

  const handlePlay = () => {
    if (playlistTracks.length > 0) {
      playTrack(playlistTracks[0], playlistTracks, 0);
    }
  };

  const handleDelete = () => {
    if (window.confirm('Sei sicuro di voler eliminare questa playlist?')) {
      deletePlaylist(playlist.id);
      navigate('/library');
    }
  };

  const totalDuration = playlistTracks.reduce((acc, track) => {
    const [mins, secs] = track.duration.split(':').map(Number);
    return acc + mins * 60 + secs;
  }, 0);

  const hours = Math.floor(totalDuration / 3600);
  const minutes = Math.floor((totalDuration % 3600) / 60);

  return (
    <div className="main-content">
      <div className="content-header">
        <div className="content-nav">
          <button className="nav-arrow" onClick={() => navigate(-1)}>
            <svg viewBox="0 0 24 24">
              <path d="M15.957 2.793a1 1 0 010 1.414L8.164 12l7.793 7.793a1 1 0 01-1.414 1.414L5.336 12l9.207-9.207a1 1 0 011.414 0z" />
            </svg>
          </button>
        </div>
      </div>

      <div className="playlist-detail-header">
        <div className="playlist-detail-image">
          <img src={playlist.image} alt={playlist.name} />
        </div>
        <div className="playlist-detail-info">
          <div className="playlist-detail-type">Playlist</div>
          <h1 className="playlist-detail-title">{playlist.name}</h1>
          <div className="playlist-detail-meta">
            {playlist.description && <span>{playlist.description} • </span>}
            <span>{playlistTracks.length} brani</span>
            {hours > 0 && <span>, {hours} ore {minutes} min</span>}
            {hours === 0 && minutes > 0 && <span>, {minutes} min</span>}
          </div>
        </div>
      </div>

      <div className="playlist-detail-actions">
        <button className="play-button-large" onClick={handlePlay}>
          <svg viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </button>

        <button className="action-btn">
          <FiHeart />
        </button>

        <button className="action-btn">
          <FiMoreHorizontal />
        </button>

        {userPlaylists.find(p => p.id === playlist.id) && (
          <button
            className="btn-secondary"
            onClick={handleDelete}
            style={{ marginLeft: 'auto' }}
          >
            Elimina
          </button>
        )}
      </div>

      <div className="track-list">
        <div className="track-list-header">
          <span>#</span>
          <span>Titolo</span>
          <span className="track-album">Album</span>
          <span></span>
          <span></span>
        </div>

        {playlistTracks.length > 0 ? (
          <TrackList tracks={playlistTracks} playlistTracks={playlistTracks} />
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">🎵</div>
            <h3 className="empty-state-title">Playlist vuota</h3>
            <p className="empty-state-desc">
              Aggiungi dei brani alla tua playlist
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlaylistDetail;
