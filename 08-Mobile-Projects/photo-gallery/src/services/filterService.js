import { FILTERS, getFilterName, getFilterStyles } from '../utils/filters';
import { photoService } from './photoService';

export const filterService = {
  // Get all available filters
  getAllFilters() {
    return Object.keys(FILTERS).map(key => ({
      key,
      ...FILTERS[key]
    }));
  },

  // Get filter by name
  getFilter(filterType) {
    return FILTERS[filterType] || FILTERS.none;
  },

  // Apply filter to photo
  async applyFilterToPhoto(photoId, filterType) {
    try {
      const updated = await photoService.updatePhotoFilter(photoId, filterType);
      return updated;
    } catch (error) {
      console.error('Errore nell\'applicare il filtro:', error);
      throw error;
    }
  },

  // Apply filter to multiple photos
  async applyFilterToPhotos(photoIds, filterType) {
    try {
      const promises = photoIds.map(id =>
        photoService.updatePhotoFilter(id, filterType)
      );
      const results = await Promise.all(promises);
      return results;
    } catch (error) {
      console.error('Errore nell\'applicare i filtri:', error);
      throw error;
    }
  },

  // Remove filter from photo
  async removeFilterFromPhoto(photoId) {
    return await this.applyFilterToPhoto(photoId, 'none');
  },

  // Get filter preview style
  getFilterPreviewStyle(filterType) {
    const filter = this.getFilter(filterType);
    return {
      filter: filter.filter.map(f => {
        const value = typeof f.value === 'number' ? f.value * 100 : f.value;
        const unit = f.name === 'blur' ? 'px' : '%';
        return `${f.name}(${f.value}${f.name === 'hueRotate' ? 'deg' : unit})`;
      }).join(' '),
    };
  },

  // Get filter information
  getFilterInfo(filterType) {
    const filter = this.getFilter(filterType);
    return {
      key: filterType,
      name: filter.name,
      nameEn: filter.nameEn,
      filterArray: filter.filter,
    };
  },

  // Check if filter is valid
  isValidFilter(filterType) {
    return FILTERS.hasOwnProperty(filterType);
  },

  // Get random filter (excluding none)
  getRandomFilter() {
    const filters = Object.keys(FILTERS).filter(key => key !== 'none');
    return filters[Math.floor(Math.random() * filters.length)];
  },
};
