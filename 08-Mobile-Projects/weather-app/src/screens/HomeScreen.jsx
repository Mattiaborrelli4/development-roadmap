import React, { useEffect, useCallback, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  ImageBackground,
  Alert,
  Image,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';

import { useWeather } from '../hooks/useWeather';
import { useLocation } from '../hooks/useLocation';
import WeatherCard from '../components/WeatherCard';
import ForecastItem from '../components/ForecastItem';
import LocationButton from '../components/LocationButton';
import LoadingSpinner from '../components/LoadingSpinner';
import SearchBar from '../components/SearchBar';
import { getLastCity, cacheLastCity } from '../utils/cache';
import { theme } from '../styles/theme';

const HomeScreen = () => {
  const navigation = useNavigation();
  const [searchText, setSearchText] = useState('');

  const {
    weather,
    forecast,
    location,
    loading,
    error,
    isRefreshing,
    loadWeatherByCoords,
    refreshWeather,
    getGradient,
  } = useWeather();

  const {
    getCurrentPosition,
    loading: locationLoading,
  } = useLocation();

  // Carica l'ultima città salvata o la posizione corrente
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      // Prima tenta di recuperare l'ultima città
      const lastCity = await getLastCity();

      if (lastCity) {
        // Carica l'ultima città (da implementare con cache)
        console.log('Ultima città:', lastCity);
      }

      // Se non c'è una città salvata, chiedi la posizione
      await handleLocationPress();
    } catch (err) {
      console.error('Errore nel caricamento iniziale:', err);
    }
  };

  const handleLocationPress = async () => {
    try {
      const pos = await getCurrentPosition();
      await loadWeatherByCoords(pos.latitude, pos.longitude);

      if (location) {
        await cacheLastCity(location.name);
      }
    } catch (err) {
      Alert.alert('Errore', err.message || 'Impossibile ottenere la posizione');
    }
  };

  const handleSearch = () => {
    if (searchText.trim()) {
      navigation.navigate('Search', { initialQuery: searchText });
    }
  };

  const handleRefresh = useCallback(() => {
    refreshWeather();
  }, [refreshWeather]);

  const renderContent = () => {
    if (loading && !weather) {
      return <LoadingSpinner message="Caricamento meteo..." />;
    }

    if (error && !weather) {
      return (
        <View style={styles.errorContainer}>
          <Ionicons name="alert-circle" size={64} color={theme.colors.error} />
          <Text style={styles.errorTitle}>Errore</Text>
          <Text style={styles.errorMessage}>{error}</Text>
          <TouchableOpacity
            style={styles.retryButton}
            onPress={handleLocationPress}
          >
            <Text style={styles.retryButtonText}>Riprova</Text>
          </TouchableOpacity>
        </View>
      );
    }

    if (!weather) {
      return (
        <View style={styles.welcomeContainer}>
          <Ionicons name="cloud-outline" size={100} color={theme.colors.primary} />
          <Text style={styles.welcomeTitle}>Benvenuto in Weather App</Text>
          <Text style={styles.welcomeSubtitle}>
            Scopri il meteo della tua posizione
          </Text>
          <LocationButton
            onPress={handleLocationPress}
            loading={locationLoading}
          />
        </View>
      );
    }

    const gradient = getGradient();

    return (
      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl
            refreshing={isRefreshing}
            onRefresh={handleRefresh}
            tintColor={theme.colors.textWhite}
          />
        }
        showsVerticalScrollIndicator={false}
      >
        <LinearGradient
          colors={gradient}
          style={styles.header}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <View style={styles.searchContainer}>
            <SearchBar
              value={searchText}
              onChangeText={setSearchText}
              onSubmit={handleSearch}
              placeholder="Cerca un'altra città..."
            />
          </View>
        </LinearGradient>

        <WeatherCard weather={weather} location={location} />

        <View style={styles.forecastContainer}>
          <View style={styles.forecastHeader}>
            <Ionicons
              name="calendar-outline"
              size={24}
              color={theme.colors.text}
            />
            <Text style={styles.forecastTitle}>Previsioni 5 giorni</Text>
          </View>

          {forecast.map((day, index) => (
            <ForecastItem key={`${day.date}-${index}`} day={day} index={index} />
          ))}
        </View>

        <View style={styles.footer}>
          <TouchableOpacity
            style={styles.locationButton}
            onPress={handleLocationPress}
          >
            <Ionicons name="navigate" size={20} color={theme.colors.primary} />
            <Text style={styles.locationButtonText}>
              Aggiorna posizione
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  };

  return <View style={styles.container}>{renderContent()}</View>;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  content: {
    flex: 1,
  },
  header: {
    paddingTop: 60,
    paddingBottom: theme.spacing.lg,
    paddingHorizontal: theme.spacing.md,
    borderBottomLeftRadius: theme.borderRadius.xl,
    borderBottomRightRadius: theme.borderRadius.xl,
  },
  searchContainer: {
    marginTop: theme.spacing.md,
  },
  welcomeContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.xl,
  },
  welcomeTitle: {
    fontSize: theme.fontSize.xxl,
    fontWeight: theme.fontWeight.bold,
    color: theme.colors.text,
    marginTop: theme.spacing.lg,
    marginBottom: theme.spacing.sm,
  },
  welcomeSubtitle: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textLight,
    textAlign: 'center',
    marginBottom: theme.spacing.xl,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.xl,
  },
  errorTitle: {
    fontSize: theme.fontSize.xl,
    fontWeight: theme.fontWeight.bold,
    color: theme.colors.error,
    marginTop: theme.spacing.md,
    marginBottom: theme.spacing.sm,
  },
  errorMessage: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textLight,
    textAlign: 'center',
    marginBottom: theme.spacing.xl,
  },
  retryButton: {
    backgroundColor: theme.colors.primary,
    paddingHorizontal: theme.spacing.xl,
    paddingVertical: theme.spacing.md,
    borderRadius: theme.borderRadius.full,
  },
  retryButtonText: {
    color: theme.colors.textWhite,
    fontSize: theme.fontSize.md,
    fontWeight: theme.fontWeight.semibold,
  },
  forecastContainer: {
    marginTop: theme.spacing.md,
    paddingBottom: theme.spacing.lg,
  },
  forecastHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.md,
    paddingBottom: theme.spacing.sm,
    gap: theme.spacing.sm,
  },
  forecastTitle: {
    fontSize: theme.fontSize.lg,
    fontWeight: theme.fontWeight.semibold,
    color: theme.colors.text,
  },
  footer: {
    padding: theme.spacing.md,
    alignItems: 'center',
    paddingBottom: theme.spacing.xl,
  },
  locationButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: theme.spacing.sm,
    padding: theme.spacing.md,
  },
  locationButtonText: {
    fontSize: theme.fontSize.md,
    color: theme.colors.primary,
    fontWeight: theme.fontWeight.semibold,
  },
});

export default HomeScreen;
