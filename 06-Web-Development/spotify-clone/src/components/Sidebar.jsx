import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { FiHome, FiSearch, FiBookOpen, FiPlusSquare, FiHeart } from 'react-icons/fi';
import { useMusic } from '../contexts/MusicContext';

const Sidebar = () => {
  const { userPlaylists } = useMusic();
  const [showCreateModal, setShowCreateModal] = useState(false);

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <svg viewBox="0 0 168 168">
          <path d="M83.996.277C37.747.277.253 37.77.253 84.019c0 46.251 37.494 83.741 83.743 83.741 46.254 0 83.744-37.49 83.744-83.741 0-46.246-37.49-83.738-83.745-83.738zM119.248 120.96c-1.693 2.804-5.322 3.707-8.13 2.02-22.16-13.52-50.052-16.586-82.937-9.078-3.176.722-6.35-1.28-7.072-4.455-.723-3.178 1.277-6.35 4.455-7.074 35.96-8.15 66.645-4.675 91.664 10.345 2.808 1.686 3.71 5.322 2.02 8.242zm10.616-20.85c-2.127 3.502-6.673 4.617-10.18 2.49-25.432-15.58-64.16-20.085-94.15-10.986-3.956 1.2-8.148-1.054-9.35-5.008-1.2-3.954 1.056-8.148 5.01-9.35 33.97-10.32 76.576-5.157 105.673 12.67 3.506 2.12 4.62 6.668 2.496 10.18v.004zm.915-21.7c-30.48-18.09-80.74-19.77-109.83-10.92-4.753 1.444-9.767-1.265-11.21-6.017-1.442-4.752 1.265-9.767 6.017-11.21 32.93-9.983 88.17-7.778 122.72 13.25 4.296 2.553 5.704 8.11 3.15 12.407-2.55 4.293-8.113 5.708-12.407 3.15z"></path>
        </svg>
        <h1>Spotify</h1>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/" className="nav-item">
          <FiHome />
          <span>Home</span>
        </NavLink>
        <NavLink to="/search" className="nav-item">
          <FiSearch />
          <span>Cerca</span>
        </NavLink>
        <NavLink to="/library" className="nav-item">
          <FiBookOpen />
          <span>La tua Libreria</span>
        </NavLink>
        <NavLink to="/liked" className="nav-item">
          <FiHeart />
          <span>Brani Piaciuti</span>
        </NavLink>
      </nav>

      <div className="sidebar-divider"></div>

      <button
        className="nav-item"
        style={{ border: 'none', background: 'none', cursor: 'pointer' }}
        onClick={() => setShowCreateModal(true)}
      >
        <FiPlusSquare />
        <span>Crea Playlist</span>
      </button>

      <div className="sidebar-divider"></div>

      <div className="sidebar-section-title">Le tue Playlist</div>

      <div className="library-playlists">
        {userPlaylists.map(playlist => (
          <NavLink
            key={playlist.id}
            to={`/playlist/${playlist.id}`}
            className="playlist-item"
          >
            <img src={playlist.image} alt={playlist.name} />
            <div className="playlist-item-info">
              <div className="playlist-item-name">{playlist.name}</div>
              <div className="playlist-item-desc">{playlist.description}</div>
            </div>
          </NavLink>
        ))}
      </div>

      {showCreateModal && (
        <CreatePlaylistModal
          onClose={() => setShowCreateModal(false)}
        />
      )}
    </aside>
  );
};

const CreatePlaylistModal = ({ onClose }) => {
  const { createPlaylist } = useMusic();
  const [name, setName] = React.useState('');
  const [description, setDescription] = React.useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      createPlaylist(name, description);
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Crea Playlist</h2>
          <button className="modal-close" onClick={onClose}>
            <svg viewBox="0 0 24 24">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path>
            </svg>
          </button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="form-group">
              <label className="form-label">Nome</label>
              <input
                type="text"
                className="form-input"
                placeholder="Nome della playlist"
                value={name}
                onChange={(e) => setName(e.target.value)}
                autoFocus
              />
            </div>
            <div className="form-group">
              <label className="form-label">Descrizione (opzionale)</label>
              <input
                type="text"
                className="form-input"
                placeholder="Aggiungi una descrizione"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Annulla
            </button>
            <button type="submit" className="btn-primary">
              Crea
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Sidebar;
