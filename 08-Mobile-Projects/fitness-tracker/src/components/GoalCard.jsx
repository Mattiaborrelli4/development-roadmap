import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Animated } from 'react-native';
import { theme } from '../styles/theme';
import { calculateProgress } from '../utils/calculations';

const GoalCard = ({ goal, current, type, label, icon, onPress }) => {
  const progress = calculateProgress(current, goal);
  const [animatedValue] = React.useState(new Animated.Value(0));

  React.useEffect(() => {
    Animated.timing(animatedValue, {
      toValue: progress,
      duration: 1000,
      useNativeDriver: false,
    }).start();
  }, [progress]);

  const getColor = () => {
    if (progress >= 100) return theme.colors.success;
    if (progress >= 50) return theme.colors.primary;
    return theme.colors.warning;
  };

  const getIcon = () => {
    if (progress >= 100) return '✅';
    return icon;
  };

  return (
    <TouchableOpacity
      style={styles.container}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <View style={styles.header}>
        <Text style={styles.icon}>{getIcon()}</Text>
        <Text style={styles.label}>{label}</Text>
        <View style={styles.progressContainer}>
          <Text style={styles.progressText}>{progress}%</Text>
        </View>
      </View>

      <View style={styles.stats}>
        <View style={styles.stat}>
          <Text style={styles.statValue}>{current.toLocaleString()}</Text>
          <Text style={styles.statLabel}>Attuale</Text>
        </View>
        <View style={styles.divider} />
        <View style={styles.stat}>
          <Text style={styles.statValue}>{goal.toLocaleString()}</Text>
          <Text style={styles.statLabel}>Obiettivo</Text>
        </View>
      </View>

      <View style={styles.barContainer}>
        <View style={styles.barBackground}>
          <Animated.View
            style={[
              styles.barFill,
              {
                backgroundColor: getColor(),
                width: animatedValue.interpolate({
                  inputRange: [0, 100],
                  outputRange: ['0%', '100%']
                })
              }
            ]}
          />
        </View>
      </View>

      {progress >= 100 && (
        <View style={styles.completedBadge}>
          <Text style={styles.completedText}>Completato! 🎉</Text>
        </View>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    marginBottom: theme.spacing.sm,
    ...theme.shadows.sm,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  icon: {
    fontSize: 24,
    marginRight: theme.spacing.sm,
  },
  label: {
    flex: 1,
    fontSize: theme.fontSize.lg,
    fontWeight: '600',
    color: theme.colors.text,
  },
  progressContainer: {
    backgroundColor: theme.colors.background,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.sm,
  },
  progressText: {
    fontSize: theme.fontSize.md,
    fontWeight: 'bold',
    color: theme.colors.primary,
  },
  stats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: theme.spacing.sm,
  },
  stat: {
    alignItems: 'center',
    flex: 1,
  },
  statValue: {
    fontSize: theme.fontSize.xl,
    fontWeight: 'bold',
    color: theme.colors.text,
  },
  statLabel: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
    marginTop: theme.spacing.xs,
  },
  divider: {
    width: 1,
    backgroundColor: theme.colors.border,
    marginHorizontal: theme.spacing.md,
  },
  barContainer: {
    marginTop: theme.spacing.sm,
  },
  barBackground: {
    height: 8,
    backgroundColor: theme.colors.border,
    borderRadius: 4,
    overflow: 'hidden',
  },
  barFill: {
    height: '100%',
    borderRadius: 4,
  },
  completedBadge: {
    marginTop: theme.spacing.sm,
    backgroundColor: theme.colors.success,
    paddingVertical: theme.spacing.xs,
    paddingHorizontal: theme.spacing.sm,
    borderRadius: theme.borderRadius.sm,
    alignItems: 'center',
  },
  completedText: {
    color: theme.colors.surface,
    fontSize: theme.fontSize.sm,
    fontWeight: '600',
  },
});

export default GoalCard;
