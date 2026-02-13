import React, { useState, useEffect, useRef } from 'react';
import { FiPlay, FiPause, FiSkipBack, FiSkipForward, FiShuffle, FiRepeat, FiHeart, FiVolume2, FiVolumeX } from 'react-icons/fi';
import { useMusic } from '../contexts/MusicContext';

const Player = () => {
  const {
    currentTrack,
    isPlaying,
    volume,
    progress,
    isMuted,
    shuffle,
    repeat,
    togglePlay,
    nextTrack,
    prevTrack,
    setVolume,
    toggleMute,
    setProgress,
    toggleShuffle,
    toggleRepeat,
    toggleLike,
    isLiked
  } = useMusic();

  const [localVolume, setLocalVolume] = useState(volume);
  const [localProgress, setLocalProgress] = useState(progress);
  const progressRef = useRef(null);
  const volumeRef = useRef(null);

  useEffect(() => {
    setLocalVolume(volume);
  }, [volume]);

  useEffect(() => {
    setLocalProgress(progress);
  }, [progress]);

  // Simulazione della progress bar
  useEffect(() => {
    let interval;
    if (isPlaying && currentTrack) {
      interval = setInterval(() => {
        setLocalProgress(prev => {
          const newProgress = prev + 0.5;
          if (newProgress >= 100) {
            if (repeat === 'one') {
              return 0;
            } else if (repeat === 'all') {
              nextTrack();
              return 0;
            } else {
              nextTrack();
              return 0;
            }
          }
          return newProgress;
        });
      }, 500);
    }
    return () => clearInterval(interval);
  }, [isPlaying, currentTrack, repeat, nextTrack]);

  const formatTime = (seconds) => {
    if (!currentTrack) return '0:00';
    const [mins, secs] = currentTrack.duration.split(':').map(Number);
    const totalSeconds = mins * 60 + secs;
    const currentSeconds = Math.floor((seconds / 100) * totalSeconds);
    const minsDisplay = Math.floor(currentSeconds / 60);
    const secsDisplay = currentSeconds % 60;
    return `${minsDisplay}:${secsDisplay.toString().padStart(2, '0')}`;
  };

  const handleProgressClick = (e) => {
    const rect = progressRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percentage = (x / rect.width) * 100;
    setLocalProgress(percentage);
    setProgress(percentage);
  };

  const handleVolumeClick = (e) => {
    const rect = volumeRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
    setLocalVolume(percentage);
    setVolume(percentage);
  };

  const getRepeatIcon = () => {
    if (repeat === 'one') {
      return <FiRepeat />;
    }
    return <FiRepeat />;
  };

  return (
    <div className="player-bar">
      <div className="player-left">
        {currentTrack && (
          <>
            <div className="now-playing">
              <img
                src={currentTrack.image}
                alt={currentTrack.title}
                className="now-playing-image"
              />
              <div className="now-playing-info">
                <div className="now-playing-title">{currentTrack.title}</div>
                <div className="now-playing-artist">{currentTrack.artist}</div>
              </div>
            </div>
            <button
              className={`like-button ${isLiked(currentTrack?.id) ? 'active' : ''}`}
              onClick={() => currentTrack && toggleLike(currentTrack.id)}
            >
              <svg viewBox="0 0 16 16">
                <path d="M1.69 2A4.582 4.582 0 018 2.023 4.583 4.583 0 0111.758 4.5c2.058 2.381 1.693 6.31-1.885 9.747L8 15.38l-1.873-1.133C2.55 10.811 2.187 6.88 4.245 4.5A4.582 4.582 0 011.69 2zm4.897 12.65l.356.214.357-.214C9.316 13.17 11.25 11.254 11.25 8.5a3 3 0 00-6 0c0 2.754 1.934 4.67 4.337 6.15z" />
              </svg>
            </button>
          </>
        )}
      </div>

      <div className="player-center">
        <div className="player-controls">
          <button
            className={`control-btn ${shuffle ? 'active' : ''}`}
            onClick={toggleShuffle}
            title="Casuale"
          >
            <FiShuffle />
          </button>
          <button
            className="control-btn"
            onClick={prevTrack}
            title="Precedente"
          >
            <FiSkipBack />
          </button>
          <button
            className="control-btn play-btn"
            onClick={togglePlay}
            title={isPlaying ? 'Pausa' : 'Riproduci'}
          >
            {isPlaying ? <FiPause /> : <FiPlay />}
          </button>
          <button
            className="control-btn"
            onClick={nextTrack}
            title="Successivo"
          >
            <FiSkipForward />
          </button>
          <button
            className={`control-btn ${repeat !== 'off' ? 'active' : ''}`}
            onClick={toggleRepeat}
            title={repeat === 'one' ? 'Ripeti brano' : repeat === 'all' ? 'Ripeti tutto' : 'Disattiva ripetizione'}
          >
            {getRepeatIcon()}
            {repeat === 'one' && <span style={{ fontSize: '10px', position: 'absolute', bottom: '2px' }}>1</span>}
          </button>
        </div>

        <div className="progress-container">
          <span className="progress-time">{formatTime(localProgress)}</span>
          <div
            className="progress-bar"
            ref={progressRef}
            onClick={handleProgressClick}
          >
            <div
              className="progress-bar-fill"
              style={{ width: `${localProgress}%` }}
            >
              <div className="progress-handle"></div>
            </div>
          </div>
          <span className="progress-time">{currentTrack ? currentTrack.duration : '0:00'}</span>
        </div>
      </div>

      <div className="player-right">
        <button
          className="control-btn"
          onClick={toggleMute}
          title={isMuted ? 'Attiva volume' : 'Disattiva volume'}
        >
          {isMuted || localVolume === 0 ? <FiVolumeX /> : <FiVolume2 />}
        </button>
        <div className="volume-bar-container">
          <div
            className="volume-bar"
            ref={volumeRef}
            onClick={handleVolumeClick}
          >
            <div
              className="volume-bar-fill"
              style={{ width: `${isMuted ? 0 : localVolume}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Player;
