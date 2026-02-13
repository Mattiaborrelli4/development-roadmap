import { useState, useEffect } from 'react';
import NetInfo from '@react-native-community/netinfo';
import { fetchExchangeRates } from '../services/currencyAPI';
import {
  loadCachedRates,
  cacheRates,
  getLastUpdate,
} from '../services/storageService';
import { areRatesValid } from '../services/currencyAPI';

/**
 * Hook per gestire i tassi di cambio e lo stato di rete
 */
export const useCurrencies = () => {
  const [rates, setRates] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isOnline, setIsOnline] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [error, setError] = useState(null);

  // Carica i tassi (online o offline)
  const loadRates = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Prima prova a caricare dalla cache
      const cachedRates = await loadCachedRates();
      const cachedUpdate = await getLastUpdate();

      // Se siamo online e i tassi non sono validi, aggiorna
      const netInfo = await NetInfo.fetch();
      const shouldUpdate = !areRatesValid(cachedUpdate) && netInfo.isConnected;

      if (shouldUpdate) {
        try {
          const data = await fetchExchangeRates();
          setRates(data.rates);
          setLastUpdate(new Date());
          await cacheRates(data.rates);
        } catch (apiError) {
          // Se l'API fallisce, usa la cache se disponibile
          if (cachedRates) {
            setRates(cachedRates);
            setLastUpdate(cachedUpdate);
            setError('Utilizzando tassi cached. Aggiornamento fallito.');
          } else {
            throw apiError;
          }
        }
      } else if (cachedRates) {
        // Usa i tassi cached
        setRates(cachedRates);
        setLastUpdate(cachedUpdate);
        if (!netInfo.isConnected) {
          setError('Modalità offline. Tassi aggiornati all\'ultima connessione.');
        }
      } else {
        throw new Error('Nessun tasso disponibile. Controlla la connessione.');
      }
    } catch (err) {
      setError(err.message || 'Errore nel caricamento dei tassi');
      console.error('Errore nel caricamento dei tassi:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Monitora lo stato di rete
  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener((state) => {
      setIsOnline(state.isConnected);

      // Quando torni online, aggiorna i tassi se sono vecchi
      if (state.isConnected && rates) {
        const cachedUpdate = lastUpdate;
        if (!areRatesValid(cachedUpdate)) {
          loadRates();
        }
      }
    });

    return () => unsubscribe();
  }, [rates, lastUpdate]);

  // Carica i tassi al montaggio
  useEffect(() => {
    loadRates();
  }, []);

  // Aggiorna manualmente i tassi
  const refreshRates = async () => {
    const netInfo = await NetInfo.fetch();
    if (netInfo.isConnected) {
      await loadRates();
    } else {
      setError('Nessuna connessione internet. Impossibile aggiornare.');
    }
  };

  return {
    rates,
    isLoading,
    isOnline,
    lastUpdate,
    error,
    refreshRates,
  };
};
