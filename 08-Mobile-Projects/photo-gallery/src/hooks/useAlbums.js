import { useState, useEffect, useCallback } from 'react';
import { albumService } from '../services/albumService';

export const useAlbums = () => {
  const [albums, setAlbums] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carica gli album
  const loadAlbums = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await albumService.getAllAlbums();
      setAlbums(data);
    } catch (err) {
      setError(err.message);
      console.error('Errore nel caricare gli album:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Crea un nuovo album
  const createAlbum = useCallback(async (name, coverPhoto = null) => {
    try {
      const newAlbum = await albumService.createAlbum(name, coverPhoto);
      setAlbums(prev => [newAlbum, ...prev]);
      return newAlbum;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Aggiorna un album
  const updateAlbum = useCallback(async (albumId, updates) => {
    try {
      const updated = await albumService.updateAlbum(albumId, updates);
      setAlbums(prev =>
        prev.map(a => (a.id === albumId ? { ...a, ...updates } : a))
      );
      return updated;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Rinomina album
  const renameAlbum = useCallback(async (albumId, newName) => {
    try {
      const updated = await albumService.renameAlbum(albumId, newName);
      setAlbums(prev =>
        prev.map(a => (a.id === albumId ? { ...a, name: newName } : a))
      );
      return updated;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Aggiorna copertina album
  const updateCover = useCallback(async (albumId, coverPhoto) => {
    try {
      await albumService.updateAlbumCover(albumId, coverPhoto);
      setAlbums(prev =>
        prev.map(a => (a.id === albumId ? { ...a, coverPhoto } : a))
      );
      return true;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Cancella album
  const deleteAlbum = useCallback(async (albumId, movePhotosTo = null) => {
    try {
      await albumService.deleteAlbum(albumId, movePhotosTo);
      setAlbums(prev => prev.filter(a => a.id !== albumId));
      return true;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Aggiungi foto a un album
  const addPhotosToAlbum = useCallback(async (albumId, photoIds) => {
    try {
      await albumService.addPhotosToAlbum(albumId, photoIds);
      // Ricarica gli album per aggiornare i conteggi
      await loadAlbums();
      return true;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [loadAlbums]);

  // Rimuovi foto dagli album
  const removePhotosFromAlbum = useCallback(async (photoIds) => {
    try {
      await albumService.removePhotosFromAlbum(photoIds);
      // Ricarica gli album per aggiornare i conteggi
      await loadAlbums();
      return true;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [loadAlbums]);

  // Ottieni statistiche
  const getStats = useCallback(async () => {
    try {
      return await albumService.getAlbumStats();
    } catch (err) {
      setError(err.message);
      return null;
    }
  }, []);

  // Carica gli album all'avvio
  useEffect(() => {
    loadAlbums();
  }, [loadAlbums]);

  return {
    albums,
    loading,
    error,
    refresh: loadAlbums,
    createAlbum,
    updateAlbum,
    renameAlbum,
    updateCover,
    deleteAlbum,
    addPhotosToAlbum,
    removePhotosFromAlbum,
    getStats,
  };
};
