import { generateId } from '../utils/helpers';
import { storageService } from './storageService';
import { photoService } from './photoService';

export const albumService = {
  // Create album
  async createAlbum(name, coverPhoto = null) {
    try {
      const albums = await storageService.getAlbums();
      const newAlbum = {
        id: generateId(),
        name,
        coverPhoto,
        count: 0,
        createdAt: Date.now(),
      };

      albums.unshift(newAlbum);
      await storageService.saveAlbums(albums);
      return newAlbum;
    } catch (error) {
      console.error('Errore nel creare l\'album:', error);
      throw error;
    }
  },

  // Get all albums
  async getAllAlbums() {
    try {
      const albums = await storageService.getAlbums();
      const photos = await photoService.getAllPhotos();

      // Aggiorna il conteggio delle foto per ogni album
      return albums.map(album => ({
        ...album,
        count: photos.filter(p => p.albumId === album.id).length,
      }));
    } catch (error) {
      console.error('Errore nel recuperare gli album:', error);
      return [];
    }
  },

  // Get album by id
  async getAlbumById(albumId) {
    try {
      const albums = await storageService.getAlbums();
      const album = albums.find(a => a.id === albumId);

      if (album) {
        const photos = await photoService.getPhotosByAlbum(albumId);
        return {
          ...album,
          count: photos.length,
          photos,
        };
      }
      return null;
    } catch (error) {
      console.error('Errore nel recuperare l\'album:', error);
      return null;
    }
  },

  // Update album
  async updateAlbum(albumId, updates) {
    try {
      const albums = await storageService.getAlbums();
      const index = albums.findIndex(a => a.id === albumId);

      if (index !== -1) {
        albums[index] = { ...albums[index], ...updates };
        await storageService.saveAlbums(albums);
        return albums[index];
      }
      return null;
    } catch (error) {
      console.error('Errore nell\'aggiornare l\'album:', error);
      throw error;
    }
  },

  // Update album cover
  async updateAlbumCover(albumId, coverPhoto) {
    return await this.updateAlbum(albumId, { coverPhoto });
  },

  // Rename album
  async renameAlbum(albumId, newName) {
    return await this.updateAlbum(albumId, { name: newName });
  },

  // Delete album
  async deleteAlbum(albumId, movePhotosTo = null) {
    try {
      // Sposta le foto o rimuovi l'albumId
      const photos = await photoService.getPhotosByAlbum(albumId);

      if (movePhotosTo) {
        // Sposta le foto in un altro album
        for (const photo of photos) {
          await photoService.movePhotoToAlbum(photo.id, movePhotosTo);
        }
      } else {
        // Rimuovi l'albumId dalle foto
        for (const photo of photos) {
          await photoService.movePhotoToAlbum(photo.id, null);
        }
      }

      // Cancella l'album
      const albums = await storageService.getAlbums();
      const filtered = albums.filter(a => a.id !== albumId);
      await storageService.saveAlbums(filtered);

      return true;
    } catch (error) {
      console.error('Errore nel cancellare l\'album:', error);
      throw error;
    }
  },

  // Add photos to album
  async addPhotosToAlbum(albumId, photoIds) {
    try {
      for (const photoId of photoIds) {
        await photoService.movePhotoToAlbum(photoId, albumId);
      }
      return true;
    } catch (error) {
      console.error('Errore nell\'aggiungere le foto all\'album:', error);
      throw error;
    }
  },

  // Remove photos from album
  async removePhotosFromAlbum(photoIds) {
    try {
      for (const photoId of photoIds) {
        await photoService.movePhotoToAlbum(photoId, null);
      }
      return true;
    } catch (error) {
      console.error('Errore nel rimuovere le foto dall\'album:', error);
      throw error;
    }
  },

  // Get album statistics
  async getAlbumStats() {
    try {
      const albums = await storageService.getAlbums();
      const photos = await photoService.getAllPhotos();

      const photosInAlbums = photos.filter(p => p.albumId).length;
      const photosWithoutAlbum = photos.length - photosInAlbums;

      return {
        totalAlbums: albums.length,
        totalPhotos: photos.length,
        photosInAlbums,
        photosWithoutAlbum,
      };
    } catch (error) {
      console.error('Errore nel recuperare le statistiche:', error);
      return {
        totalAlbums: 0,
        totalPhotos: 0,
        photosInAlbums: 0,
        photosWithoutAlbum: 0,
      };
    }
  },
};
