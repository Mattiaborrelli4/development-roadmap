import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Player from './components/Player';
import Home from './pages/Home';
import Search from './pages/Search';
import Library from './pages/Library';
import PlaylistDetail from './pages/PlaylistDetail';
import Liked from './pages/Liked';
import { MusicProvider } from './contexts/MusicContext';
import './App.css';

function App() {
  return (
    <MusicProvider>
      <Router>
        <div className="app-container">
          <Sidebar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<Search />} />
            <Route path="/library" element={<Library />} />
            <Route path="/playlist/:id" element={<PlaylistDetail />} />
            <Route path="/liked" element={<Liked />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
        <Player />
      </Router>
    </MusicProvider>
  );
}

export default App;
