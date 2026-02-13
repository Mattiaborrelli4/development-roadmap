import {useState, useEffect, useCallback} from 'react';
import storageService from '../services/storageService';
import syncService from '../services/syncService';
import {CATEGORIES} from '../utils/constants';

export const useItems = (listId) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, bought, unbought, category

  // Carica gli elementi
  const loadItems = useCallback(async () => {
    if (!listId) {
      setItems([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const data = await storageService.getItemsByListId(listId);
      setItems(data);
    } catch (err) {
      console.error('Errore nel caricamento degli elementi:', err);
    } finally {
      setLoading(false);
    }
  }, [listId]);

  // Aggiunge un elemento
  const addItem = useCallback(async (itemData) => {
    try {
      const newItem = {
        id: Date.now().toString() + Math.random(),
        listId,
        name: itemData.name,
        quantity: itemData.quantity || 1,
        category: itemData.category || 'Altro',
        bought: false,
        notes: itemData.notes || '',
        barcode: itemData.barcode || '',
        createdAt: new Date().toISOString(),
      };

      const success = await storageService.addItem(newItem);
      if (success) {
        setItems(prev => [...prev, newItem]);
        await syncService.sync();
        return newItem;
      }
      throw new Error('Errore nell\'aggiunta dell\'elemento');
    } catch (err) {
      console.error('Errore nell\'aggiunta:', err);
      throw err;
    }
  }, [listId]);

  // Aggiorna un elemento
  const updateItem = useCallback(async (itemId, updates) => {
    try {
      const success = await storageService.updateItem(itemId, updates);
      if (success) {
        setItems(prev =>
          prev.map(item =>
            item.id === itemId ? {...item, ...updates} : item
          )
        );
        await syncService.sync();
        return true;
      }
      throw new Error('Errore nell\'aggiornamento');
    } catch (err) {
      console.error('Errore nell\'aggiornamento:', err);
      throw err;
    }
  }, []);

  // Toggle bought status
  const toggleBought = useCallback(async (itemId) => {
    try {
      const item = items.find(i => i.id === itemId);
      if (!item) return;

      const success = await storageService.updateItem(itemId, {
        bought: !item.bought,
      });

      if (success) {
        setItems(prev =>
          prev.map(i =>
            i.id === itemId ? {...i, bought: !i.bought} : i
          )
        );
        await syncService.sync();
      }
    } catch (err) {
      console.error('Errore nel toggle:', err);
      throw err;
    }
  }, [items]);

  // Elimina un elemento
  const deleteItem = useCallback(async (itemId) => {
    try {
      const success = await storageService.deleteItem(itemId);
      if (success) {
        setItems(prev => prev.filter(item => item.id !== itemId));
        await syncService.sync();
        return true;
      }
      throw new Error('Errore nell\'eliminazione');
    } catch (err) {
      console.error('Errore nell\'eliminazione:', err);
      throw err;
    }
  }, []);

  // Sposta elementi in un'altra lista
  const moveItems = useCallback(async (itemIds, targetListId) => {
    try {
      for (const itemId of itemIds) {
        await updateItem(itemId, {listId: targetListId});
      }
      await loadItems();
      return true;
    } catch (err) {
      console.error('Errore nello spostamento:', err);
      throw err;
    }
  }, [updateItem, loadItems]);

  // Copia elementi in un'altra lista
  const copyItems = useCallback(async (itemIds, targetListId) => {
    try {
      const itemsToCopy = items.filter(i => itemIds.includes(i.id));
      for (const item of itemsToCopy) {
        await storageService.addItem({
          ...item,
          id: Date.now().toString() + Math.random(),
          listId: targetListId,
          bought: false,
        });
      }
      await syncService.sync();
      return true;
    } catch (err) {
      console.error('Errore nella copia:', err);
      throw err;
    }
  }, [items]);

  // Elimina gli elementi comprati
  const clearBoughtItems = useCallback(async () => {
    try {
      const success = await storageService.clearBoughtItems(listId);
      if (success) {
        setItems(prev => prev.filter(item => !item.bought));
        await syncService.sync();
        return true;
      }
      throw new Error('Errore nella pulizia');
    } catch (err) {
      console.error('Errore nella pulizia:', err);
      throw err;
    }
  }, [listId]);

  // Raggruppa elementi per categoria
  const getItemsByCategory = useCallback(() => {
    const filtered = items.filter(item => {
      if (filter === 'all') return true;
      if (filter === 'bought') return item.bought;
      if (filter === 'unbought') return !item.bought;
      return item.category === filter;
    });

    const grouped = {};
    CATEGORIES.forEach(cat => {
      grouped[cat.name] = filtered.filter(item => item.category === cat.name);
    });

    return grouped;
  }, [items, filter]);

  // Ottieni statistiche
  const getStatistics = useCallback(() => {
    const total = items.length;
    const bought = items.filter(i => i.bought).length;
    const unbought = total - bought;
    const byCategory = {};

    CATEGORIES.forEach(cat => {
      byCategory[cat.name] = items.filter(i => i.category === cat.name).length;
    });

    return {
      total,
      bought,
      unbought,
      completionRate: total > 0 ? ((bought / total) * 100).toFixed(1) : 0,
      byCategory,
    };
  }, [items]);

  // Carica gli elementi al mount o quando cambia listId
  useEffect(() => {
    loadItems();
  }, [listId, loadItems]);

  // Ascolta gli aggiornamenti dalla sincronizzazione
  useEffect(() => {
    const unsubscribe = syncService.addListener((event, data) => {
      if (event === 'remoteUpdate' || event === 'sync') {
        loadItems();
      }
    });

    return () => {
      unsubscribe();
    };
  }, [loadItems]);

  return {
    items,
    loading,
    filter,
    setFilter,
    addItem,
    updateItem,
    toggleBought,
    deleteItem,
    moveItems,
    copyItems,
    clearBoughtItems,
    getItemsByCategory,
    getStatistics,
    refresh: loadItems,
  };
};
