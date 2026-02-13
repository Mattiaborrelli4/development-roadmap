// Lista delle valute supportate con flag e simboli
export const CURRENCIES = [
  { code: 'USD', name: 'Dollaro Americano', symbol: '$', flag: '🇺🇸' },
  { code: 'EUR', name: 'Euro', symbol: '€', flag: '🇪🇺' },
  { code: 'GBP', name: 'Sterlina Britannica', symbol: '£', flag: '🇬🇧' },
  { code: 'JPY', name: 'Yen Giapponese', symbol: '¥', flag: '🇯🇵' },
  { code: 'CHF', name: 'Franco Svizzero', symbol: 'CHF', flag: '🇨🇭' },
  { code: 'CAD', name: 'Dollaro Canadese', symbol: 'C$', flag: '🇨🇦' },
  { code: 'AUD', name: 'Dollaro Australiano', symbol: 'A$', flag: '🇦🇺' },
];

// Chiave API gratuita per exchangerate-api.com
export const EXCHANGE_RATE_API_KEY = 'YOUR_API_KEY_HERE'; // Sostituisci con la tua chiave API
export const EXCHANGE_RATE_API_URL = 'https://v6.exchangerate-api.com/v6';

// Chiavi per AsyncStorage
export const STORAGE_KEYS = {
  FAVORITES: '@currency_converter:favorites',
  HISTORY: '@currency_converter:history',
  RATES_CACHE: '@currency_converter:rates_cache',
  LAST_UPDATE: '@currency_converter:last_update',
};

// Limiti
export const MAX_HISTORY_ITEMS = 10;
