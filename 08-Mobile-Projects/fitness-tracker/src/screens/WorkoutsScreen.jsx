import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Modal,
  SafeAreaView,
  Alert,
} from 'react-native';
import { useWorkouts } from '../hooks/useWorkouts';
import { theme } from '../styles/theme';
import WorkoutCard from '../components/WorkoutCard';
import { WORKOUT_TYPES, WORKOUT_LABELS } from '../utils/constants';
import { calculateCalories } from '../utils/calculations';

const WorkoutsScreen = () => {
  const { workouts, addWorkout, deleteWorkout } = useWorkouts();
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedType, setSelectedType] = useState(WORKOUT_TYPES.RUNNING);
  const [duration, setDuration] = useState('');
  const [distance, setDistance] = useState('');
  const [notes, setNotes] = useState('');

  const handleAddWorkout = async () => {
    const mins = parseInt(duration);
    const dist = parseFloat(distance);

    if (!mins || mins <= 0) {
      Alert.alert('Errore', 'Inserisci una durata valida');
      return;
    }

    const workoutData = {
      type: selectedType,
      duration: mins,
      distance: dist || 0,
      notes,
    };

    const result = await addWorkout(workoutData);

    if (result) {
      Alert.alert('Successo', 'Allenamento salvato!');
      resetForm();
    } else {
      Alert.alert('Errore', 'Impossibile salvare l\'allenamento');
    }
  };

  const resetForm = () => {
    setSelectedType(WORKOUT_TYPES.RUNNING);
    setDuration('');
    setDistance('');
    setNotes('');
    setModalVisible(false);
  };

  const handleDeleteWorkout = (workoutId) => {
    Alert.alert(
      'Elimina Allenamento',
      'Sei sicuro di voler eliminare questo allenamento?',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Elimina',
          style: 'destructive',
          onPress: async () => {
            await deleteWorkout(workoutId);
          }
        }
      ]
    );
  };

  const WorkoutTypeButton = ({ type, label, icon }) => (
    <TouchableOpacity
      style={[
        styles.typeButton,
        selectedType === type && styles.typeButtonSelected
      ]}
      onPress={() => setSelectedType(type)}
    >
      <Text style={styles.typeIcon}>{icon}</Text>
      <Text style={[
        styles.typeLabel,
        selectedType === type && styles.typeLabelSelected
      ]}>
        {label}
      </Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Allenamenti</Text>
        <Text style={styles.subtitle}>{workouts.length} totali</Text>
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {workouts.length > 0 ? (
          workouts.map((workout) => (
            <WorkoutCard
              key={workout.id}
              workout={workout}
              onPress={() => {}}
              onDelete={() => handleDeleteWorkout(workout.id)}
            />
          ))
        ) : (
          <View style={styles.emptyState}>
            <Text style={styles.emptyIcon}>💪</Text>
            <Text style={styles.emptyTitle}>Nessun Allenamento</Text>
            <Text style={styles.emptyText}>
              Aggiungi il tuo primo allenamento per iniziare a tracciare i progressi
            </Text>
            <TouchableOpacity
              style={styles.emptyButton}
              onPress={() => setModalVisible(true)}
            >
              <Text style={styles.emptyButtonText}>+ Aggiungi Allenamento</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>

      {/* Add Workout Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Nuovo Allenamento</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Text style={styles.closeButton}>✕</Text>
              </TouchableOpacity>
            </View>

            <ScrollView showsVerticalScrollIndicator={false}>
              {/* Workout Type Selection */}
              <Text style={styles.label}>Tipo di Allenamento</Text>
              <View style={styles.typeGrid}>
                {Object.entries(WORKOUT_TYPES).map(([key, type]) => (
                  <WorkoutTypeButton
                    key={type}
                    type={type}
                    label={WORKOUT_LABELS[type]}
                    icon={WORKOUT_LABELS[type] === 'Corsa' ? '🏃' :
                          WORKOUT_LABELS[type] === 'Ciclismo' ? '🚴' :
                          WORKOUT_LABELS[type] === 'Camminata' ? '🚶' :
                          WORKOUT_LABELS[type] === 'Palestra' ? '🏋️' :
                          WORKOUT_LABELS[type] === 'Nuoto' ? '🏊' :
                          WORKOUT_LABELS[type] === 'Yoga' ? '🧘' : '💪'}
                  />
                ))}
              </View>

              {/* Duration Input */}
              <Text style={styles.label}>Durata (minuti)</Text>
              <TextInput
                style={styles.input}
                value={duration}
                onChangeText={setDuration}
                placeholder="30"
                keyboardType="numeric"
                placeholderTextColor={theme.colors.textSecondary}
              />

              {/* Distance Input */}
              <Text style={styles.label}>Distanza (km) - opzionale</Text>
              <TextInput
                style={styles.input}
                value={distance}
                onChangeText={setDistance}
                placeholder="5.0"
                keyboardType="decimal-pad"
                placeholderTextColor={theme.colors.textSecondary}
              />

              {/* Notes Input */}
              <Text style={styles.label}>Note - opzionale</Text>
              <TextInput
                style={[styles.input, styles.textArea]}
                value={notes}
                onChangeText={setNotes}
                placeholder="Come è andato l'allenamento?"
                multiline
                numberOfLines={4}
                placeholderTextColor={theme.colors.textSecondary}
              />

              {/* Estimated Calories */}
              {duration && (
                <View style={styles.caloriesPreview}>
                  <Text style={styles.caloriesIcon}>🔥</Text>
                  <Text style={styles.caloriesText}>
                    Calorie stimate: {calculateCalories(selectedType, parseInt(duration) || 0)}
                  </Text>
                </View>
              )}
            </ScrollView>

            {/* Buttons */}
            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={[styles.modalButton, styles.cancelButton]}
                onPress={resetForm}
              >
                <Text style={styles.cancelButtonText}>Annulla</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalButton, styles.saveButton]}
                onPress={handleAddWorkout}
              >
                <Text style={styles.saveButtonText}>Salva</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      {/* Floating Action Button */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => setModalVisible(true)}
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
    padding: theme.spacing.lg,
    paddingTop: theme.spacing.lg,
  },
  title: {
    fontSize: theme.fontSize.xxl,
    fontWeight: 'bold',
    color: theme.colors.text,
  },
  subtitle: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textSecondary,
    marginTop: theme.spacing.xs,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.xl,
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: theme.spacing.lg,
  },
  emptyTitle: {
    fontSize: theme.fontSize.xl,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.sm,
  },
  emptyText: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    marginBottom: theme.spacing.xl,
  },
  emptyButton: {
    backgroundColor: theme.colors.primary,
    paddingHorizontal: theme.spacing.xl,
    paddingVertical: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
  },
  emptyButtonText: {
    color: theme.colors.surface,
    fontSize: theme.fontSize.md,
    fontWeight: '600',
  },
  modalContainer: {
    flex: 1,
    backgroundColor: theme.colors.overlay,
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: theme.colors.surface,
    borderTopLeftRadius: theme.borderRadius.xl,
    borderTopRightRadius: theme.borderRadius.xl,
    padding: theme.spacing.lg,
    maxHeight: '90%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
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
  label: {
    fontSize: theme.fontSize.md,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: theme.spacing.sm,
    marginTop: theme.spacing.md,
  },
  typeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -theme.spacing.xs,
  },
  typeButton: {
    width: '48%',
    marginHorizontal: '1%',
    marginBottom: theme.spacing.sm,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    backgroundColor: theme.colors.background,
    borderWidth: 2,
    borderColor: 'transparent',
    alignItems: 'center',
  },
  typeButtonSelected: {
    borderColor: theme.colors.primary,
    backgroundColor: `${theme.colors.primary}10`,
  },
  typeIcon: {
    fontSize: 32,
    marginBottom: theme.spacing.xs,
  },
  typeLabel: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
  },
  typeLabelSelected: {
    color: theme.colors.primary,
    fontWeight: '600',
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
  },
  textArea: {
    height: 100,
    textAlignVertical: 'top',
  },
  caloriesPreview: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${theme.colors.warning}20`,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.sm,
    marginTop: theme.spacing.md,
  },
  caloriesIcon: {
    fontSize: 24,
    marginRight: theme.spacing.sm,
  },
  caloriesText: {
    fontSize: theme.fontSize.md,
    fontWeight: '600',
    color: theme.colors.text,
  },
  modalButtons: {
    flexDirection: 'row',
    marginTop: theme.spacing.lg,
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

export default WorkoutsScreen;
