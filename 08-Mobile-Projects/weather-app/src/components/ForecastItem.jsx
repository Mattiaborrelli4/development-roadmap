import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';
import { getWeatherIcon } from '../services/weatherAPI';
import { getDayName, formatTemperature, translateWeatherCondition } from '../utils/helpers';
import { theme } from '../styles/theme';

const ForecastItem = ({ day, index }) => {
  const isToday = index === 0;

  return (
    <View style={styles.container}>
      <View style={styles.dayContainer}>
        <Text style={styles.dayText}>
          {isToday ? 'Oggi' : getDayName(day.timestamp)}
        </Text>
      </View>

      <Image
        source={{ uri: getWeatherIcon(day.icon) }}
        style={styles.icon}
        resizeMode="contain"
      />

      <View style={styles.temperatures}>
        <Text style={styles.tempMax}>{formatTemperature(day.temp_max, false)}°</Text>
        <View style={styles.tempBar}>
          <View
            style={[
              styles.tempBarFill,
              {
                width: `${((day.temp_max - day.temp_min) / 30) * 100}%`,
                opacity: 0.3,
              },
            ]}
          />
        </View>
        <Text style={styles.tempMin}>{formatTemperature(day.temp_min, false)}°</Text>
      </View>

      <View style={styles.conditionContainer}>
        <Text style={styles.conditionText} numberOfLines={1}>
          {translateWeatherCondition(day.condition)}
        </Text>
      </View>

      <View style={styles.extraInfo}>
        <View style={styles.infoItem}>
          <Text style={styles.infoIcon}>💧</Text>
          <Text style={styles.infoText}>{day.humidity}%</Text>
        </View>
        <View style={styles.infoItem}>
          <Text style={styles.infoIcon}>💨</Text>
          <Text style={styles.infoText}>{Math.round(day.wind_speed * 3.6)}km/h</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    marginHorizontal: theme.spacing.md,
    marginVertical: theme.spacing.xs,
    ...theme.shadows.sm,
  },
  dayContainer: {
    width: 60,
  },
  dayText: {
    fontSize: theme.fontSize.md,
    fontWeight: theme.fontWeight.medium,
    color: theme.colors.text,
  },
  icon: {
    width: 40,
    height: 40,
    marginHorizontal: theme.spacing.md,
  },
  temperatures: {
    flex: 1,
    alignItems: 'center',
    flexDirection: 'row',
    paddingHorizontal: theme.spacing.sm,
  },
  tempMax: {
    fontSize: theme.fontSize.md,
    fontWeight: theme.fontWeight.bold,
    color: theme.colors.text,
    marginRight: theme.spacing.sm,
  },
  tempMin: {
    fontSize: theme.fontSize.md,
    fontWeight: theme.fontWeight.regular,
    color: theme.colors.textLight,
    marginLeft: theme.spacing.sm,
  },
  tempBar: {
    width: 40,
    height: 4,
    backgroundColor: theme.colors.border,
    borderRadius: 2,
    overflow: 'hidden',
  },
  tempBarFill: {
    height: '100%',
    backgroundColor: theme.colors.primary,
  },
  conditionContainer: {
    width: 80,
    paddingHorizontal: theme.spacing.sm,
  },
  conditionText: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textLight,
    textTransform: 'capitalize',
  },
  extraInfo: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
  },
  infoItem: {
    alignItems: 'center',
  },
  infoIcon: {
    fontSize: 16,
  },
  infoText: {
    fontSize: theme.fontSize.xs,
    color: theme.colors.textLight,
    marginTop: 2,
  },
});

export default ForecastItem;
