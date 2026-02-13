import { EXCHANGE_RATE_API_URL, EXCHANGE_RATE_API_KEY } from '../utils/constants';

/**
 * Servizio per le API dei tassi di cambio
 */

// Fetch dei tassi di cambio
export const fetchExchangeRates = async (baseCurrency = 'USD') => {
  try {
    // Usa la chiave API configurata
    const apiKey = EXCHANGE_RATE_API_KEY;

    // Se non c'è una chiave API, usa il piano gratuito
    const url = apiKey
      ? `${EXCHANGE_RATE_API_URL}/${apiKey}/latest/${baseCurrency}`
      : `https://v6.exchangerate-api.com/v6/latest/${baseCurrency}`;

    const response = await fetch(url);
    const data = await response.json();

    if (data.success === false) {
      throw new Error(data.error_type || 'Errore nel fetch dei tassi');
    }

    return {
      rates: data.conversion_rates,
      base: data.base_code,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    console.error('Errore nel fetch dei tassi di cambio:', error);
    throw error;
  }
};

// Converti importo tra valute
export const convertCurrency = (amount, fromCurrency, toCurrency, rates) => {
  try {
    if (fromCurrency === toCurrency) {
      return {
        amount,
        from: fromCurrency,
        to: toCurrency,
        result: amount,
        rate: 1,
        timestamp: new Date().toISOString(),
      };
    }

    // Ottieni il tasso di cambio
    const fromRate = rates[fromCurrency] || 1;
    const toRate = rates[toCurrency] || 1;

    // Converti prima nella valuta base poi nella valuta di destinazione
    const inBase = amount / fromRate;
    const result = inBase * toRate;
    const rate = toRate / fromRate;

    return {
      amount,
      from: fromCurrency,
      to: toCurrency,
      result: parseFloat(result.toFixed(2)),
      rate: parseFloat(rate.toFixed(6)),
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    console.error('Errore nella conversione:', error);
    throw error;
  }
};

// Formatta valuta per la visualizzazione
export const formatCurrency = (amount, currency, symbol) => {
  try {
    return new Intl.NumberFormat('it-IT', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(amount);
  } catch (error) {
    // Fallback se la valuta non è supportata da Intl
    return `${symbol}${amount.toFixed(2)}`;
  }
};

// Verifica se i tassi sono ancora validi (meno di 1 ora)
export const areRatesValid = (lastUpdate) => {
  if (!lastUpdate) return false;

  const now = new Date();
  const updateDate = new Date(lastUpdate);
  const diffInHours = (now - updateDate) / (1000 * 60 * 60);

  return diffInHours < 1;
};
