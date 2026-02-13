import { format, startOfWeek, endOfWeek, eachDayOfInterval, isSameDay } from 'date-fns';
import { it } from 'date-fns/locale';

/**
 * Calcola le calorie bruciate in base all'attività
 * @param {string} type - Tipo di allenamento
 * @param {number} duration - Durata in minuti
 * @param {number} weight - Peso in kg (opzionale, default 70)
 * @returns {number} Calorie bruciate
 */
export const calculateCalories = (type, duration, weight = 70) => {
  const MET_VALUES = {
    running: 9.8,
    cycling: 7.5,
    walking: 3.5,
    gym: 5.0,
    swimming: 8.0,
    yoga: 2.5,
    other: 4.0
  };

  const met = MET_VALUES[type] || MET_VALUES.other;
  return Math.round(met * weight * (duration / 60));
};

/**
 * Calcola la distanza percorsa in base ai passi
 * @param {number} steps - Numero di passi
 * @param {number} stepLength - Lunghezza del passo in metri (opzionale, default 0.75)
 * @returns {number} Distanza in km
 */
export const calculateDistanceFromSteps = (steps, stepLength = 0.75) => {
  const distanceInMeters = steps * stepLength;
  return parseFloat((distanceInMeters / 1000).toFixed(2));
};

/**
 * Calcola la distanza in base a velocità e durata
 * @param {number} speedKmh - Velocità in km/h
 * @param {number} durationMinutes - Durata in minuti
 * @returns {number} Distanza in km
 */
export const calculateDistance = (speedKmh, durationMinutes) => {
  return parseFloat(((speedKmh * durationMinutes) / 60).toFixed(2));
};

/**
 * Calcola il ritmo (minuti per km)
 * @param {number} distanceKm - Distanza in km
 * @param {number} durationMinutes - Durata in minuti
 * @returns {string} Ritmo in minuti:secondi per km
 */
export const calculatePace = (distanceKm, durationMinutes) => {
  if (distanceKm === 0) return '0:00';
  const minutesPerKm = durationMinutes / distanceKm;
  const mins = Math.floor(minutesPerKm);
  const secs = Math.round((minutesPerKm - mins) * 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

/**
 * Calcola le calorie bruciate dai passi
 * @param {number} steps - Numero di passi
 * @param {number} weight - Peso in kg (opzionale, default 70)
 * @returns {number} Calorie stimate
 */
export const calculateCaloriesFromSteps = (steps, weight = 70) => {
  // Media di 0.04 calorie per passo per persona di 70kg
  const caloriesPerStep = 0.04 * (weight / 70);
  return Math.round(steps * caloriesPerStep);
};

/**
 * Calcola il progresso verso un obiettivo
 * @param {number} current - Valore attuale
 * @param {number} target - Valore obiettivo
 * @returns {number} Percentuale di completamento (0-100)
 */
export const calculateProgress = (current, target) => {
  if (target === 0) return 0;
  return Math.min(Math.round((current / target) * 100), 100);
};

/**
 * Calcola i passi giornalieri medi della settimana
 * @param {Array} dailyStats - Array di statistiche giornaliere
 * @returns {number} Media dei passi
 */
export const calculateAverageSteps = (dailyStats) => {
  if (!dailyStats || dailyStats.length === 0) return 0;
  const total = dailyStats.reduce((sum, day) => sum + day.steps, 0);
  return Math.round(total / dailyStats.length);
};

/**
 * Raggruppa gli allenamenti per settimana
 * @param {Array} workouts - Array di allenamenti
 * @returns {Array} Array di settimane con i relativi allenamenti
 */
export const groupWorkoutsByWeek = (workouts) => {
  const weeks = {};

  workouts.forEach(workout => {
    const date = new Date(workout.date);
    const weekStart = startOfWeek(date, { weekStartsOn: 1 }); // Lunedì
    const weekKey = format(weekStart, 'yyyy-MM-dd');

    if (!weeks[weekKey]) {
      const weekEnd = endOfWeek(date, { weekStartsOn: 1 });
      weeks[weekKey] = {
        weekStart: weekStart.getTime(),
        weekEnd: weekEnd.getTime(),
        workouts: []
      };
    }

    weeks[weekKey].workouts.push(workout);
  });

  return Object.values(weeks).sort((a, b) => b.weekStart - a.weekStart);
};

/**
 * Ottiene le statistiche della settimana corrente
 * @param {Array} workouts - Array di allenamenti
 * @param {number} steps - Passi della settimana
 * @returns {Object} Statistiche settimanali
 */
export const getWeeklyStats = (workouts, steps = 0) => {
  const now = new Date();
  const weekStart = startOfWeek(now, { weekStartsOn: 1 });
  const weekEnd = endOfWeek(now, { weekStartsOn: 1 });

  const weekWorkouts = workouts.filter(w => {
    const date = new Date(w.date);
    return date >= weekStart && date <= weekEnd;
  });

  const totalCalories = weekWorkouts.reduce((sum, w) => sum + w.calories, 0);
  const totalDuration = weekWorkouts.reduce((sum, w) => sum + w.duration, 0);
  const totalDistance = weekWorkouts.reduce((sum, w) => sum + (w.distance || 0), 0);

  // Distribuzione per tipo
  const workoutByType = weekWorkouts.reduce((acc, w) => {
    acc[w.type] = (acc[w.type] || 0) + 1;
    return acc;
  }, {});

  // Distribuzione giornaliera
  const days = eachDayOfInterval({ start: weekStart, end: weekEnd });
  const dailySteps = days.map(day => {
    const dayWorkouts = weekWorkouts.filter(w => isSameDay(new Date(w.date), day));
    const daySteps = dayWorkouts.reduce((sum, w) => {
      // Stima passi dalla distanza (corsa: ~1300 passi/km, camminata: ~1400 passi/km)
      const stepsPerKm = w.type === 'running' ? 1300 : w.type === 'walking' ? 1400 : 0;
      return sum + (w.distance ? Math.round(w.distance * stepsPerKm) : 0);
    }, 0);
    return {
      date: format(day, 'EEE', { locale: it }),
      fullDate: day,
      steps: daySteps,
      calories: dayWorkouts.reduce((sum, w) => sum + w.calories, 0)
    };
  });

  return {
    workouts: weekWorkouts.length,
    calories: totalCalories,
    duration: totalDuration,
    distance: parseFloat(totalDistance.toFixed(2)),
    steps: steps,
    workoutByType,
    daily: dailySteps
  };
};

/**
 * Verifica se un achievement è sbloccato
 * @param {Object} achievement - Achievement da verificare
 * @param {Object} stats - Statistiche dell'utente
 * @returns {boolean} True se l'achievement è sbloccato
 */
export const isAchievementUnlocked = (achievement, stats) => {
  const { id, requirement } = achievement;

  switch (id) {
    case 'first_workout':
      return stats.totalWorkouts >= requirement;
    case 'week_streak':
      return stats.currentStreak >= requirement;
    case 'marathon':
      return stats.totalRunningDistance >= requirement;
    case 'century':
      return stats.totalWorkouts >= requirement;
    case 'steps_10k':
      return stats.maxDailySteps >= requirement;
    case 'calorie_goal':
      return stats.maxDailyCalories >= requirement;
    default:
      return false;
  }
};

/**
 * Formatta il tempo in minuti in formato leggibile
 * @param {number} minutes - Minuti
 * @returns {string} Tempo formattato (es: "1h 30min")
 */
export const formatDuration = (minutes) => {
  if (minutes < 60) {
    return `${minutes}min`;
  }
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return mins > 0 ? `${hours}h ${mins}min` : `${hours}h`;
};

/**
 * Formatta la distanza in modo leggibile
 * @param {number} km - Chilometri
 * @returns {string} Distanza formattata
 */
export const formatDistance = (km) => {
  if (km < 1) {
    return `${Math.round(km * 1000)}m`;
  }
  return `${km.toFixed(2)}km`;
};

/**
 * Calcola la serie di allenamenti consecutivi
 * @param {Array} workouts - Array di allenamenti
 * @returns {number} Numero di giorni consecutivi con allenamenti
 */
export const calculateStreak = (workouts) => {
  if (!workouts || workouts.length === 0) return 0;

  // Ottieni le date uniche degli allenamenti
  const uniqueDates = [...new Set(workouts.map(w =>
    format(new Date(w.date), 'yyyy-MM-dd')
  ))].sort().reverse();

  let streak = 0;
  let currentDate = new Date();
  currentDate.setHours(0, 0, 0, 0);

  for (const dateStr of uniqueDates) {
    const workoutDate = new Date(dateStr);
    workoutDate.setHours(0, 0, 0, 0);

    const diffDays = Math.floor((currentDate - workoutDate) / (1000 * 60 * 60 * 24));

    if (diffDays === streak) {
      streak++;
    } else if (diffDays > streak) {
      break;
    }
  }

  return streak;
};
