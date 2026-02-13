import { Pedometer } from 'expo-sensors';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { STORAGE_KEYS } from '../utils/constants';
import { format, startOfDay, endOfDay } from 'date-fns';

class SensorService {
  constructor() {
    this.subscription = null;
    this.isAvailable = false;
    this.currentSteps = 0;
  }

  /**
   * Verifica se il pedometro è disponibile
   */
  async isPedometerAvailable() {
    try {
      const result = await Pedometer.isAvailableAsync();
      this.isAvailable = result;
      return result;
    } catch (error) {
      console.error('Errore verifica pedometro:', error);
      return false;
    }
  }

  /**
   * Ottiene i passi del giorno corrente
   */
  async getTodaySteps() {
    try {
      if (!this.isAvailable) {
        await this.isPedometerAvailable();
      }

      if (!this.isAvailable) {
        // Fallback: recupera dai dati salvati
        return this.getStoredSteps();
      }

      const start = startOfDay(new Date());
      const end = endOfDay(new Date());

      const result = await Pedometer.getStepCountAsync(start, end);
      this.currentSteps = result.steps;

      // Salva i passi correnti
      await this.saveSteps(result.steps);

      return result.steps;
    } catch (error) {
      console.error('Errore ottenimento passi:', error);
      return this.getStoredSteps();
    }
  }

  /**
   * Ottiene i passi per un periodo specifico
   */
  async getStepsForPeriod(startDate, endDate) {
    try {
      if (!this.isAvailable) {
        return null;
      }

      const result = await Pedometer.getStepCountAsync(startDate, endDate);
      return result.steps;
    } catch (error) {
      console.error('Errore ottenimento passi periodo:', error);
      return null;
    }
  }

  /**
   * Sottoscrivi agli aggiornamenti dei passi
   */
  async subscribeToStepUpdates(callback) {
    try {
      if (!this.isAvailable) {
        await this.isPedometerAvailable();
      }

      if (!this.isAvailable) {
        console.log('Pedometro non disponibile');
        return;
      }

      this.subscription = await Pedometer.watchStepCountAsync((result) => {
        this.currentSteps = result.steps;
        callback(result.steps);
      });

    } catch (error) {
      console.error('Errore sottoscrizione passi:', error);
    }
  }

  /**
   * Annulla la sottoscrizione agli aggiornamenti
   */
  unsubscribeFromStepUpdates() {
    if (this.subscription) {
      this.subscription.remove();
      this.subscription = null;
    }
  }

  /**
   * Salva i passi nello storage
   */
  async saveSteps(steps) {
    try {
      const today = format(new Date(), 'yyyy-MM-dd');
      const data = {
        date: today,
        steps: steps,
        timestamp: Date.now()
      };

      await AsyncStorage.setItem(STORAGE_KEYS.STEPS, JSON.stringify(data));
    } catch (error) {
      console.error('Errore salvataggio passi:', error);
    }
  }

  /**
   * Recupera i passi salvati
   */
  async getStoredSteps() {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.STEPS);
      if (data) {
        const parsed = JSON.parse(data);
        const today = format(new Date(), 'yyyy-MM-dd');

        // Verifica se i dati sono di oggi
        if (parsed.date === today) {
          return parsed.steps;
        }
      }
      return 0;
    } catch (error) {
      console.error('Errore recupero passi salvati:', error);
      return 0;
    }
  }

  /**
   * Aggiunge manualmente i passi (quando il sensore non è disponibile)
   */
  async addManualSteps(steps) {
    try {
      const currentSteps = await this.getStoredSteps();
      const newSteps = currentSteps + steps;
      await this.saveSteps(newSteps);
      return newSteps;
    } catch (error) {
      console.error('Errore aggiunta manuale passi:', error);
      return null;
    }
  }

  /**
   * Resetta i passi del giorno (per testing)
   */
  async resetSteps() {
    try {
      await this.saveSteps(0);
      this.currentSteps = 0;
    } catch (error) {
      console.error('Errore reset passi:', error);
    }
  }

  /**
   * Pulisce le risorse
   */
  cleanup() {
    this.unsubscribeFromStepUpdates();
  }
}

export default new SensorService();
