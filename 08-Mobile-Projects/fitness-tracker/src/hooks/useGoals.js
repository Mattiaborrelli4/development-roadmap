import { useState, useEffect, useCallback } from 'react';
import workoutService from '../services/workoutService';
import { calculateProgress } from '../utils/calculations';
import { GOAL_TYPES, GOAL_PERIODS } from '../utils/constants';

export const useGoals = () => {
  const [goals, setGoals] = useState({
    daily: {},
    weekly: {}
  });
  const [progress, setProgress] = useState({
    daily: {},
    weekly: {}
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadGoals();
  }, []);

  const loadGoals = async () => {
    setLoading(true);
    try {
      const savedGoals = await workoutService.getGoals();
      setGoals(savedGoals);
    } catch (error) {
      console.error('Errore caricamento obiettivi:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateGoalProgress = useCallback(async (steps, calories, distance, duration) => {
    const dailyProgress = {};
    const weeklyProgress = {};

    // Calcola progresso giornaliero
    Object.entries(goals.daily).forEach(([key, target]) => {
      let current = 0;

      switch (key) {
        case GOAL_TYPES.STEPS:
          current = steps;
          break;
        case GOAL_TYPES.CALORIES:
          current = calories;
          break;
        case GOAL_TYPES.DISTANCE:
          current = distance;
          break;
        case GOAL_TYPES.DURATION:
          current = duration;
          break;
      }

      dailyProgress[key] = {
        target,
        current,
        percentage: calculateProgress(current, target),
        completed: current >= target
      };
    });

    // Calcola progresso settimanale (da implementare con dati storici)
    Object.entries(goals.weekly).forEach(([key, target]) => {
      weeklyProgress[key] = {
        target,
        current: 0, // Da calcolare con dati storici
        percentage: 0,
        completed: false
      };
    });

    setProgress({ daily: dailyProgress, weekly: weeklyProgress });
  }, [goals]);

  const updateGoal = useCallback(async (period, type, value) => {
    const success = await workoutService.updateGoal(period, type, value);
    if (success) {
      await loadGoals();
      return true;
    }
    return false;
  }, []);

  const resetGoals = useCallback(async () => {
    // Implementa reset ai valori di default
    await loadGoals();
  }, []);

  const getGoalStatus = useCallback((period, type) => {
    return progress[period][type] || { target: 0, current: 0, percentage: 0, completed: false };
  }, [progress]);

  const getCompletedGoals = useCallback((period) => {
    return Object.values(progress[period]).filter(g => g.completed);
  }, [progress]);

  const getTotalCompletion = useCallback((period) => {
    const goals = progress[period];
    const keys = Object.keys(goals);
    if (keys.length === 0) return 0;

    const totalPercentage = keys.reduce((sum, key) => sum + goals[key].percentage, 0);
    return Math.round(totalPercentage / keys.length);
  }, [progress]);

  return {
    goals,
    progress,
    loading,
    updateGoalProgress,
    updateGoal,
    resetGoals,
    getGoalStatus,
    getCompletedGoals,
    getTotalCompletion,
    loadGoals
  };
};
