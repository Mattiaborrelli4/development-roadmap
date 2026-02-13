import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';
import { getWeatherIcon } from '../services/weatherAPI';
import {
  formatTemperature,
  formatWindSpeed,
  getWindDirection,
  formatSunTime,
  translateWeatherCondition,
} from '../utils/helpers';
import { theme } from '../styles/theme';

const WeatherCard = ({ weather, location }) => {
  if (!weather) return null;

  return (
    <View style={styles.container}>
      {/* Località e data */}
      <View style={styles.header}>
        <View>
          <Text style={styles.cityName}>{location?.name || 'Caricamento...'}</Text>
          <Text style={styles.country}>{location?.country || ''}</Text>
        </View>
      </View>

      {/* Temperatura principale */}
      <View style={styles.mainWeather}>
        <Image
          source={{ uri: getWeatherIcon(weather.icon) }}
          style={styles.weatherIcon}
          resizeMode="contain"
        />
        <View>
          <Text style={styles.temperature}>
            {formatTemperature(weather.temp)}
          </Text>
          <Text style={styles.description}>
            {translateWeatherCondition(weather.condition)}
          </Text>
          <Text style={styles.feelsLike}>
            Percepita {formatTemperature(weather.feels_like)}
          </Text>
        </View>
      </View>

      {/* Temperature min/max */}
      <View style={styles.tempRange}>
        <View style={styles.tempItem}>
          <Text style={styles.tempLabel}>Min</Text>
          <Text style={styles.tempValue}>
            {formatTemperature(weather.temp_min)}
          </Text>
        </View>
        <View style={[styles.tempItem, styles.tempItemCenter]}>
          <Text style={styles.tempLabel}>Max</Text>
          <Text style={styles.tempValue}>
            {formatTemperature(weather.temp_max)}
          </Text>
        </View>
      </View>

      {/* Dettagli aggiuntivi */}
      <View style={styles.details}>
        <View style={styles.detailRow}>
          <View style={styles.detailItem}>
            <Text style={styles.detailIcon}>💧</Text>
            <Text style={styles.detailLabel}>Umidità</Text>
            <Text style={styles.detailValue}>{weather.humidity}%</Text>
          </View>

          <View style={styles.detailItem}>
            <Text style={styles.detailIcon}>💨</Text>
            <Text style={styles.detailLabel}>Vento</Text>
            <Text style={styles.detailValue}>
              {formatWindSpeed(weather.wind_speed)}
            </Text>
            <Text style={styles.detailSubvalue}>
              {getWindDirection(weather.wind_deg)}
            </Text>
          </View>

          <View style={styles.detailItem}>
            <Text style={styles.detailIcon}>👁️</Text>
            <Text style={styles.detailLabel}>Visibilità</Text>
            <Text style={styles.detailValue}>
              {(weather.visibility / 1000).toFixed(1)} km
            </Text>
          </View>
        </View>

        <View style={styles.detailRow}>
          <View style={styles.detailItem}>
            <Text style={styles.detailIcon}>🌅</Text>
            <Text style={styles.detailLabel}>Alba</Text>
            <Text style={styles.detailValue}>
              {formatSunTime(weather.sunrise)}
            </Text>
          </View>

          <View style={styles.detailItem}>
            <Text style={styles.detailIcon}>🌇</Text>
            <Text style={styles.detailLabel}>Tramonto</Text>
            <Text style={styles.detailValue}>
              {formatSunTime(weather.sunset)}
            </Text>
          </View>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: theme.borderRadius.lg,
    padding: theme.spacing.lg,
    margin: theme.spacing.md,
    ...theme.shadows.lg,
  },
  header: {
    marginBottom: theme.spacing.lg,
  },
  cityName: {
    fontSize: theme.fontSize.xxl,
    fontWeight: theme.fontWeight.bold,
    color: theme.colors.text,
    marginBottom: theme.spacing.xs,
  },
  country: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textLight,
  },
  mainWeather: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  weatherIcon: {
    width: 100,
    height: 100,
    marginRight: theme.spacing.lg,
  },
  temperature: {
    fontSize: 64,
    fontWeight: theme.fontWeight.light,
    color: theme.colors.text,
  },
  description: {
    fontSize: theme.fontSize.lg,
    color: theme.colors.textLight,
    marginTop: theme.spacing.xs,
    textTransform: 'capitalize',
  },
  feelsLike: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textLight,
    marginTop: theme.spacing.xs,
  },
  tempRange: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: theme.spacing.md,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: theme.colors.border,
    marginBottom: theme.spacing.lg,
  },
  tempItem: {
    alignItems: 'center',
    flex: 1,
  },
  tempItemCenter: {
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderColor: theme.colors.border,
  },
  tempLabel: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textLight,
    marginBottom: theme.spacing.xs,
  },
  tempValue: {
    fontSize: theme.fontSize.xl,
    fontWeight: theme.fontWeight.semibold,
    color: theme.colors.text,
  },
  details: {
    gap: theme.spacing.md,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  detailItem: {
    flex: 1,
    alignItems: 'center',
    paddingHorizontal: theme.spacing.sm,
  },
  detailIcon: {
    fontSize: 28,
    marginBottom: theme.spacing.xs,
  },
  detailLabel: {
    fontSize: theme.fontSize.xs,
    color: theme.colors.textLight,
    marginBottom: theme.spacing.xs,
  },
  detailValue: {
    fontSize: theme.fontSize.md,
    fontWeight: theme.fontWeight.semibold,
    color: theme.colors.text,
  },
  detailSubvalue: {
    fontSize: theme.fontSize.xs,
    color: theme.colors.textLight,
  },
});

export default WeatherCard;
