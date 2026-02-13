import React from 'react';
import { FiHeart } from 'react-icons/fi';
import { useMusic } from '../contexts/MusicContext';

const TrackList = ({ tracks, playlistTracks }) => {
  const {
    currentTrack,
    isPlaying,
    playTrack,
    playlist,
    toggleLike,
    isLiked,
    addTrackToPlaylist
  } = useMusic();

  const handleTrackClick = (track, index) => {
    const trackList = playlistTracks || tracks;
    playTrack(track, trackList, index);
  };

  return (
    <div className="track-list">
      <div className="track-list-header">
        <span>#</span>
        <span>Titolo</span>
        <span className="track-album">Album</span>
        <span></span>
        <span></span>
      </div>

      {tracks.map((track, index) => {
        const isActive = currentTrack?.id === track.id;
        const isTrackPlaying = isActive && isPlaying;

        return (
          <div
            key={track.id}
            className={`track-item ${isActive ? 'active' : ''}`}
            onClick={() => handleTrackClick(track, index)}
          >
            <div className="track-number">
              {isTrackPlaying ? (
                <div className="playing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              ) : (
                index + 1
              )}
              <div className="track-play-icon">
                <svg viewBox="0 0 16 16">
                  <path d="M3 1.713a.7.7 0 011.05-.607l10.89 6.288a.7.7 0 010 1.212L4.05 14.894A.7.7 0 013 14.288V1.713z" />
                </svg>
              </div>
            </div>

            <div className="track-info">
              <img
                src={track.image}
                alt={track.title}
                className="track-image"
              />
              <div className="track-details">
                <div className="track-title">{track.title}</div>
                <div className="track-artist">{track.artist}</div>
              </div>
            </div>

            <div className="track-album">{track.album}</div>

            <div className="track-like">
              <button
                className={`track-like ${isLiked(track.id) ? 'liked' : ''}`}
                onClick={(e) => {
                  e.stopPropagation();
                  toggleLike(track.id);
                }}
              >
                <svg viewBox="0 0 16 16">
                  <path d="M1.69 2A4.582 4.582 0 018 2.023 4.583 4.583 0 0111.758 4.5c2.058 2.381 1.693 6.31-1.885 9.747L8 15.38l-1.873-1.133C2.55 10.811 2.187 6.88 4.245 4.5A4.582 4.582 0 011.69 2zm4.897 12.65l.356.214.357-.214C9.316 13.17 11.25 11.254 11.25 8.5a3 3 0 00-6 0c0 2.754 1.934 4.67 4.337 6.15z" />
                </svg>
              </button>
            </div>

            <div className="track-duration">{track.duration}</div>
          </div>
        );
      })}
    </div>
  );
};

export default TrackList;
