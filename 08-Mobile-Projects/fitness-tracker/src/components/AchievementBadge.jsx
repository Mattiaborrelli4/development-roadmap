import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { theme } from '../styles/theme';

const AchievementBadge = ({ achievement, unlocked, size = 'large', onPress }) => {
  const isSmall = size === 'small';

  return (
    <TouchableOpacity
      style={[
        styles.container,
        isSmall && styles.containerSmall,
        !unlocked && styles.locked
      ]}
      onPress={() => unlocked && onPress && onPress(achievement)}
      disabled={!unlocked}
      activeOpacity={unlocked ? 0.7 : 1}
    >
      <View style={[
        styles.iconContainer,
        isSmall && styles.iconContainerSmall,
        unlocked && styles.iconContainerUnlocked
      ]}>
        <Text style={[styles.icon, isSmall && styles.iconSmall]}>
          {unlocked ? achievement.icon : '🔒'}
        </Text>
      </View>

      {!isSmall && (
        <>
          <Text style={styles.title}>{achievement.title}</Text>
          <Text style={styles.description}>{achievement.description}</Text>
          {unlocked && (
            <View style={styles.unlockedBadge}>
              <Text style={styles.unlockedText}>Sbloccato</Text>
            </View>
          )}
        </>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    alignItems: 'center',
    width: 150,
    ...theme.shadows.sm,
  },
  containerSmall: {
    width: 80,
    padding: theme.spacing.sm,
  },
  locked: {
    opacity: 0.5,
  },
  iconContainer: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: theme.colors.background,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  iconContainerSmall: {
    width: 50,
    height: 50,
    borderRadius: 25,
    marginBottom: theme.spacing.xs,
  },
  iconContainerUnlocked: {
    backgroundColor: `${theme.colors.primary}20`,
    borderWidth: 2,
    borderColor: theme.colors.primary,
  },
  icon: {
    fontSize: 36,
  },
  iconSmall: {
    fontSize: 24,
  },
  title: {
    fontSize: theme.fontSize.md,
    fontWeight: '600',
    color: theme.colors.text,
    textAlign: 'center',
    marginBottom: theme.spacing.xs,
  },
  description: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    marginBottom: theme.spacing.sm,
  },
  unlockedBadge: {
    backgroundColor: theme.colors.success,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.sm,
  },
  unlockedText: {
    color: theme.colors.surface,
    fontSize: theme.fontSize.xs,
    fontWeight: '600',
  },
});

export default AchievementBadge;
