import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { useWorkouts } from '../hooks/useWorkouts';
import { useSteps } from '../hooks/useSteps';
import { theme } from '../styles/theme';
import ProgressChart from '../components/ProgressChart';
import { getWeeklyStats, formatDistance, formatDuration } from '../utils/calculations';
import { format } from 'date-fns';
import { it } from 'date-fns/locale';

const ProgressScreen = () => {
  const { workouts, weekWorkouts } = useWorkouts();
  const { steps } = useSteps();
  const [timeRange, setTimeRange] = useState('week'); // 'week' or 'month'
  const [weeklyStats, setWeeklyStats] = useState(null);

  useEffect(() => {
    loadWeeklyStats();
  }, [workouts, steps]);

  const loadWeeklyStats = () => {
    const stats = getWeeklyStats(workouts, steps);
    setWeeklyStats(stats);
  };

  const getWeekChartData = () => {
    if (!weeklyStats) return [];

    return weeklyStats.daily.map(day => ({
      label: day.date,
      value: day.steps || 0
    }));
  };

  const getCaloriesChartData = () => {
    if (!weeklyStats) return [];

    return weeklyStats.daily.map(day => ({
      label: day.date,
      value: day.calories || 0
    }));
  };

  const getWorkoutDistributionData = () => {
    if (!weeklyStats || !weeklyStats.workoutByType) return [];

    return Object.entries(weeklyStats.workoutByType).map(([type, count]) => ({
      x: type,
      y: count
    }));
  };

  const StatCard = ({ title, value, unit, icon, color }) => (
    <View style={[styles.statCard, { borderLeftColor: color }]}>
      <Text style={styles.statIcon}>{icon}</Text>
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statTitle}>{title}</Text>
      {unit && <Text style={styles.statUnit}>{unit}</Text>}
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Progressi</Text>

        <View style={styles.timeRangeSelector}>
          <TouchableOpacity
            style={[
              styles.timeRangeButton,
              timeRange === 'week' && styles.timeRangeButtonActive
            ]}
            onPress={() => setTimeRange('week')}
          >
            <Text style={[
              styles.timeRangeText,
              timeRange === 'week' && styles.timeRangeTextActive
            ]}>
              Settimana
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.timeRangeButton,
              timeRange === 'month' && styles.timeRangeButtonActive
            ]}
            onPress={() => setTimeRange('month')}
          >
            <Text style={[
              styles.timeRangeText,
              timeRange === 'month' && styles.timeRangeTextActive
            ]}>
              Mese
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Weekly Summary Stats */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Riepilogo Settimanale</Text>

          <View style={styles.statsGrid}>
            <StatCard
              title="Allenamenti"
              value={weeklyStats?.workouts || 0}
              icon="💪"
              color={theme.colors.primary}
            />

            <StatCard
              title="Passi"
              value={(weeklyStats?.steps || 0).toLocaleString()}
              icon="👟"
              color={theme.colors.secondary}
            />

            <StatCard
              title="Calorie"
              value={weeklyStats?.calories || 0}
              unit="kcal"
              icon="🔥"
              color={theme.colors.accent}
            />

            <StatCard
              title="Distanza"
              value={formatDistance(weeklyStats?.distance || 0)}
              icon="📍"
              color={theme.colors.success}
            />

            <StatCard
              title="Durata"
              value={formatDuration(weeklyStats?.duration || 0)}
              icon="⏱️"
              color={theme.colors.warning}
            />
          </View>
        </View>

        {/* Weekly Steps Chart */}
        <ProgressChart
          type="bar"
          title="Passi Giornalieri"
          data={getWeekChartData()}
        />

        {/* Weekly Calories Chart */}
        <ProgressChart
          type="line"
          title="Calorie Giornaliere"
          data={getCaloriesChartData()}
        />

        {/* Workout Distribution */}
        {getWorkoutDistributionData().length > 0 && (
          <ProgressChart
            type="pie"
            title="Distribuzione Allenamenti"
            data={getWorkoutDistributionData()}
          />
        )}

        {/* Recent Workouts Summary */}
        {weekWorkouts.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Allenamenti della Settimana</Text>

            {weekWorkouts.slice(0, 5).map((workout) => (
              <View key={workout.id} style={styles.workoutSummary}>
                <View style={styles.workoutSummaryLeft}>
                  <Text style={styles.workoutSummaryTitle}>
                    {workout.type === 'running' ? '🏃 Corsa' :
                     workout.type === 'cycling' ? '🚴 Ciclismo' :
                     workout.type === 'walking' ? '🚶 Camminata' :
                     workout.type === 'gym' ? '🏋️ Palestra' :
                     workout.type === 'swimming' ? '🏊 Nuoto' :
                     workout.type === 'yoga' ? '🧘 Yoga' : '💪 Altro'}
                  </Text>
                  <Text style={styles.workoutSummaryDate}>
                    {format(new Date(workout.date), 'dd MMM HH:mm', { locale: it })}
                  </Text>
                </View>
                <View style={styles.workoutSummaryRight}>
                  <Text style={styles.workoutSummaryCalories}>
                    {workout.calories} kcal
                  </Text>
                  <Text style={styles.workoutSummaryDuration}>
                    {workout.duration} min
                  </Text>
                </View>
              </View>
            ))}
          </View>
        )}

        <View style={{ height: 80 }} />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    padding: theme.spacing.lg,
    paddingTop: theme.spacing.lg,
  },
  title: {
    fontSize: theme.fontSize.xxl,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  timeRangeSelector: {
    flexDirection: 'row',
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.xs,
    ...theme.shadows.sm,
  },
  timeRangeButton: {
    flex: 1,
    paddingVertical: theme.spacing.sm,
    paddingHorizontal: theme.spacing.md,
    borderRadius: theme.borderRadius.sm,
    alignItems: 'center',
  },
  timeRangeButtonActive: {
    backgroundColor: theme.colors.primary,
  },
  timeRangeText: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textSecondary,
    fontWeight: '600',
  },
  timeRangeTextActive: {
    color: theme.colors.surface,
  },
  section: {
    padding: theme.spacing.lg,
  },
  sectionTitle: {
    fontSize: theme.fontSize.xl,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -theme.spacing.xs,
  },
  statCard: {
    width: '48%',
    marginHorizontal: '1%',
    marginBottom: theme.spacing.md,
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    borderLeftWidth: 4,
    ...theme.shadows.sm,
  },
  statIcon: {
    fontSize: 32,
    marginBottom: theme.spacing.xs,
  },
  statValue: {
    fontSize: theme.fontSize.xl,
    fontWeight: 'bold',
    color: theme.colors.text,
  },
  statTitle: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
    marginTop: theme.spacing.xs,
  },
  statUnit: {
    fontSize: theme.fontSize.xs,
    color: theme.colors.textSecondary,
  },
  workoutSummary: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    marginBottom: theme.spacing.sm,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    ...theme.shadows.sm,
  },
  workoutSummaryLeft: {
    flex: 1,
  },
  workoutSummaryTitle: {
    fontSize: theme.fontSize.md,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: theme.spacing.xs,
  },
  workoutSummaryDate: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
  },
  workoutSummaryRight: {
    alignItems: 'flex-end',
  },
  workoutSummaryCalories: {
    fontSize: theme.fontSize.md,
    fontWeight: 'bold',
    color: theme.colors.primary,
  },
  workoutSummaryDuration: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
  },
});

export default ProgressScreen;
