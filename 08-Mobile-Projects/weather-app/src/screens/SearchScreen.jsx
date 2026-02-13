import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
  Keyboard,
  ScrollView,
} from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';

import SearchBar from '../components/SearchBar';
import { useWeather } from '../hooks/useWeather';
import { cacheLastCity } from '../utils/cache';
import { theme } from '../styles/theme';

const SearchScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { initialQuery } = route.params || {};

  const [searchText, setSearchText] = useState(initialQuery || '');
  const [cities, setCities] = useState([]);
  const [searching, setSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const { loadWeatherByCity } = useWeather();

  // Popolari città italiane
  const popularCities = [
    { name: 'Roma', country: 'IT' },
    { name: 'Milano', country: 'IT' },
    { name: 'Napoli', country: 'IT' },
    { name: 'Torino', country: 'IT' },
    { name: 'Palermo', country: 'IT' },
    { name: 'Genova', country: 'IT' },
    { name: 'Bologna', country: 'IT' },
    { name: 'Firenze', country: 'IT' },
    { name: 'Venezia', country: 'IT' },
    { name: 'Verona', country: 'IT' },
  ];

  useEffect(() => {
    if (initialQuery) {
      handleSearch(initialQuery);
    }
  }, [initialQuery]);

  useEffect(() => {
    const searchTimer = setTimeout(() => {
      performSearch(searchText);
    }, 300);

    return () => clearTimeout(searchTimer);
  }, [searchText]);

  const performSearch = (query) => {
    if (!query.trim()) {
      setCities([]);
      setHasSearched(false);
      return;
    }

    setSearching(true);
    setHasSearched(true);

    // Filtra le città popolari
    const filtered = popularCities.filter((city) =>
      city.name.toLowerCase().includes(query.toLowerCase())
    );

    setCities(filtered);
    setSearching(false);
  };

  const handleSearch = async (query) => {
    if (!query.trim()) return;

    Keyboard.dismiss();

    try {
      const data = await loadWeatherByCity(query);
      await cacheLastCity(data.location.name);
      navigation.goBack();
    } catch (error) {
      console.error('Errore nel caricamento:', error);
    }
  };

  const handleCitySelect = async (cityName) => {
    setSearchText(cityName);
    await handleSearch(cityName);
  };

  const renderCityItem = ({ item }) => (
    <TouchableOpacity
      style={styles.cityItem}
      onPress={() => handleCitySelect(item.name)}
    >
      <View style={styles.cityInfo}>
        <Ionicons name="location-outline" size={20} color={theme.colors.text} />
        <View style={styles.cityDetails}>
          <Text style={styles.cityName}>{item.name}</Text>
          <Text style={styles.countryName}>{item.country}</Text>
        </View>
      </View>
      <Ionicons name="chevron-forward" size={20} color={theme.colors.textLight} />
    </TouchableOpacity>
  );

  const renderPopularCities = () => (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>Città popolari</Text>
      <View style={styles.citiesGrid}>
        {popularCities.map((city) => (
          <TouchableOpacity
            key={city.name}
            style={styles.popularCityItem}
            onPress={() => handleCitySelect(city.name)}
          >
            <Text style={styles.popularCityName}>{city.name}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  const renderNoResults = () => {
    if (!hasSearched || searching) return null;

    return (
      <View style={styles.noResults}>
        <Ionicons name="search-outline" size={64} color={theme.colors.textLight} />
        <Text style={styles.noResultsTitle}>Nessun risultato</Text>
        <Text style={styles.noResultsText}>
          Prova a cercare un'altra città
        </Text>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Ionicons name="arrow-back" size={24} color={theme.colors.text} />
        </TouchableOpacity>
        <SearchBar
          value={searchText}
          onChangeText={setSearchText}
          onSubmit={() => handleSearch(searchText)}
          placeholder="Cerca città..."
        />
      </View>

      {searching ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="small" color={theme.colors.primary} />
          <Text style={styles.searchingText}>Ricerca in corso...</Text>
        </View>
      ) : cities.length > 0 ? (
        <FlatList
          data={cities}
          renderItem={renderCityItem}
          keyExtractor={(item) => item.name}
          contentContainerStyle={styles.list}
          ItemSeparatorComponent={() => <View style={styles.separator} />}
        />
      ) : (
        <ScrollView style={styles.content}>{renderPopularCities()}</ScrollView>
      )}

      {renderNoResults()}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop: 60,
    paddingBottom: theme.spacing.md,
    paddingHorizontal: theme.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  backButton: {
    marginRight: theme.spacing.sm,
    padding: theme.spacing.sm,
  },
  content: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    gap: theme.spacing.md,
  },
  searchingText: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textLight,
  },
  list: {
    paddingVertical: theme.spacing.sm,
  },
  cityItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
    backgroundColor: theme.colors.card,
  },
  cityInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    gap: theme.spacing.md,
  },
  cityDetails: {
    flex: 1,
  },
  cityName: {
    fontSize: theme.fontSize.md,
    fontWeight: theme.fontWeight.medium,
    color: theme.colors.text,
    marginBottom: 2,
  },
  countryName: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textLight,
  },
  separator: {
    height: 1,
    backgroundColor: theme.colors.border,
    marginLeft: theme.spacing.xl,
  },
  section: {
    padding: theme.spacing.lg,
  },
  sectionTitle: {
    fontSize: theme.fontSize.lg,
    fontWeight: theme.fontWeight.semibold,
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  citiesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: theme.spacing.sm,
  },
  popularCityItem: {
    backgroundColor: theme.colors.card,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.full,
    ...theme.shadows.sm,
  },
  popularCityName: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.text,
    fontWeight: theme.fontWeight.medium,
  },
  noResults: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.xl,
  },
  noResultsTitle: {
    fontSize: theme.fontSize.lg,
    fontWeight: theme.fontWeight.semibold,
    color: theme.colors.text,
    marginTop: theme.spacing.md,
  },
  noResultsText: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textLight,
    marginTop: theme.spacing.sm,
    textAlign: 'center',
  },
});

export default SearchScreen;
