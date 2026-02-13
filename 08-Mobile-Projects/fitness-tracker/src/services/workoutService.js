import AsyncStorage from '@react-native-async-storage/async-storage';
import { STORAGE_KEYS, DEFAULT_GOALS } from '../utils/constants';
import { format, startOfWeek, endOfWeek } from 'date-fns';

class WorkoutService {
  /**
   * Ottieni tutti gli allenamenti
   */
  async getWorkouts() {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.WORKOUTS);
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('Errore recupero allenamenti:', error);
      return [];
    }
  }

  /**
   * Salva un nuovo allenamento
   */
  async saveWorkout(workout) {
    try {
      const workouts = await this.getWorkouts();
      const newWorkout = {
        ...workout,
        id: workout.id || `workout_${Date.now()}`,
        date: workout.date || Date.now(),
        createdAt: Date.now()
      };

      workouts.push(newWorkout);
      await AsyncStorage.setItem(STORAGE_KEYS.WORKOUTS, JSON.stringify(workouts));

      // Aggiorna le statistiche giornaliere
      await this.updateDailyStats(newWorkout);

      return newWorkout;
    } catch (error) {
      console.error('Errore salvataggio allenamento:', error);
      return null;
    }
  }

  /**
   * Aggiorna un allenamento esistente
   */
  async updateWorkout(workoutId, updates) {
    try {
      const workouts = await this.getWorkouts();
      const index = workouts.findIndex(w => w.id === workoutId);

      if (index !== -1) {
        workouts[index] = { ...workouts[index], ...updates, updatedAt: Date.now() };
        await AsyncStorage.setItem(STORAGE_KEYS.WORKOUTS, JSON.stringify(workouts));
        return workouts[index];
      }

      return null;
    } catch (error) {
      console.error('Errore aggiornamento allenamento:', error);
      return null;
    }
  }

  /**
   * Elimina un allenamento
   */
  async deleteWorkout(workoutId) {
    try {
      const workouts = await this.getWorkouts();
      const filtered = workouts.filter(w => w.id !== workoutId);
      await AsyncStorage.setItem(STORAGE_KEYS.WORKOUTS, JSON.stringify(filtered));
      return true;
    } catch (error) {
      console.error('Errore eliminazione allenamento:', error);
      return false;
    }
  }

  /**
   * Ottieni gli allenamenti di oggi
   */
  async getTodayWorkouts() {
    try {
      const workouts = await this.getWorkouts();
      const today = format(new Date(), 'yyyy-MM-dd');

      return workouts.filter(w => {
        const workoutDate = format(new Date(w.date), 'yyyy-MM-dd');
        return workoutDate === today;
      });
    } catch (error) {
      console.error('Errore recupero allenamenti oggi:', error);
      return [];
    }
  }

  /**
   * Ottieni gli allenamenti della settimana corrente
   */
  async getWeekWorkouts() {
    try {
      const workouts = await this.getWorkouts();
      const now = new Date();
      const weekStart = startOfWeek(now, { weekStartsOn: 1 });
      const weekEnd = endOfWeek(now, { weekStartsOn: 1 });

      return workouts.filter(w => {
        const date = new Date(w.date);
        return date >= weekStart && date <= weekEnd;
      });
    } catch (error) {
      console.error('Errore recupero allenamenti settimana:', error);
      return [];
    }
  }

  /**
   * Ottieni gli obiettivi
   */
  async getGoals() {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.GOALS);
      if (data) {
        return JSON.parse(data);
      }
      return DEFAULT_GOALS;
    } catch (error) {
      console.error('Errore recupero obiettivi:', error);
      return DEFAULT_GOALS;
    }
  }

  /**
   * Salva gli obiettivi
   */
  async saveGoals(goals) {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.GOALS, JSON.stringify(goals));
      return true;
    } catch (error) {
      console.error('Errore salvataggio obiettivi:', error);
      return false;
    }
  }

  /**
   * Aggiorna un obiettivo
   */
  async updateGoal(period, type, value) {
    try {
      const goals = await this.getGoals();
      goals[period][type] = value;
      await this.saveGoals(goals);
      return true;
    } catch (error) {
      console.error('Errore aggiornamento obiettivo:', error);
      return false;
    }
  }

  /**
   * Aggiorna le statistiche giornaliere
   */
  async updateDailyStats(workout) {
    try {
      const stats = await this.getDailyStats();
      const today = format(new Date(), 'yyyy-MM-dd');

      if (!stats[today]) {
        stats[today] = {
          date: today,
          steps: 0,
          calories: 0,
          distance: 0,
          activeMinutes: 0
        };
      }

      stats[today].calories += workout.calories;
      stats[today].distance += workout.distance || 0;
      stats[today].activeMinutes += workout.duration;

      await AsyncStorage.setItem(STORAGE_KEYS.STATS, JSON.stringify(stats));
    } catch (error) {
      console.error('Errore aggiornamento statistiche:', error);
    }
  }

  /**
   * Ottieni le statistiche giornaliere
   */
  async getDailyStats() {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.STATS);
      return data ? JSON.parse(data) : {};
    } catch (error) {
      console.error('Errore recupero statistiche:', error);
      return {};
    }
  }

  /**
   * Ottieni le statistiche complessive
   */
  async getOverallStats() {
    try {
      const workouts = await this.getWorkouts();
      const stats = await this.getDailyStats();

      const totalWorkouts = workouts.length;
      const totalCalories = workouts.reduce((sum, w) => sum + w.calories, 0);
      const totalDistance = workouts.reduce((sum, w) => sum + (w.distance || 0), 0);
      const totalDuration = workouts.reduce((sum, w) => sum + w.duration, 0);

      // Trova il massimo di passi e calorie giornalieri
      const dailyValues = Object.values(stats);
      const maxDailySteps = Math.max(...dailyValues.map(d => d.steps), 0);
      const maxDailyCalories = Math.max(...dailyValues.map(d => d.calories), 0);

      // Calcola la distanza totale corsa
      const totalRunningDistance = workouts
        .filter(w => w.type === 'running')
        .reduce((sum, w) => sum + (w.distance || 0), 0);

      return {
        totalWorkouts,
        totalCalories,
        totalDistance: parseFloat(totalDistance.toFixed(2)),
        totalDuration,
        maxDailySteps,
        maxDailyCalories,
        totalRunningDistance: parseFloat(totalRunningDistance.toFixed(2)),
        avgCaloriesPerWorkout: totalWorkouts > 0 ? Math.round(totalCalories / totalWorkouts) : 0,
        avgDurationPerWorkout: totalWorkouts > 0 ? Math.round(totalDuration / totalWorkouts) : 0
      };
    } catch (error) {
      console.error('Errore recupero statistiche complessive:', error);
      return {};
    }
  }

  /**
   * Ottieni gli achievement sbloccati
   */
  async getAchievements() {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.ACHIEVEMENTS);
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('Errore recupero achievement:', error);
      return [];
    }
  }

  /**
   * Sblocca un achievement
   */
  async unlockAchievement(achievementId) {
    try {
      const achievements = await this.getAchievements();

      if (!achievements.includes(achievementId)) {
        achievements.push(achievementId);
        await AsyncStorage.setItem(
          STORAGE_KEYS.ACHIEVEMENTS,
          JSON.stringify(achievements)
        );
        return true;
      }

      return false;
    } catch (error) {
      console.error('Errore sblocco achievement:', error);
      return false;
    }
  }

  /**
   * Resetta tutti i dati (per testing)
   */
  async resetAllData() {
    try {
      await AsyncStorage.multiRemove([
        STORAGE_KEYS.WORKOUTS,
        STORAGE_KEYS.GOALS,
        STORAGE_KEYS.STEPS,
        STORAGE_KEYS.ACHIEVEMENTS,
        STORAGE_KEYS.STATS
      ]);
      return true;
    } catch (error) {
      console.error('Errore reset dati:', error);
      return false;
    }
  }
}

export default new WorkoutService();
