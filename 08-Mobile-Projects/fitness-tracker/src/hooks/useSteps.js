import { useState, useEffect } from 'react';
import { Animated } from 'react-native';
import sensorService from '../services/sensorService';
import { calculateCaloriesFromSteps, calculateDistanceFromSteps } from '../utils/calculations';

export const useSteps = () => {
  const [steps, setSteps] = useState(0);
  const [calories, setCalories] = useState(0);
  const [distance, setDistance] = useState(0);
  const [isAvailable, setIsAvailable] = useState(false);
  const [loading, setLoading] = useState(true);
  const [pulseAnimation] = useState(new Animated.Value(1));

  useEffect(() => {
    let mounted = true;

    const initializeSteps = async () => {
      setLoading(true);

      // Verifica disponibilità pedometro
      const available = await sensorService.isPedometerAvailable();
      if (mounted) {
        setIsAvailable(available);
      }

      // Ottieni passi iniziali
      const initialSteps = await sensorService.getTodaySteps();
      if (mounted) {
        setSteps(initialSteps);
        updateDerivedStats(initialSteps);
        setLoading(false);
      }

      // Sottoscrivi agli aggiornamenti
      await sensorService.subscribeToStepUpdates((newSteps) => {
        if (mounted) {
          setSteps(newSteps);
          updateDerivedStats(newSteps);
          triggerPulseAnimation();
        }
      });
    };

    initializeSteps();

    return () => {
      mounted = false;
      sensorService.unsubscribeFromStepUpdates();
    };
  }, []);

  const updateDerivedStats = (stepCount) => {
    setCalories(calculateCaloriesFromSteps(stepCount));
    setDistance(calculateDistanceFromSteps(stepCount));
  };

  const triggerPulseAnimation = () => {
    Animated.sequence([
      Animated.timing(pulseAnimation, {
        toValue: 1.1,
        duration: 100,
        useNativeDriver: true
      }),
      Animated.timing(pulseAnimation, {
        toValue: 1,
        duration: 100,
        useNativeDriver: true
      })
    ]).start();
  };

  const addManualSteps = async (additionalSteps) => {
    const newTotal = await sensorService.addManualSteps(additionalSteps);
    if (newTotal !== null) {
      setSteps(newTotal);
      updateDerivedStats(newTotal);
      return true;
    }
    return false;
  };

  return {
    steps,
    calories,
    distance,
    isAvailable,
    loading,
    pulseAnimation,
    addManualSteps,
    refreshSteps: async () => {
      const newSteps = await sensorService.getTodaySteps();
      setSteps(newSteps);
      updateDerivedStats(newSteps);
    }
  };
};
