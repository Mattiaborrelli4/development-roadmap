import React from 'react';
import { useNavigate } from 'react-router-dom';
import { playlists, tracks, artists } from '../data';
import { useMusic } from '../contexts/MusicContext';

const Library = () => {
  const navigate = useNavigate();
  const { userPlaylists, isLiked } = useMusic();

  const likedTracks = tracks.filter(track => isLiked(track.id));

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

      <section className="mb-4">
        <h2 className="section-title">Le tue Playlist</h2>
        <div className="playlists-grid">
          {userPlaylists.map(playlist => (
            <div
              key={playlist.id}
              className="playlist-card"
              onClick={() => navigate(`/playlist/${playlist.id}`)}
            >
              <div className="playlist-card-image">
                <img src={playlist.image} alt={playlist.name} />
              </div>
              <div className="playlist-card-title">{playlist.name}</div>
              <div className="playlist-card-desc">{playlist.description}</div>
            </div>
          ))}
        </div>
      </section>

      {likedTracks.length > 0 && (
        <section className="mb-4">
          <h2 className="section-title">Brani Piaciuti</h2>
          <div className="artists-grid">
            {likedTracks.slice(0, 6).map(track => (
              <div key={track.id} className="artist-card">
                <div className="artist-card-image">
                  <img src={track.image} alt={track.title} style={{ borderRadius: '4px' }} />
                </div>
                <div className="artist-card-name">{track.title}</div>
                <div className="artist-card-followers">{track.artist}</div>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="mb-4">
        <h2 className="section-title">Artisti che segui</h2>
        <div className="artists-grid">
          {artists.slice(0, 6).map(artist => (
            <div key={artist.id} className="artist-card">
              <div className="artist-card-image">
                <img src={artist.image} alt={artist.name} />
              </div>
              <div className="artist-card-name">{artist.name}</div>
              <div className="artist-card-followers">{artist.followers} follower</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Library;
