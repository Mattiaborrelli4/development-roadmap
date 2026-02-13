import AsyncStorage from '@react-native-async-storage/async-storage';

// Chiavi per lo storage
const KEYS = {
  POSTS: '@social_posts',
  LIKED_POSTS: '@social_liked_posts',
  SAVED_POSTS: '@social_saved_posts',
  PROFILE: '@social_profile',
  NOTIFICATIONS: '@social_notifications',
  MESSAGES: '@social_messages',
};

// Storage Service
class StorageService {
  // Salva dati
  static async save(key, data) {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(data));
      return true;
    } catch (error) {
      console.error('Errore nel salvataggio:', error);
      return false;
    }
  }

  // Recupera dati
  static async get(key) {
    try {
      const data = await AsyncStorage.getItem(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Errore nel recupero:', error);
      return null;
    }
  }

  // Rimuovi dati
  static async remove(key) {
    try {
      await AsyncStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error('Errore nella rimozione:', error);
      return false;
    }
  }

  // Pulisci tutti i dati
  static async clear() {
    try {
      await AsyncStorage.clear();
      return true;
    } catch (error) {
      console.error('Errore nella pulizia:', error);
      return false;
    }
  }

  // Posts
  async savePosts(posts) {
    return StorageService.save(KEYS.POSTS, posts);
  }

  async getPosts() {
    return StorageService.get(KEYS.POSTS);
  }

  // Liked posts
  async saveLikedPosts(postIds) {
    return StorageService.save(KEYS.LIKED_POSTS, postIds);
  }

  async getLikedPosts() {
    return StorageService.get(KEYS.LIKED_POSTS) || [];
  }

  async isPostLiked(postId) {
    const likedPosts = await this.getLikedPosts();
    return likedPosts.includes(postId);
  }

  async toggleLikePost(postId) {
    const likedPosts = await this.getLikedPosts();
    const index = likedPosts.indexOf(postId);

    if (index > -1) {
      likedPosts.splice(index, 1);
    } else {
      likedPosts.push(postId);
    }

    await this.saveLikedPosts(likedPosts);
    return likedPosts.includes(postId);
  }

  // Saved posts
  async saveSavedPosts(postIds) {
    return StorageService.save(KEYS.SAVED_POSTS, postIds);
  }

  async getSavedPosts() {
    return StorageService.get(KEYS.SAVED_POSTS) || [];
  }

  async isPostSaved(postId) {
    const savedPosts = await this.getSavedPosts();
    return savedPosts.includes(postId);
  }

  async toggleSavePost(postId) {
    const savedPosts = await this.getSavedPosts();
    const index = savedPosts.indexOf(postId);

    if (index > -1) {
      savedPosts.splice(index, 1);
    } else {
      savedPosts.push(postId);
    }

    await this.saveSavedPosts(savedPosts);
    return savedPosts.includes(postId);
  }

  // Profile
  async saveProfile(profile) {
    return StorageService.save(KEYS.PROFILE, profile);
  }

  async getProfile() {
    return StorageService.get(KEYS.PROFILE);
  }

  // Notifications
  async saveNotifications(notifications) {
    return StorageService.save(KEYS.NOTIFICATIONS, notifications);
  }

  async getNotifications() {
    return StorageService.get(KEYS.NOTIFICATIONS);
  }
}

export default new StorageService();
