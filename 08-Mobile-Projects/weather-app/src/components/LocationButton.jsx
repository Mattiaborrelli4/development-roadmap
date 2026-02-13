import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../styles/theme';

const LocationButton = ({ onPress, loading, disabled }) => {
  return (
    <TouchableOpacity
      style={[styles.container, disabled && styles.containerDisabled]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.8}
    >
      {loading ? (
        <ActivityIndicator color={theme.colors.textWhite} size="small" />
      ) : (
        <>
          <Ionicons name="location" size={24} color={theme.colors.textWhite} />
          <View style={styles.textContainer}>
            <Text style={styles.title}>Usa la mia posizione</Text>
            <Text style={styles.subtitle}>Ottieni il meteo della tua area</Text>
          </View>
          <Ionicons
            name="chevron-forward"
            size={20}
            color={theme.colors.textWhite}
          />
        </>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: theme.colors.primary,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    marginHorizontal: theme.spacing.md,
    marginVertical: theme.spacing.sm,
    ...theme.shadows.md,
  },
  containerDisabled: {
    opacity: 0.5,
  },
  textContainer: {
    flex: 1,
    marginLeft: theme.spacing.md,
    marginRight: theme.spacing.sm,
  },
  title: {
    fontSize: theme.fontSize.md,
    fontWeight: theme.fontWeight.semibold,
    color: theme.colors.textWhite,
  },
  subtitle: {
    fontSize: theme.fontSize.sm,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 2,
  },
});

export default LocationButton;
