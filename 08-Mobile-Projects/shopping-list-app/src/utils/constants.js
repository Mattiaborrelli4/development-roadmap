// Categorie con icone e colori
export const CATEGORIES = [
  { name: 'Ortofrutta', icon: '🥬', color: '#4CAF50' },
  { name: 'Latticini', icon: '🥛', color: '#2196F3' },
  { name: 'Carne', icon: '🥩', color: '#F44336' },
  { name: 'Panificio', icon: '🍞', color: '#FF9800' },
  { name: 'Surgeleti', icon: '🧊', color: '#00BCD4' },
  { name: 'Dispensa', icon: '🥫', color: '#9C27B0' },
  { name: 'Bevande', icon: '🍷', color: '#E91E63' },
  { name: 'Casa', icon: '🧹', color: '#607D8B' },
  { name: 'Altro', icon: '📦', color: '#9E9E9E' }
];

// Icone per le liste
export const LIST_ICONS = ['🛒', '🛍️', '🏪', '🏬', '🎁', '📋', '✅', '⭐'];

// Colori per le liste
export const LIST_COLORS = [
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
  '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
];

// Database simulato di codici a barre
export const BARCODE_DATABASE = {
  '8001234567890': { name: 'Latte interno 1L', category: 'Latticini' },
  '8001234567891': { name: 'Pane integrale', category: 'Panificio' },
  '8001234567892': { name: 'Uova 12pz', category: 'Ortofrutta' },
  '8001234567893': { name: 'Pasta 500g', category: 'Dispensa' },
  '8001234567894': { name: 'Acqua 1.5L', category: 'Bevande' },
  '8001234567895': { name: 'Formaggio grattugiato', category: 'Latticini' },
  '8001234567896': { name: 'Pollo 1kg', category: 'Carne' },
  '8001234567897': { name: 'Pomodori 1kg', category: 'Ortofrutta' },
  '8001234567898': { name: 'Detersivo piatti', category: 'Casa' },
  '8001234567899': { name: 'Gelato vaniglia', category: 'Surgeleti' }
};

// Tema dell'app
export const THEME = {
  light: {
    background: '#FFFFFF',
    surface: '#F5F5F5',
    primary: '#4ECDC4',
    secondary: '#FF6B6B',
    text: '#2C3E50',
    textSecondary: '#7F8C8D',
    border: '#E0E0E0',
    success: '#4CAF50',
    warning: '#FF9800',
    error: '#F44336',
    shadow: 'rgba(0, 0, 0, 0.1)'
  },
  dark: {
    background: '#1A1A1A',
    surface: '#2D2D2D',
    primary: '#4ECDC4',
    secondary: '#FF6B6B',
    text: '#FFFFFF',
    textSecondary: '#B0B0B0',
    border: '#3D3D3D',
    success: '#4CAF50',
    warning: '#FF9800',
    error: '#F44336',
    shadow: 'rgba(0, 0, 0, 0.3)'
  }
};

// Costanti per le animazioni
export const ANIMATIONS = {
  duration: {
    fast: 200,
    normal: 300,
    slow: 500
  },
  easing: {
    ease: 'ease',
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out'
  }
};

// Chiavi per AsyncStorage
export const STORAGE_KEYS = {
  LISTS: '@shopping_lists',
  ITEMS: '@shopping_items',
  SETTINGS: '@shopping_settings',
  THEME: '@shopping_theme'
};
