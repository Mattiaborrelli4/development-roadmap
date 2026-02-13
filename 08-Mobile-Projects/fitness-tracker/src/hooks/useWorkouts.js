import { useState, useEffect, useCallback } from 'react';
import workoutService from '../services/workoutService';
import { calculateCalories } from '../utils/calculations';

export const useWorkouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [todayWorkouts, setTodayWorkouts] = useState([]);
  const [weekWorkouts, setWeekWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadWorkouts();
  }, []);

  const loadWorkouts = async () => {
    setLoading(true);
    try {
      const all = await workoutService.getWorkouts();
      const today = await workoutService.getTodayWorkouts();
      const week = await workoutService.getWeekWorkouts();

      setWorkouts(all.sort((a, b) => b.date - a.date));
      setTodayWorkouts(today);
      setWeekWorkouts(week);
    } catch (error) {
      console.error('Errore caricamento allenamenti:', error);
    } finally {
      setLoading(false);
    }
  };

  const addWorkout = useCallback(async (workoutData) => {
    try {
      // Calcola calories se non fornite
      const calories = workoutData.calories || calculateCalories(
        workoutData.type,
        workoutData.duration
      );

      const newWorkout = {
        type: workoutData.type,
        duration: workoutData.duration,
        calories,
        distance: workoutData.distance || 0,
        notes: workoutData.notes || '',
        date: workoutData.date || Date.now()
      };

      const saved = await workoutService.saveWorkout(newWorkout);

      if (saved) {
        await loadWorkouts();
        return saved;
      }

      return null;
    } catch (error) {
      console.error('Errore aggiunta allenamento:', error);
      return null;
    }
  }, []);

  const updateWorkout = useCallback(async (workoutId, updates) => {
    const updated = await workoutService.updateWorkout(workoutId, updates);
    if (updated) {
      await loadWorkouts();
      return true;
    }
    return false;
  }, []);

  const deleteWorkout = useCallback(async (workoutId) => {
    const success = await workoutService.deleteWorkout(workoutId);
    if (success) {
      await loadWorkouts();
      return true;
    }
    return false;
  }, []);

  const getWorkoutsByType = useCallback((type) => {
    return workouts.filter(w => w.type === type);
  }, [workouts]);

  const getTotalCalories = useCallback(() => {
    return workouts.reduce((sum, w) => sum + w.calories, 0);
  }, [workouts]);

  const getTotalDuration = useCallback(() => {
    return workouts.reduce((sum, w) => sum + w.duration, 0);
  }, [workouts]);

  const getTotalDistance = useCallback(() => {
    return workouts.reduce((sum, w) => sum + (w.distance || 0), 0);
  }, [workouts]);

  const getTodaysStats = useCallback(() => {
    return {
      count: todayWorkouts.length,
      calories: todayWorkouts.reduce((sum, w) => sum + w.calories, 0),
      duration: todayWorkouts.reduce((sum, w) => sum + w.duration, 0),
      distance: todayWorkouts.reduce((sum, w) => sum + (w.distance || 0), 0)
    };
  }, [todayWorkouts]);

  const getWeekStats = useCallback(() => {
    return {
      count: weekWorkouts.length,
      calories: weekWorkouts.reduce((sum, w) => sum + w.calories, 0),
      duration: weekWorkouts.reduce((sum, w) => sum + w.duration, 0),
      distance: weekWorkouts.reduce((sum, w) => sum + (w.distance || 0), 0)
    };
  }, [weekWorkouts]);

  return {
    workouts,
    todayWorkouts,
    weekWorkouts,
    loading,
    addWorkout,
    updateWorkout,
    deleteWorkout,
    loadWorkouts,
    getWorkoutsByType,
    getTotalCalories,
    getTotalDuration,
    getTotalDistance,
    getTodaysStats,
    getWeekStats
  };
};
