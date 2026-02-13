import { useState, useCallback } from 'react';
import { convertCurrency } from '../services/currencyAPI';
import {
  addToHistory,
  loadFavorites,
  addFavorite,
  removeFavorite,
} from '../services/storageService';
import { CURRENCIES } from '../utils/constants';

/**
 * Hook per gestire la logica di conversione
 */
export const useConverter = (rates) => {
  const [fromCurrency, setFromCurrency] = useState('USD');
  const [toCurrency, setToCurrency] = useState('EUR');
  const [amount, setAmount] = useState('');
  const [result, setResult] = useState(null);
  const [favorites, setFavorites] = useState([]);
  const [history, setHistory] = useState([]);

  // Carica preferiti e cronologia
  const loadData = useCallback(async () => {
    try {
      const [favData, histData] = await Promise.all([
        loadFavorites(),
        loadHistory(),
      ]);
      setFavorites(favData);
      setHistory(histData);
    } catch (error) {
      console.error('Errore nel caricamento dei dati:', error);
    }
  }, []);

  // Esegui la conversione
  const convert = useCallback(async () => {
    if (!rates || !amount || parseFloat(amount) <= 0) {
      return;
    }

    try {
      const conversion = convertCurrency(
        parseFloat(amount),
        fromCurrency,
        toCurrency,
        rates
      );

      setResult(conversion);

      // Aggiungi alla cronologia
      const updatedHistory = await addToHistory(conversion);
      setHistory(updatedHistory);
    } catch (error) {
      console.error('Errore nella conversione:', error);
    }
  }, [rates, amount, fromCurrency, toCurrency]);

  // Swap delle valute
  const swapCurrencies = useCallback(() => {
    setFromCurrency(toCurrency);
    setToCurrency(fromCurrency);
    setResult(null);
  }, [fromCurrency, toCurrency]);

  // Gestione preferiti
  const toggleFavorite = useCallback(async () => {
    const exists = favorites.some(
      (fav) => fav.from === fromCurrency && fav.to === toCurrency
    );

    let updated;
    if (exists) {
      updated = await removeFavorite(fromCurrency, toCurrency);
    } else {
      updated = await addFavorite(fromCurrency, toCurrency);
    }

    setFavorites(updated);
  }, [favorites, fromCurrency, toCurrency]);

  // Seleziona una coppia di valute
  const selectCurrencyPair = useCallback((from, to) => {
    setFromCurrency(from);
    setToCurrency(to);
    setResult(null);
  }, []);

  // Ottieni info valuta
  const getCurrencyInfo = useCallback((code) => {
    return CURRENCIES.find((c) => c.code === code) || CURRENCIES[0];
  }, []);

  // Verifica se è un preferito
  const isFavorite = useCallback(
    (from, to) => {
      return favorites.some((fav) => fav.from === from && fav.to === to);
    },
    [favorites]
  );

  return {
    fromCurrency,
    setFromCurrency,
    toCurrency,
    setToCurrency,
    amount,
    setAmount,
    result,
    setResult,
    favorites,
    history,
    convert,
    swapCurrencies,
    toggleFavorite,
    selectCurrencyPair,
    getCurrencyInfo,
    isFavorite,
    loadData,
  };
};
