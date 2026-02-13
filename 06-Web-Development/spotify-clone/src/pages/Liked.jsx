import React, { useMemo } from 'react';
import { FiHeart } from 'react-icons/fi';
import { tracks } from '../data';
import TrackList from '../components/TrackList';
import { useMusic } from '../contexts/MusicContext';

const Liked = () => {
  const { isLiked } = useMusic();

  const likedTracks = useMemo(() => {
    return tracks.filter(track => isLiked(track.id));
  }, [isLiked]);

  return (
    <div className="main-content">
      <div className="content-header">
        <div className="content-nav">
          <button className="nav-arrow">
            <svg viewBox="0 0 24 24">
              <path d="M15.957 2.793a1 1 0 010 1.414L8.164 12l7.793 7.793a1 1 0 01-1.414 1.414L5.336 12l9.207-9.207a1 1 0 011.414 0z" />
            </svg>
          </button>
          <button className="nav-arrow" disabled>
            <svg viewBox="0 0 24 24">
              <path d="M8.043 2.793a1 1 0 000 1.414L15.836 12l-7.793 7.793a1 1 0 001.414 1.414L18.664 12 9.457 2.793a1 1 0 00-1.414 0z" />
            </svg>
          </button>
        </div>

        <div className="user-menu">
          <img
            src="https://i.pravatar.cc/150?img=68"
            alt="Utente"
          />
          <span>Matteo</span>
        </div>
      </div>

      <div className="playlist-detail-header">
        <div
          className="playlist-detail-image"
          style={{
            background: 'linear-gradient(135deg, #450af5, #c4efd9)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <FiHeart size={80} color="white" />
        </div>
        <div className="playlist-detail-info">
          <div className="playlist-detail-type">Playlist</div>
          <h1 className="playlist-detail-title">Brani Piaciuti</h1>
          <div className="playlist-detail-meta">
            <span>{likedTracks.length} brani</span>
          </div>
        </div>
      </div>

      <div className="playlist-detail-actions">
        <button
          className="play-button-large"
          onClick={() => {
            if (likedTracks.length > 0) {
              window.dispatchEvent(new CustomEvent('playAll', { detail: likedTracks }));
            }
          }}
        >
          <svg viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </button>

        <button className="action-btn">
          <FiHeart />
        </button>

        <button className="action-btn">
          <svg viewBox="0 0 24 24" width="32" height="32">
            <path fill="currentColor" d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm0 18c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" />
          </svg>
        </button>
      </div>

      {likedTracks.length > 0 ? (
        <TrackList tracks={likedTracks} />
      ) : (
        <div className="empty-state">
          <div className="empty-state-icon">💚</div>
          <h3 className="empty-state-title">Nessun brano piaciuto</h3>
          <p className="empty-state-desc">
            Salva i brani che ti piacciono premendo sull'icona del cuore.
          </p>
        </div>
      )}
    </div>
  );
};

export default Liked;
