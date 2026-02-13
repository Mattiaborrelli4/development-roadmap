import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  StatusBar,
  RefreshControl,
} from 'react-native';
import { useCurrencies } from '../hooks/useCurrencies';
import { useConverter } from '../hooks/useConverter';
import { clearHistory } from '../services/storageService';
import { COLORS, SPACING, FONT_SIZES } from '../styles/theme';

// Componenti
import CurrencyInput from '../components/CurrencyInput';
import CurrencyPicker from '../components/CurrencyPicker';
import SwapButton from '../components/SwapButton';
import ResultCard from '../components/ResultCard';
import HistoryList from '../components/HistoryList';
import FavoritesBar from '../components/FavoritesBar';

const ConverterScreen = () => {
  const { rates, isLoading, isOnline, lastUpdate, error, refreshRates } =
    useCurrencies();

  const {
    fromCurrency,
    setFromCurrency,
    toCurrency,
    setToCurrency,
    amount,
    setAmount,
    result,
    favorites,
    history,
    convert,
    swapCurrencies,
    toggleFavorite,
    selectCurrencyPair,
    getCurrencyInfo,
    isFavorite,
    loadData,
  } = useConverter(rates);

  const [showFromPicker, setShowFromPicker] = useState(false);
  const [showToPicker, setShowToPicker] = useState(false);
  const [converting, setConverting] = useState(false);

  // Carica dati all'avvio
  useEffect(() => {
    if (rates) {
      loadData();
    }
  }, [rates]);

  // Converti quando cambiano i parametri
  useEffect(() => {
    if (amount && rates) {
      const timer = setTimeout(() => {
        convert();
        setConverting(false);
      }, 500);

      return () => clearTimeout(timer);
    }
  }, [amount, fromCurrency, toCurrency, rates]);

  const handleAmountChange = (value) => {
    setConverting(true);
    // Validazione: solo numeri e punto decimale
    const cleaned = value.replace(/[^0-9.]/g, '');
    // Verifica che ci sia solo un punto decimale
    const parts = cleaned.split('.');
    if (parts.length > 2) {
      return;
    }
    setAmount(cleaned);
  };

  const handleSelectFromHistory = (item) => {
    setFromCurrency(item.from);
    setToCurrency(item.to);
    setAmount(item.amount.toString());
  };

  const handleClearHistory = async () => {
    const updated = await clearHistory();
    loadData();
  };

  const getCurrencyInfoByCode = (code) => {
    return getCurrencyInfo(code);
  };

  const formatLastUpdate = () => {
    if (!lastUpdate) return '';

    const now = new Date();
    const diff = now - lastUpdate;
    const minutes = Math.floor(diff / 60000);

    if (minutes < 1) return 'Appena aggiornato';
    if (minutes < 60) return `Aggiornato ${minutes} min fa`;

    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `Aggiornato ${hours} ore fa`;

    const days = Math.floor(hours / 24);
    return `Aggiornato ${days} giorni fa`;
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor={COLORS.surface} />

      {/* Header con stato rete */}
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>Convertitore Valute</Text>
          {lastUpdate && (
            <Text style={styles.updateText}>{formatLastUpdate()}</Text>
          )}
        </View>
        <View style={styles.statusContainer}>
          <View
            style={[
              styles.statusDot,
              { backgroundColor: isOnline ? COLORS.secondary : COLORS.error },
            ]}
          />
          <Text style={styles.statusText}>
            {isOnline ? 'Online' : 'Offline'}
          </Text>
        </View>
      </View>

      {/* Error message */}
      {error && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      <ScrollView
        style={styles.content}
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl
            refreshing={isLoading}
            onRefresh={refreshRates}
            colors={[COLORS.primary]}
            tintColor={COLORS.primary}
          />
        }
        showsVerticalScrollIndicator={false}
      >
        {/* Barra Preferiti */}
        <FavoritesBar
          favorites={favorites}
          onSelect={selectCurrencyPair}
          currentPair={{ from: fromCurrency, to: toCurrency }}
        />

        {/* Input Valuta Da */}
        <CurrencyInput
          label="Da"
          amount={amount}
          onAmountChange={handleAmountChange}
          currency={fromCurrency}
          onPress={() => setShowFromPicker(true)}
        />

        {/* Swap Button */}
        <SwapButton onPress={swapCurrencies} />

        {/* Input Valuta A */}
        <CurrencyInput
          label="A"
          amount={result ? result.result.toFixed(2) : ''}
          currency={toCurrency}
          onPress={() => setShowToPicker(true)}
          disabled
        />

        {/* Risultato */}
        <ResultCard
          result={result}
          currencyInfo={getCurrencyInfoByCode}
          onToggleFavorite={toggleFavorite}
          isFavorite={isFavorite(fromCurrency, toCurrency)}
        />

        {/* Cronologia */}
        <HistoryList
          history={history}
          onSelectItem={handleSelectFromHistory}
          onClear={handleClearHistory}
        />

        {/* Spazio per scroll */}
        <View style={{ height: SPACING.lg }} />
      </ScrollView>

      {/* Picker Valuta Da */}
      <CurrencyPicker
        visible={showFromPicker}
        onClose={() => setShowFromPicker(false)}
        onSelect={(code) => setFromCurrency(code)}
        selectedCurrency={fromCurrency}
        title="Seleziona Valuta di Partenza"
      />

      {/* Picker Valuta A */}
      <CurrencyPicker
        visible={showToPicker}
        onClose={() => setShowToPicker(false)}
        onSelect={(code) => setToCurrency(code)}
        selectedCurrency={toCurrency}
        title="Seleziona Valuta di Destinazione"
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: SPACING.md,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  title: {
    fontSize: FONT_SIZES.xl,
    fontWeight: '700',
    color: COLORS.text,
  },
  updateText: {
    fontSize: FONT_SIZES.xs,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: SPACING.xs,
  },
  statusText: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
  },
  errorContainer: {
    backgroundColor: '#FEE2E2',
    padding: SPACING.md,
    marginHorizontal: SPACING.md,
    marginTop: SPACING.md,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.error,
  },
  errorText: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.error,
  },
  content: {
    flex: 1,
  },
  scrollContent: {
    padding: SPACING.md,
  },
});

export default ConverterScreen;
