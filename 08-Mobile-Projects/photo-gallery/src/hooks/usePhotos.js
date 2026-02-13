import { useState, useEffect, useCallback } from 'react';
import { photoService } from '../services/photoService';

export const usePhotos = (albumId = null) => {
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carica le foto
  const loadPhotos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      let data;
      if (albumId) {
        data = await photoService.getPhotosByAlbum(albumId);
      } else {
        data = await photoService.getAllPhotos();
      }

      setPhotos(data);
    } catch (err) {
      setError(err.message);
      console.error('Errore nel caricare le foto:', err);
    } finally {
      setLoading(false);
    }
  }, [albumId]);

  // Aggiungi una foto
  const addPhoto = useCallback(async (photo) => {
    try {
      const newPhoto = await photoService.savePhoto(photo);
      setPhotos(prev => [newPhoto, ...prev]);
      return newPhoto;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Aggiungi più foto
  const addPhotos = useCallback(async (newPhotos) => {
    try {
      await photoService.savePhotos(newPhotos);
      setPhotos(prev => [...newPhotos, ...prev]);
      return newPhotos;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Aggiorna una foto
  const updatePhoto = useCallback(async (photoId, updates) => {
    try {
      const updated = await photoService.updatePhoto(photoId, updates);
      setPhotos(prev =>
        prev.map(p => (p.id === photoId ? { ...p, ...updates } : p))
      );
      return updated;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Cancella una foto
  const deletePhoto = useCallback(async (photoId) => {
    try {
      await photoService.deletePhoto(photoId);
      setPhotos(prev => prev.filter(p => p.id !== photoId));
      return true;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Cancella più foto
  const deletePhotos = useCallback(async (photoIds) => {
    try {
      await photoService.deletePhotos(photoIds);
      setPhotos(prev => prev.filter(p => !photoIds.includes(p.id)));
      return true;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Applica filtro a una foto
  const applyFilter = useCallback(async (photoId, filter) => {
    try {
      await photoService.updatePhotoFilter(photoId, filter);
      setPhotos(prev =>
        prev.map(p => (p.id === photoId ? { ...p, filter } : p))
      );
      return true;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Sposta foto in un album
  const moveToAlbum = useCallback(async (photoId, targetAlbumId) => {
    try {
      await photoService.movePhotoToAlbum(photoId, targetAlbumId);

      if (albumId === null || targetAlbumId === albumId) {
        setPhotos(prev =>
          prev.map(p => (p.id === photoId ? { ...p, albumId: targetAlbumId } : p))
        );
      } else {
        setPhotos(prev => prev.filter(p => p.id !== photoId));
      }

      return true;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [albumId]);

  // Condividi foto
  const sharePhoto = useCallback(async (photoUri) => {
    try {
      await photoService.sharePhoto(photoUri);
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  // Ordina le foto
  const sortPhotos = useCallback((sortBy) => {
    const sorted = photoService.sortPhotos(photos, sortBy);
    setPhotos(sorted);
  }, [photos]);

  // Carica le foto all'avvio
  useEffect(() => {
    loadPhotos();
  }, [loadPhotos]);

  return {
    photos,
    loading,
    error,
    refresh: loadPhotos,
    addPhoto,
    addPhotos,
    updatePhoto,
    deletePhoto,
    deletePhotos,
    applyFilter,
    moveToAlbum,
    sharePhoto,
    sortPhotos,
  };
};
