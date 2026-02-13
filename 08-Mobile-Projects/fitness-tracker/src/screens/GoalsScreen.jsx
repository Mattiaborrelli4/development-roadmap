import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
  TextInput,
  Modal,
  Alert,
} from 'react-native';
import { useGoals } from '../hooks/useGoals';
import { useSteps } from '../hooks/useSteps';
import { useWorkouts } from '../hooks/useWorkouts';
import { theme } from '../styles/theme';
import GoalCard from '../components/GoalCard';
import AchievementBadge from '../components/AchievementBadge';
import { ACHIEVEMENTS, GOAL_TYPES, GOAL_PERIODS } from '../utils/constants';
import workoutService from '../services/workoutService';
import { calculateStreak } from '../utils/calculations';

const GoalsScreen = () => {
  const { goals, updateGoal, getGoalStatus } = useGoals();
  const { steps, calories, distance } = useSteps();
  const { todayWorkouts, getTodaysStats } = useWorkouts();
  const [unlockedAchievements, setUnlockedAchievements] = useState([]);
  const [editModalVisible, setEditModalVisible] = useState(false);
  const [selectedGoal, setSelectedGoal] = useState(null);
  const [goalValue, setGoalValue] = useState('');
  const [streak, setStreak] = useState(0);

  React.useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const achievements = await workoutService.getAchievements();
    const workouts = await workoutService.getWorkouts();
    setUnlockedAchievements(achievements);
    setStreak(calculateStreak(workouts));
  };

  const todaysStats = getTodaysStats();
  const totalCalories = calories + todaysStats.calories;
  const totalDistance = distance + todaysStats.distance;
  const totalDuration = Math.round(steps / 100) + todaysStats.duration;

  const openEditModal = (period, type) => {
    setSelectedGoal({ period, type });
    setGoalValue(String(goals[period][type]));
    setEditModalVisible(true);
  };

  const handleUpdateGoal = async () => {
    const value = parseInt(goalValue);
    if (!value || value <= 0) {
      Alert.alert('Errore', 'Inserisci un valore valido');
      return;
    }

    const success = await updateGoal(selectedGoal.period, selectedGoal.type, value);
    if (success) {
      Alert.alert('Successo', 'Obiettivo aggiornato!');
      setEditModalVisible(false);
    } else {
      Alert.alert('Errore', 'Impossibile aggiornare l\'obiettivo');
    }
  };

  const renderGoalCard = (period, type, label, icon, current) => (
    <GoalCard
      key={`${period}-${type}`}
      goal={goals[period]?.[type] || 0}
      current={current}
      type={type}
      label={label}
      icon={icon}
      onPress={() => openEditModal(period, type)}
    />
  );

  const getGoalLabel = (type) => {
    switch (type) {
      case GOAL_TYPES.STEPS:
        return 'Passi';
      case GOAL_TYPES.CALORIES:
        return 'Calorie';
      case GOAL_TYPES.DISTANCE:
        return 'Distanza (km)';
      case GOAL_TYPES.DURATION:
        return 'Minuti Attivi';
      default:
        return type;
    }
  };

  const getGoalIcon = (type) => {
    switch (type) {
      case GOAL_TYPES.STEPS:
        return '👟';
      case GOAL_TYPES.CALORIES:
        return '🔥';
      case GOAL_TYPES.DISTANCE:
        return '📍';
      case GOAL_TYPES.DURATION:
        return '⏱️';
      default:
        return '🎯';
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Obiettivi</Text>
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Daily Goals Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Obiettivi Giornalieri</Text>
            <Text style={styles.sectionSubtitle}>Oggi</Text>
          </View>

          {renderGoalCard(
            GOAL_PERIODS.DAILY,
            GOAL_TYPES.STEPS,
            getGoalLabel(GOAL_TYPES.STEPS),
            getGoalIcon(GOAL_TYPES.STEPS),
            steps
          )}

          {renderGoalCard(
            GOAL_PERIODS.DAILY,
            GOAL_TYPES.CALORIES,
            getGoalLabel(GOAL_TYPES.CALORIES),
            getGoalIcon(GOAL_TYPES.CALORIES),
            totalCalories
          )}

          {renderGoalCard(
            GOAL_PERIODS.DAILY,
            GOAL_TYPES.DISTANCE,
            getGoalLabel(GOAL_TYPES.DISTANCE),
            getGoalIcon(GOAL_TYPES.DISTANCE),
            totalDistance
          )}

          {renderGoalCard(
            GOAL_PERIODS.DAILY,
            GOAL_TYPES.DURATION,
            getGoalLabel(GOAL_TYPES.DURATION),
            getGoalIcon(GOAL_TYPES.DURATION),
            totalDuration
          )}
        </View>

        {/* Weekly Goals Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Obiettivi Settimanali</Text>
            <Text style={styles.sectionSubtitle}>Questa settimana</Text>
          </View>

          {renderGoalCard(
            GOAL_PERIODS.WEEKLY,
            GOAL_TYPES.STEPS,
            getGoalLabel(GOAL_TYPES.STEPS),
            getGoalIcon(GOAL_TYPES.STEPS),
            0 // Implementare con dati storici
          )}

          {renderGoalCard(
            GOAL_PERIODS.WEEKLY,
            GOAL_TYPES.CALORIES,
            getGoalLabel(GOAL_TYPES.CALORIES),
            getGoalIcon(GOAL_TYPES.CALORIES),
            0 // Implementare con dati storici
          )}

          {renderGoalCard(
            GOAL_PERIODS.WEEKLY,
            GOAL_TYPES.DISTANCE,
            getGoalLabel(GOAL_TYPES.DISTANCE),
            getGoalIcon(GOAL_TYPES.DISTANCE),
            0 // Implementare con dati storici
          )}

          {renderGoalCard(
            GOAL_PERIODS.WEEKLY,
            GOAL_TYPES.DURATION,
            getGoalLabel(GOAL_TYPES.DURATION),
            getGoalIcon(GOAL_TYPES.DURATION),
            0 // Implementare con dati storici
          )}
        </View>

        {/* Achievements Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Achievement</Text>
            <Text style={styles.sectionSubtitle}>
              {unlockedAchievements.length} / {Object.values(ACHIEVEMENTS).length}
            </Text>
          </View>

          <View style={styles.achievementsGrid}>
            {Object.values(ACHIEVEMENTS).map((achievement) => (
              <AchievementBadge
                key={achievement.id}
                achievement={achievement}
                unlocked={unlockedAchievements.includes(achievement.id)}
                size="small"
                onPress={() => {
                  Alert.alert(
                    achievement.icon + ' ' + achievement.title,
                    achievement.description + '\n\nRequisito: ' + achievement.requirement,
                    [{ text: 'OK' }]
                  );
                }}
              />
            ))}
          </View>
        </View>

        {/* Streak Info */}
        {streak > 0 && (
          <View style={styles.streakContainer}>
            <Text style={styles.streakTitle}>Serie Attuale</Text>
            <View style={styles.streakRow}>
              <Text style={styles.streakIcon}>🔥</Text>
              <Text style={styles.streakValue}>{streak}</Text>
              <Text style={styles.streakLabel}>giorni consecutivi</Text>
            </View>
            <Text style={styles.streakAdvice}>
              Continua così! Mantieni la costanza per sbloccare nuovi achievement.
            </Text>
          </View>
        )}

        <View style={{ height: 80 }} />
      </ScrollView>

      {/* Edit Goal Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={editModalVisible}
        onRequestClose={() => setEditModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Modifica Obiettivo</Text>
              <TouchableOpacity onPress={() => setEditModalVisible(false)}>
                <Text style={styles.closeButton}>✕</Text>
              </TouchableOpacity>
            </View>

            {selectedGoal && (
              <>
                <Text style={styles.modalSubtitle}>
                  {getGoalLabel(selectedGoal.type)} - {selectedGoal.period === 'daily' ? 'Giornaliero' : 'Settimanale'}
                </Text>

                <Text style={styles.label}>Nuovo Obiettivo</Text>
                <TextInput
                  style={styles.input}
                  value={goalValue}
                  onChangeText={setGoalValue}
                  keyboardType="numeric"
                  placeholder="Inserisci valore..."
                  placeholderTextColor={theme.colors.textSecondary}
                />

                <View style={styles.modalButtons}>
                  <TouchableOpacity
                    style={[styles.modalButton, styles.cancelButton]}
                    onPress={() => setEditModalVisible(false)}
                  >
                    <Text style={styles.cancelButtonText}>Annulla</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={[styles.modalButton, styles.saveButton]}
                    onPress={handleUpdateGoal}
                  >
                    <Text style={styles.saveButtonText}>Salva</Text>
                  </TouchableOpacity>
                </View>
              </>
            )}
          </View>
        </View>
      </Modal>
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
  },
  sectionSubtitle: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textSecondary,
  },
  achievementsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -theme.spacing.xs,
  },
  streakContainer: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.lg,
    marginHorizontal: theme.spacing.lg,
    marginBottom: theme.spacing.md,
    ...theme.shadows.md,
  },
  streakTitle: {
    fontSize: theme.fontSize.lg,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  streakRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  streakIcon: {
    fontSize: 32,
    marginRight: theme.spacing.sm,
  },
  streakValue: {
    fontSize: theme.fontSize.xxxl,
    fontWeight: 'bold',
    color: theme.colors.warning,
    marginRight: theme.spacing.sm,
  },
  streakLabel: {
    fontSize: theme.fontSize.md,
    color: theme.colors.text,
  },
  streakAdvice: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
    fontStyle: 'italic',
  },
  modalContainer: {
    flex: 1,
    backgroundColor: theme.colors.overlay,
    justifyContent: 'center',
    padding: theme.spacing.lg,
  },
  modalContent: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.lg,
    padding: theme.spacing.lg,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
  modalTitle: {
    fontSize: theme.fontSize.xl,
    fontWeight: 'bold',
    color: theme.colors.text,
  },
  closeButton: {
    fontSize: 32,
    color: theme.colors.textSecondary,
  },
  modalSubtitle: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.lg,
  },
  label: {
    fontSize: theme.fontSize.md,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: theme.spacing.sm,
  },
  input: {
    backgroundColor: theme.colors.background,
    borderRadius: theme.borderRadius.sm,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    fontSize: theme.fontSize.md,
    color: theme.colors.text,
    borderWidth: 1,
    borderColor: theme.colors.border,
    marginBottom: theme.spacing.lg,
  },
  modalButtons: {
    flexDirection: 'row',
    gap: theme.spacing.md,
  },
  modalButton: {
    flex: 1,
    paddingVertical: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    alignItems: 'center',
  },
  cancelButton: {
    backgroundColor: theme.colors.background,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  cancelButtonText: {
    color: theme.colors.text,
    fontSize: theme.fontSize.md,
    fontWeight: '600',
  },
  saveButton: {
    backgroundColor: theme.colors.primary,
  },
  saveButtonText: {
    color: theme.colors.surface,
    fontSize: theme.fontSize.md,
    fontWeight: '600',
  },
});

export default GoalsScreen;
