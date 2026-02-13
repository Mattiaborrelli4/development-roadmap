import { Dimensions, Platform } from 'react-native';

export const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

export const isIOS = Platform.OS === 'ios';

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

export const formatDate = (timestamp) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;

  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 7) {
    return date.toLocaleDateString('it-IT', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  } else if (days > 0) {
    return `${days} ${days === 1 ? 'giorno fa' : 'giorni fa'}`;
  } else if (hours > 0) {
    return `${hours} ${hours === 1 ? 'ora fa' : 'ore fa'}`;
  } else if (minutes > 0) {
    return `${minutes} ${minutes === 1 ? 'minuto fa' : 'minuti fa'}`;
  } else {
    return 'Adesso';
  }
};

export const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

export const getFileExtension = (filename) => {
  return filename.slice(((filename.lastIndexOf('.') - 1) >>> 0) + 2);
};

export const validateImageUri = (uri) => {
  return uri && (uri.startsWith('http') || uri.startsWith('file') || uri.startsWith('/'));
};

export const calculateGridColumns = (screenWidth, itemSize = 100) => {
  const spacing = 8;
  const availableWidth = screenWidth - (spacing * 2);
  return Math.floor(availableWidth / (itemSize + spacing));
};
