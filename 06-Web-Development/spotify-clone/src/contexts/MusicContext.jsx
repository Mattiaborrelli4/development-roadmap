import React, { createContext, useContext, useState, useReducer } from 'react';
import { tracks, playlists } from '../data';

const MusicContext = createContext();

export const useMusic = () => {
  const context = useContext(MusicContext);
  if (!context) {
    throw new Error('useMusic must be used within a MusicProvider');
  }
  return context;
};

const initialState = {
  currentTrack: null,
  isPlaying: false,
  playlist: [],
  currentIndex: 0,
  volume: 0.7,
  progress: 0,
  isMuted: false,
  shuffle: false,
  repeat: 'off', // 'off', 'all', 'one'
  userPlaylists: [...playlists]
};

function musicReducer(state, action) {
  switch (action.type) {
    case 'SET_TRACK':
      return { ...state, currentTrack: action.payload };
    case 'SET_PLAYING':
      return { ...state, isPlaying: action.payload };
    case 'SET_PLAYLIST':
      return { ...state, playlist: action.payload };
    case 'SET_CURRENT_INDEX':
      return { ...state, currentIndex: action.payload };
    case 'SET_VOLUME':
      return { ...state, volume: action.payload };
    case 'SET_PROGRESS':
      return { ...state, progress: action.payload };
    case 'SET_MUTED':
      return { ...state, isMuted: action.payload };
    case 'SET_SHUFFLE':
      return { ...state, shuffle: action.payload };
    case 'SET_REPEAT':
      return { ...state, repeat: action.payload };
    case 'ADD_PLAYLIST':
      return { ...state, userPlaylists: [...state.userPlaylists, action.payload] };
    case 'REMOVE_PLAYLIST':
      return {
        ...state,
        userPlaylists: state.userPlaylists.filter(p => p.id !== action.payload)
      };
    case 'UPDATE_PLAYLIST':
      return {
        ...state,
        userPlaylists: state.userPlaylists.map(p =>
          p.id === action.payload.id ? action.payload : p
        )
      };
    default:
      return state;
  }
}

export const MusicProvider = ({ children }) => {
  const [state, dispatch] = useReducer(musicReducer, initialState);
  const [searchQuery, setSearchQuery] = useState('');
  const [likedTracks, setLikedTracks] = useState(new Set());

  const playTrack = (track, playlist = [], index = 0) => {
    dispatch({ type: 'SET_TRACK', payload: track });
    dispatch({ type: 'SET_PLAYING', payload: true });
    if (playlist.length > 0) {
      dispatch({ type: 'SET_PLAYLIST', payload: playlist });
      dispatch({ type: 'SET_CURRENT_INDEX', payload: index });
    }
  };

  const togglePlay = () => {
    if (!state.currentTrack) {
      // Se non c'è una traccia selezionata, riproduci la prima
      const firstTrack = tracks[0];
      playTrack(firstTrack, tracks, 0);
    } else {
      dispatch({ type: 'SET_PLAYING', payload: !state.isPlaying });
    }
  };

  const nextTrack = () => {
    if (state.playlist.length === 0) return;

    let nextIndex;
    if (state.shuffle) {
      // Modalità shuffle: indice casuale
      nextIndex = Math.floor(Math.random() * state.playlist.length);
    } else {
      // Modalità normale: prossima traccia
      nextIndex = (state.currentIndex + 1) % state.playlist.length;
    }

    const trackId = state.playlist[nextIndex];
    const track = tracks.find(t => t.id === trackId);
    if (track) {
      dispatch({ type: 'SET_TRACK', payload: track });
      dispatch({ type: 'SET_CURRENT_INDEX', payload: nextIndex });
    }
  };

  const prevTrack = () => {
    if (state.playlist.length === 0) return;

    let prevIndex;
    if (state.shuffle) {
      prevIndex = Math.floor(Math.random() * state.playlist.length);
    } else {
      prevIndex = state.currentIndex === 0
        ? state.playlist.length - 1
        : state.currentIndex - 1;
    }

    const trackId = state.playlist[prevIndex];
    const track = tracks.find(t => t.id === trackId);
    if (track) {
      dispatch({ type: 'SET_TRACK', payload: track });
      dispatch({ type: 'SET_CURRENT_INDEX', payload: prevIndex });
    }
  };

  const setVolume = (volume) => {
    dispatch({ type: 'SET_VOLUME', payload: volume });
    if (volume > 0) {
      dispatch({ type: 'SET_MUTED', payload: false });
    }
  };

  const toggleMute = () => {
    dispatch({ type: 'SET_MUTED', payload: !state.isMuted });
  };

  const setProgress = (progress) => {
    dispatch({ type: 'SET_PROGRESS', payload: progress });
  };

  const toggleShuffle = () => {
    dispatch({ type: 'SET_SHUFFLE', payload: !state.shuffle });
  };

  const toggleRepeat = () => {
    const modes = ['off', 'all', 'one'];
    const currentModeIndex = modes.indexOf(state.repeat);
    const nextMode = modes[(currentModeIndex + 1) % modes.length];
    dispatch({ type: 'SET_REPEAT', payload: nextMode });
  };

  const toggleLike = (trackId) => {
    const newLiked = new Set(likedTracks);
    if (newLiked.has(trackId)) {
      newLiked.delete(trackId);
    } else {
      newLiked.add(trackId);
    }
    setLikedTracks(newLiked);
  };

  const isLiked = (trackId) => likedTracks.has(trackId);

  const createPlaylist = (name, description = '', image = '') => {
    const newPlaylist = {
      id: Date.now(),
      name,
      description,
      image: image || `https://picsum.photos/seed/${Date.now()}/300/300`,
      tracks: []
    };
    dispatch({ type: 'ADD_PLAYLIST', payload: newPlaylist });
    return newPlaylist;
  };

  const deletePlaylist = (playlistId) => {
    dispatch({ type: 'REMOVE_PLAYLIST', payload: playlistId });
  };

  const updatePlaylist = (playlist) => {
    dispatch({ type: 'UPDATE_PLAYLIST', payload: playlist });
  };

  const addTrackToPlaylist = (playlistId, trackId) => {
    const playlist = state.userPlaylists.find(p => p.id === playlistId);
    if (playlist && !playlist.tracks.includes(trackId)) {
      const updatedPlaylist = {
        ...playlist,
        tracks: [...playlist.tracks, trackId]
      };
      dispatch({ type: 'UPDATE_PLAYLIST', payload: updatedPlaylist });
    }
  };

  const removeTrackFromPlaylist = (playlistId, trackId) => {
    const playlist = state.userPlaylists.find(p => p.id === playlistId);
    if (playlist) {
      const updatedPlaylist = {
        ...playlist,
        tracks: playlist.tracks.filter(id => id !== trackId)
      };
      dispatch({ type: 'UPDATE_PLAYLIST', payload: updatedPlaylist });
    }
  };

  const value = {
    ...state,
    searchQuery,
    setSearchQuery,
    playTrack,
    togglePlay,
    nextTrack,
    prevTrack,
    setVolume,
    toggleMute,
    setProgress,
    toggleShuffle,
    toggleRepeat,
    toggleLike,
    isLiked,
    createPlaylist,
    deletePlaylist,
    updatePlaylist,
    addTrackToPlaylist,
    removeTrackFromPlaylist,
    allTracks: tracks
  };

  return (
    <MusicContext.Provider value={value}>
      {children}
    </MusicContext.Provider>
  );
};
