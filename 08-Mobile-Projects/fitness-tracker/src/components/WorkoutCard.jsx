import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { format } from 'date-fns';
import { it } from 'date-fns/locale';
import { theme } from '../styles/theme';
import { WORKOUT_ICONS, WORKOUT_LABELS } from '../utils/constants';
import { formatDuration, formatDistance } from '../utils/calculations';

const WorkoutCard = ({ workout, onPress, onDelete }) => {
  const workoutDate = new Date(workout.date);
  const isToday = format(new Date(), 'yyyy-MM-dd') === format(workoutDate, 'yyyy-MM-dd');

  const getDateLabel = () => {
    if (isToday) return 'Oggi';

    const now = new Date();
    const diffDays = Math.floor((now - workoutDate) / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return 'Ieri';
    if (diffDays < 7) return format(workoutDate, 'EEEE', { locale: it });

    return format(workoutDate, 'dd MMM', { locale: it });
  };

  return (
    <TouchableOpacity
      style={styles.container}
      onPress={() => onPress && onPress(workout)}
      activeOpacity={0.7}
    >
      <View style={styles.header}>
        <View style={styles.iconContainer}>
          <Text style={styles.icon}>
            {WORKOUT_ICONS[workout.type] || WORKOUT_ICONS.other}
          </Text>
        </View>

        <View style={styles.info}>
          <Text style={styles.type}>{WORKOUT_LABELS[workout.type] || workout.type}</Text>
          <Text style={styles.date}>{getDateLabel()}</Text>
        </View>

        <View style={styles.metrics}>
          <View style={styles.metric}>
            <Text style={styles.metricValue}>{workout.calories}</Text>
            <Text style={styles.metricLabel}>cal</Text>
          </View>
        </View>
      </View>

      <View style={styles.details}>
        <View style={styles.detailItem}>
          <Text style={styles.detailIcon}>⏱️</Text>
          <Text style={styles.detailText}>{formatDuration(workout.duration)}</Text>
        </View>

        {workout.distance > 0 && (
          <View style={styles.detailItem}>
            <Text style={styles.detailIcon}>📍</Text>
            <Text style={styles.detailText}>{formatDistance(workout.distance)}</Text>
          </View>
        )}

        {workout.notes && (
          <View style={[styles.detailItem, styles.notesItem]}>
            <Text style={styles.detailIcon}>📝</Text>
            <Text style={styles.notesText} numberOfLines={1}>
              {workout.notes}
            </Text>
          </View>
        )}
      </View>
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
  },
  iconContainer: {
    width: 50,
    height: 50,
    borderRadius: theme.borderRadius.md,
    backgroundColor: theme.colors.background,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: theme.spacing.md,
  },
  icon: {
    fontSize: 28,
  },
  info: {
    flex: 1,
  },
  type: {
    fontSize: theme.fontSize.lg,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: theme.spacing.xs,
  },
  date: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
  },
  metrics: {
    alignItems: 'flex-end',
  },
  metric: {
    alignItems: 'center',
  },
  metricValue: {
    fontSize: theme.fontSize.xl,
    fontWeight: 'bold',
    color: theme.colors.primary,
  },
  metricLabel: {
    fontSize: theme.fontSize.xs,
    color: theme.colors.textSecondary,
  },
  details: {
    flexDirection: 'row',
    marginTop: theme.spacing.sm,
    paddingTop: theme.spacing.sm,
    borderTopWidth: 1,
    borderTopColor: theme.colors.border,
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: theme.spacing.lg,
  },
  detailIcon: {
    fontSize: 16,
    marginRight: theme.spacing.xs,
  },
  detailText: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
  },
  notesItem: {
    flex: 1,
  },
  notesText: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
    flex: 1,
  },
});

export default WorkoutCard;
