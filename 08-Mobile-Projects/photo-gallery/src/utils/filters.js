import { Image } from 'react-native';

// Configurazioni dei filtri immagine
export const FILTERS = {
  none: {
    name: 'Originale',
    nameEn: 'Original',
    filter: [],
  },
  grayscale: {
    name: 'Bianco e Nero',
    nameEn: 'Grayscale',
    filter: [
      { name: 'hueRotate', value: 0 },
      { name: 'saturation', value: 0 },
    ],
  },
  sepia: {
    name: 'Seppia',
    nameEn: 'Sepia',
    filter: [
      { name: 'sepia', value: 1 },
    ],
  },
  vintage: {
    name: 'Vintage',
    nameEn: 'Vintage',
    filter: [
      { name: 'sepia', value: 0.3 },
      { name: 'contrast', value: 1.2 },
      { name: 'brightness', value: 0.9 },
      { name: 'saturation', value: 0.8 },
    ],
  },
  warm: {
    name: 'Caldo',
    nameEn: 'Warm',
    filter: [
      { name: 'sepia', value: 0.2 },
      { name: 'brightness', value: 1.1 },
      { name: 'saturation', value: 1.2 },
    ],
  },
  cool: {
    name: 'Freddo',
    nameEn: 'Cool',
    filter: [
      { name: 'hueRotate', value: 180 },
      { name: 'saturation', value: 0.8 },
      { name: 'brightness', value: 1.05 },
    ],
  },
  dramatic: {
    name: 'Drammatico',
    nameEn: 'Dramatic',
    filter: [
      { name: 'contrast', value: 1.5 },
      { name: 'saturation', value: 1.2 },
      { name: 'brightness', value: 0.9 },
    ],
  },
  blur: {
    name: 'Sfocato',
    nameEn: 'Blur',
    filter: [
      { name: 'blur', value: 2 },
    ],
  },
};

export const getFilterArray = (filterType) => {
  const filter = FILTERS[filterType] || FILTERS.none;
  return filter.filter;
};

export const getFilterName = (filterType) => {
  const filter = FILTERS[filterType] || FILTERS.none;
  return filter.name;
};

export const getFilterStyles = (filterType) => {
  const filterArray = getFilterArray(filterType);
  const style = {};

  filterArray.forEach(item => {
    switch (item.name) {
      case 'sepia':
        style.sepia = item.value;
        break;
      case 'grayscale':
        style.grayscale = item.value;
        break;
      case 'contrast':
        style.contrast = item.value;
        break;
      case 'brightness':
        style.brightness = item.value;
        break;
      case 'saturation':
        style.saturation = item.value;
        break;
      case 'hueRotate':
        style.hueRotate = item.value;
        break;
      case 'blur':
        style.blur = item.value;
        break;
      case 'invert':
        style.invert = item.value;
        break;
    }
  });

  return style;
};

// Funzione per applicare filtri CSS-style a componenti
export const applyFilterStyle = (filterType) => {
  const filter = FILTERS[filterType] || FILTERS.none;
  const filterArray = filter.filter;

  return filterArray.map(f => {
    const value = typeof f.value === 'number' ? f.value * 100 : f.value;
    const unit = f.name === 'blur' ? 'px' : '%';
    return `${f.name}(${f.value}${f.name === 'hueRotate' ? 'deg' : unit})`;
  }).join(' ');
};

// Ottieni tutti i filtri disponibili
export const getAllFilters = () => {
  return Object.keys(FILTERS).map(key => ({
    key,
    ...FILTERS[key]
  }));
};
