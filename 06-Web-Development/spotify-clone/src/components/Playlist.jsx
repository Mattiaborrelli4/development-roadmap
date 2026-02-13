import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FiPlay } from 'react-icons/fi';

const PlaylistCard = ({ playlist }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/playlist/${playlist.id}`);
  };

  const handlePlayClick = (e) => {
    e.stopPropagation();
    // Qui si potrebbe implementare la riproduzione diretta
    handleClick();
  };

  return (
    <div className="playlist-card" onClick={handleClick}>
      <div className="playlist-card-image">
        <img src={playlist.image} alt={playlist.name} />
        <div className="play-button-overlay" onClick={handlePlayClick}>
          <FiPlay />
        </div>
      </div>
      <div className="playlist-card-title">{playlist.name}</div>
      <div className="playlist-card-desc">{playlist.description}</div>
    </div>
  );
};

export default PlaylistCard;
