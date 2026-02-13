import {useState, useEffect, useCallback} from 'react';
import storageService from '../services/storageService';
import syncService from '../services/syncService';

export const useLists = () => {
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carica le liste
  const loadLists = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await storageService.getLists();
      setLists(data);
    } catch (err) {
      setError(err.message);
      console.error('Errore nel caricamento delle liste:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Crea una nuova lista
  const createList = useCallback(async (listData) => {
    try {
      const newList = {
        id: Date.now().toString(),
        name: listData.name,
        icon: listData.icon || '🛒',
        color: listData.color || '#4ECDC4',
        shared: false,
        owner: 'Tu',
        createdAt: new Date().toISOString(),
        ...listData,
      };

      const success = await storageService.addList(newList);
      if (success) {
        setLists(prev => [...prev, newList]);
        await syncService.sync();
        return newList;
      }
      throw new Error('Errore nella creazione della lista');
    } catch (err) {
      setError(err.message);
      console.error('Errore nella creazione della lista:', err);
      throw err;
    }
  }, []);

  // Aggiorna una lista
  const updateList = useCallback(async (listId, updates) => {
    try {
      const success = await storageService.updateList(listId, updates);
      if (success) {
        setLists(prev =>
          prev.map(list =>
            list.id === listId ? {...list, ...updates} : list
          )
        );
        await syncService.sync();
        return true;
      }
      throw new Error('Errore nell\'aggiornamento della lista');
    } catch (err) {
      setError(err.message);
      console.error('Errore nell\'aggiornamento della lista:', err);
      throw err;
    }
  }, []);

  // Elimina una lista
  const deleteList = useCallback(async (listId) => {
    try {
      const success = await storageService.deleteList(listId);
      if (success) {
        setLists(prev => prev.filter(list => list.id !== listId));
        await syncService.sync();
        return true;
      }
      throw new Error('Errore nell\'eliminazione della lista');
    } catch (err) {
      setError(err.message);
      console.error('Errore nell\'eliminazione della lista:', err);
      throw err;
    }
  }, []);

  // Condividi una lista
  const shareList = useCallback(async (listId, email) => {
    try {
      const result = await syncService.shareList(listId, email);
      if (result.success) {
        await loadLists();
      }
      return result;
    } catch (err) {
      setError(err.message);
      console.error('Errore nella condivisione:', err);
      throw err;
    }
  }, [loadLists]);

  // Revoca la condivisione
  const unshareList = useCallback(async (listId, email) => {
    try {
      const result = await syncService.unshareList(listId, email);
      if (result.success) {
        await loadLists();
      }
      return result;
    } catch (err) {
      setError(err.message);
      console.error('Errore nella revoca:', err);
      throw err;
    }
  }, [loadLists]);

  // Duplica una lista
  const duplicateList = useCallback(async (listId) => {
    try {
      const listToDuplicate = lists.find(l => l.id === listId);
      if (!listToDuplicate) {
        throw new Error('Lista non trovata');
      }

      const items = await storageService.getItemsByListId(listId);
      const newList = {
        ...listToDuplicate,
        id: Date.now().toString(),
        name: `${listToDuplicate.name} (copia)`,
        createdAt: new Date().toISOString(),
        shared: false,
      };

      await storageService.addList(newList);

      // Copia gli elementi
      for (const item of items) {
        await storageService.addItem({
          ...item,
          id: Date.now().toString() + Math.random(),
          listId: newList.id,
        });
      }

      await loadLists();
      await syncService.sync();
      return newList;
    } catch (err) {
      setError(err.message);
      console.error('Errore nella duplicazione:', err);
      throw err;
    }
  }, [lists, loadLists]);

  // Carica le liste al mount
  useEffect(() => {
    loadLists();

    // Ascolta gli aggiornamenti dalla sincronizzazione
    const unsubscribe = syncService.addListener((event, data) => {
      if (event === 'remoteUpdate' || event === 'sync') {
        loadLists();
      }
    });

    return () => {
      unsubscribe();
    };
  }, [loadLists]);

  return {
    lists,
    loading,
    error,
    createList,
    updateList,
    deleteList,
    shareList,
    unshareList,
    duplicateList,
    refresh: loadLists,
  };
};
