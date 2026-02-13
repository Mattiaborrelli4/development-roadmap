import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
  Alert,
} from 'react-native';
import { useSteps } from '../hooks/useSteps';
import { useWorkouts } from '../hooks/useWorkouts';
import { useGoals } from '../hooks/useGoals';
import { theme } from '../styles/theme';
import StepCounter from '../components/StepCounter';
import WorkoutCard from '../components/WorkoutCard';
import GoalCard from '../components/GoalCard';
import AchievementBadge from '../components/AchievementBadge';
import { ACHIEVEMENTS, GOAL_TYPES } from '../utils/constants';
import workoutService from '../services/workoutService';
import { calculateStreak } from '../utils/calculations';
import { format } from 'date-fns';
import { it } from 'date-fns/locale';

const DashboardScreen = ({ navigation }) => {
  const { steps, calories, distance, isAvailable, loading: stepsLoading, pulseAnimation } = useSteps();
  const { todayWorkouts, getTodaysStats } = useWorkouts();
  const { goals, updateGoalProgress, getGoalStatus } = useGoals();
  const [unlockedAchievements, setUnlockedAchievements] = useState([]);
  const [streak, setStreak] = useState(0);

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    // Aggiorna il progresso degli obiettivi quando i passi cambiano
    updateGoalProgress(
      steps,
      calories + getTodaysStats().calories,
      distance + getTodaysStats().distance,
      Math.round(steps / 100) + getTodaysStats().duration
    );
  }, [steps, calories, distance, todayWorkouts]);

  const loadData = async () => {
    try {
      // Carica achievement sbloccati
      const achievements = await workoutService.getAchievements();
      setUnlockedAchievements(achievements);

      // Calcola streak
      const workouts = await workoutService.getWorkouts();
      setStreak(calculateStreak(workouts));

      // Verifica nuovi achievement
      await checkAchievements(workouts);
    } catch (error) {
      console.error('Errore caricamento dati:', error);
    }
  };

  const checkAchievements = async (workouts) => {
    const stats = await workoutService.getOverallStats();
    stats.currentStreak = streak;

    const newUnlocks = [];

    Object.values(ACHIEVEMENTS).forEach(achievement => {
      if (!unlockedAchievements.includes(achievement.id)) {
        const isUnlocked = stats.totalWorkouts >= achievement.requirement ||
          stats.maxDailySteps >= achievement.requirement ||
          stats.maxDailyCalories >= achievement.requirement ||
          streak >= achievement.requirement ||
          stats.totalRunningDistance >= achievement.requirement;

        if (isUnlocked) {
          newUnlocks.push(achievement);
        }
      }
    });

    // Sblocca nuovi achievement
    for (const achievement of newUnlocks) {
      await workoutService.unlockAchievement(achievement.id);
      Alert.alert(
        '🎉 Nuovo Achievement!',
        `Hai sbloccato: ${achievement.icon} ${achievement.title}`
      );
    }

    if (newUnlocks.length > 0) {
      const achievements = await workoutService.getAchievements();
      setUnlockedAchievements(achievements);
    }
  };

  const todaysStats = getTodaysStats();
  const totalCalories = calories + todaysStats.calories;
  const totalDistance = distance + todaysStats.distance;
  const totalDuration = Math.round(steps / 100) + todaysStats.duration;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>
              👋 {format(new Date(), 'EEEE', { locale: it })}
            </Text>
            <Text style={styles.title}>Dashboard</Text>
          </View>
          <TouchableOpacity
            style={styles.settingsButton}
            onPress={() => navigation.navigate('Settings')}
          >
            <Text style={styles.settingsIcon}>⚙️</Text>
          </TouchableOpacity>
        </View>

        {/* Step Counter */}
        <StepCounter
          steps={steps}
          calories={calories}
          distance={distance}
          goal={goals.daily?.steps || 10000}
          pulseAnimation={pulseAnimation}
        />

        {/* Daily Goals */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Obiettivi Giornalieri</Text>

          <GoalCard
            goal={goals.daily?.calories || 500}
            current={totalCalories}
            type={GOAL_TYPES.CALORIES}
            label="Calorie"
            icon="🔥"
          />

          <GoalCard
            goal={goals.daily?.distance || 5}
            current={totalDistance}
            type={GOAL_TYPES.DISTANCE}
            label="Distanza (km)"
            icon="📍"
          />

          <GoalCard
            goal={goals.daily?.duration || 30}
            current={totalDuration}
            type={GOAL_TYPES.DURATION}
            label="Minuti Attivi"
            icon="⏱️"
          />
        </View>

        {/* Today's Workouts */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Allenamenti di Oggi</Text>
            {todayWorkouts.length > 0 && (
              <Text style={styles.workoutCount}>{todayWorkouts.length}</Text>
            )}
          </View>

          {todayWorkouts.length > 0 ? (
            todayWorkouts.map((workout) => (
              <WorkoutCard
                key={workout.id}
                workout={workout}
                onPress={() => navigation.navigate('WorkoutDetail', { workout })}
              />
            ))
          ) : (
            <View style={styles.emptyState}>
              <Text style={styles.emptyText}>Nessun allenamento oggi</Text>
              <TouchableOpacity
                style={styles.addButton}
                onPress={() => navigation.navigate('AddWorkout')}
              >
                <Text style={styles.addButtonText}>+ Aggiungi Allenamento</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>

        {/* Recent Achievements */}
        {unlockedAchievements.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Achievement Recenti</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {unlockedAchievements.slice(-5).map((id) => {
                const achievement = Object.values(ACHIEVEMENTS).find(a => a.id === id);
                return achievement ? (
                  <AchievementBadge
                    key={achievement.id}
                    achievement={achievement}
                    unlocked={true}
                    size="small"
                    onPress={() => {}}
                  />
                ) : null;
              })}
            </ScrollView>
          </View>
        )}

        {/* Streak */}
        {streak > 0 && (
          <View style={styles.streakContainer}>
            <Text style={styles.streakIcon}>🔥</Text>
            <Text style={styles.streakText}>{streak} giorni consecutivi</Text>
          </View>
        )}

        <View style={{ height: 80 }} />
      </ScrollView>

      {/* Floating Action Button */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => navigation.navigate('AddWorkout')}
      >
        <Text style={styles.fabIcon}>+</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: theme.spacing.lg,
  },
  greeting: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textSecondary,
  },
  title: {
    fontSize: theme.fontSize.xxl,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginTop: theme.spacing.xs,
  },
  settingsButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: theme.colors.surface,
    justifyContent: 'center',
    alignItems: 'center',
    ...theme.shadows.sm,
  },
  settingsIcon: {
    fontSize: 24,
  },
  section: {
    padding: theme.spacing.lg,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
  sectionTitle: {
    fontSize: theme.fontSize.xl,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  workoutCount: {
    backgroundColor: theme.colors.primary,
    color: theme.colors.surface,
    fontSize: theme.fontSize.sm,
    fontWeight: 'bold',
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.round,
  },
  emptyState: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.xl,
    alignItems: 'center',
    ...theme.shadows.sm,
  },
  emptyText: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.md,
  },
  addButton: {
    backgroundColor: theme.colors.primary,
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
  },
  addButtonText: {
    color: theme.colors.surface,
    fontSize: theme.fontSize.md,
    fontWeight: '600',
  },
  streakContainer: {
    flexDirection: 'row',
    backgroundColor: `${theme.colors.warning}20`,
    marginHorizontal: theme.spacing.lg,
    marginBottom: theme.spacing.md,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  streakIcon: {
    fontSize: 24,
    marginRight: theme.spacing.sm,
  },
  streakText: {
    fontSize: theme.fontSize.lg,
    fontWeight: '600',
    color: theme.colors.text,
  },
  fab: {
    position: 'absolute',
    bottom: 24,
    right: 24,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: theme.colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    ...theme.shadows.lg,
  },
  fabIcon: {
    fontSize: 32,
    color: theme.colors.surface,
    fontWeight: 'bold',
  },
});

export default DashboardScreen;
