import React from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import Svg, { Circle } from 'react-native-svg';
import { theme } from '../styles/theme';
import { formatDistance, formatDuration } from '../utils/calculations';

const StepCounter = ({ steps, calories, distance, goal = 10000, pulseAnimation }) => {
  const percentage = Math.min((steps / goal) * 100, 100);
  const radius = 80;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const getProgressColor = () => {
    if (percentage < 30) return theme.colors.danger;
    if (percentage < 70) return theme.colors.warning;
    return theme.colors.success;
  };

  return (
    <View style={styles.container}>
      <Animated.View style={[
        styles.circleContainer,
        { transform: [{ scale: pulseAnimation }] }
      ]}>
        <Svg width={200} height={200}>
          {/* Circle background */}
          <Circle
            cx="100"
            cy="100"
            r={radius}
            stroke={theme.colors.border}
            strokeWidth="12"
            fill="none"
          />
          {/* Progress circle */}
          <Circle
            cx="100"
            cy="100"
            r={radius}
            stroke={getProgressColor()}
            strokeWidth="12"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            rotation="-90"
            origin="100, 100"
          />
        </Svg>

        <View style={styles.textContainer}>
          <Text style={styles.stepsCount}>{steps.toLocaleString()}</Text>
          <Text style={styles.stepsLabel}>Passi</Text>
          <Text style={styles.percentage}>{percentage.toFixed(0)}%</Text>
        </View>
      </Animated.View>

      <View style={styles.statsContainer}>
        <View style={styles.statItem}>
          <Text style={styles.statIcon}>🔥</Text>
          <Text style={styles.statValue}>{calories}</Text>
          <Text style={styles.statLabel}>Cal</Text>
        </View>

        <View style={styles.statItem}>
          <Text style={styles.statIcon}>📍</Text>
          <Text style={styles.statValue}>{formatDistance(distance)}</Text>
          <Text style={styles.statLabel}>Distanza</Text>
        </View>

        <View style={styles.statItem}>
          <Text style={styles.statIcon}>⏱️</Text>
          <Text style={styles.statValue}>{Math.round(steps / 100)}</Text>
          <Text style={styles.statLabel}>Min attivi</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.lg,
    padding: theme.spacing.lg,
    alignItems: 'center',
    ...theme.shadows.md,
  },
  circleContainer: {
    position: 'relative',
    width: 200,
    height: 200,
    justifyContent: 'center',
    alignItems: 'center',
  },
  textContainer: {
    position: 'absolute',
    alignItems: 'center',
  },
  stepsCount: {
    fontSize: 36,
    fontWeight: 'bold',
    color: theme.colors.text,
  },
  stepsLabel: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textSecondary,
    marginTop: theme.spacing.xs,
  },
  percentage: {
    fontSize: theme.fontSize.lg,
    fontWeight: '600',
    color: theme.colors.primary,
    marginTop: theme.spacing.xs,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginTop: theme.spacing.lg,
    paddingTop: theme.spacing.lg,
    borderTopWidth: 1,
    borderTopColor: theme.colors.border,
  },
  statItem: {
    alignItems: 'center',
  },
  statIcon: {
    fontSize: 24,
    marginBottom: theme.spacing.xs,
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
});

export default StepCounter;
