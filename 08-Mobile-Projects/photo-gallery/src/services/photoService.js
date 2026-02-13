import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';
import { generateId } from '../utils/helpers';
import { storageService } from './storageService';

export const photoService = {
  // Request permissions
  async requestPermissions() {
    const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
    const { status: libraryStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();

    return {
      camera: cameraStatus === 'granted',
      library: libraryStatus === 'granted',
    };
  },

  // Take photo with camera
  async takePhoto() {
    try {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ['images'],
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
        exif: true,
      });

      if (!result.canceled && result.assets[0]) {
        const asset = result.assets[0];
        const fileInfo = await FileSystem.getInfoAsync(asset.uri);

        return {
          id: generateId(),
          uri: asset.uri,
          width: asset.width || 0,
          height: asset.height || 0,
          size: fileInfo.size || 0,
          createdAt: Date.now(),
          filter: 'none',
          albumId: null,
        };
      }
      return null;
    } catch (error) {
      console.error('Errore nel scattare la foto:', error);
      throw error;
    }
  },

  // Pick photo from gallery
  async pickFromGallery(multiple = false) {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ['images'],
        allowsMultipleSelection: multiple,
        allowsEditing: !multiple,
        aspect: [4, 3],
        quality: 0.8,
      });

      if (!result.canceled && result.assets) {
        const photos = [];

        for (const asset of result.assets) {
          const fileInfo = await FileSystem.getInfoAsync(asset.uri);

          photos.push({
            id: generateId(),
            uri: asset.uri,
            width: asset.width || 0,
            height: asset.height || 0,
            size: fileInfo.size || 0,
            createdAt: Date.now(),
            filter: 'none',
            albumId: null,
          });
        }

        return multiple ? photos : photos[0];
      }
      return null;
    } catch (error) {
      console.error('Errore nel selezionare la foto:', error);
      throw error;
    }
  },

  // Save photo to storage
  async savePhoto(photo) {
    try {
      const photos = await storageService.getPhotos();
      photos.unshift(photo);
      await storageService.savePhotos(photos);
      return photo;
    } catch (error) {
      console.error('Errore nel salvare la foto:', error);
      throw error;
    }
  },

  // Save multiple photos
  async savePhotos(newPhotos) {
    try {
      const photos = await storageService.getPhotos();
      photos.unshift(...newPhotos);
      await storageService.savePhotos(photos);
      return newPhotos;
    } catch (error) {
      console.error('Errore nel salvare le foto:', error);
      throw error;
    }
  },

  // Get all photos
  async getAllPhotos() {
    try {
      return await storageService.getPhotos();
    } catch (error) {
      console.error('Errore nel recuperare le foto:', error);
      return [];
    }
  },

  // Get photos by album
  async getPhotosByAlbum(albumId) {
    try {
      const photos = await storageService.getPhotos();
      return photos.filter(photo => photo.albumId === albumId);
    } catch (error) {
      console.error('Errore nel recuperare le foto dell\'album:', error);
      return [];
    }
  },

  // Update photo
  async updatePhoto(photoId, updates) {
    try {
      const photos = await storageService.getPhotos();
      const index = photos.findIndex(p => p.id === photoId);

      if (index !== -1) {
        photos[index] = { ...photos[index], ...updates };
        await storageService.savePhotos(photos);
        return photos[index];
      }
      return null;
    } catch (error) {
      console.error('Errore nell\'aggiornare la foto:', error);
      throw error;
    }
  },

  // Update photo filter
  async updatePhotoFilter(photoId, filter) {
    return await this.updatePhoto(photoId, { filter });
  },

  // Move photo to album
  async movePhotoToAlbum(photoId, albumId) {
    return await this.updatePhoto(photoId, { albumId });
  },

  // Delete photo
  async deletePhoto(photoId) {
    try {
      const photos = await storageService.getPhotos();
      const filtered = photos.filter(p => p.id !== photoId);
      await storageService.savePhotos(filtered);
      return true;
    } catch (error) {
      console.error('Errore nel cancellare la foto:', error);
      throw error;
    }
  },

  // Delete multiple photos
  async deletePhotos(photoIds) {
    try {
      const photos = await storageService.getPhotos();
      const filtered = photos.filter(p => !photoIds.includes(p.id));
      await storageService.savePhotos(filtered);
      return true;
    } catch (error) {
      console.error('Errore nel cancellare le foto:', error);
      throw error;
    }
  },

  // Share photo
  async sharePhoto(photoUri) {
    try {
      const isAvailable = await Sharing.isAvailableAsync();

      if (!isAvailable) {
        throw new Error('La condivisione non è disponibile su questo dispositivo');
      }

      await Sharing.shareAsync(photoUri, {
        mimeType: 'image/jpeg',
        dialogTitle: 'Condividi foto',
      });
    } catch (error) {
      console.error('Errore nella condivisione:', error);
      throw error;
    }
  },

  // Sort photos
  sortPhotos(photos, sortBy = 'date') {
    const sorted = [...photos];

    switch (sortBy) {
      case 'date':
        return sorted.sort((a, b) => b.createdAt - a.createdAt);
      case 'name':
        return sorted.sort((a, b) => a.uri.localeCompare(b.uri));
      case 'size':
        return sorted.sort((a, b) => b.size - a.size);
      default:
        return sorted;
    }
  },
};
