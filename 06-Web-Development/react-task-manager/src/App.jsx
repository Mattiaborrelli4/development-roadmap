import { useState, useEffect } from 'react';
import './App.css';

function App() {
  // Stati per gestire i task
  const [tasks, setTasks] = useState(() => {
    const savedTasks = localStorage.getItem('tasks');
    return savedTasks ? JSON.parse(savedTasks) : [];
  });

  const [newTask, setNewTask] = useState('');
  const [category, setCategory] = useState('lavoro');
  const [priority, setPriority] = useState('media');
  const [filter, setFilter] = useState('tutte');
  const [searchTerm, setSearchTerm] = useState('');

  // Salva nel localStorage quando i task cambiano
  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }, [tasks]);

  // Aggiungi nuovo task
  const addTask = () => {
    if (newTask.trim() === '') return;

    const task = {
      id: Date.now(),
      text: newTask,
      category,
      priority,
      completed: false,
      createdAt: new Date().toISOString()
    };

    setTasks([task, ...tasks]);
    setNewTask('');
  };

  // Elimina task
  const deleteTask = (id) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  // Toggle completamento task
  const toggleComplete = (id) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  // Filtra i task
  const filteredTasks = tasks.filter(task => {
    const matchesFilter = filter === 'tutte' ||
                         (filter === 'completate' && task.completed) ||
                         (filter === 'attive' && !task.completed);

    const matchesSearch = task.text.toLowerCase().includes(searchTerm.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  // Ordina per priorità
  const priorityOrder = { alta: 0, media: 1, bassa: 2 };
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    if (a.completed !== b.completed) {
      return a.completed ? 1 : -1;
    }
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });

  // Statistiche
  const stats = {
    total: tasks.length,
    completed: tasks.filter(t => t.completed).length,
    active: tasks.filter(t => !t.completed).length
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>📋 Task Manager</h1>
          <p className="subtitle">Gestisci i tuoi compiti in modo efficiente</p>
        </header>

        {/* Statistiche */}
        <div className="stats">
          <div className="stat-card">
            <span className="stat-number">{stats.total}</span>
            <span className="stat-label">Totale</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">{stats.active}</span>
            <span className="stat-label">Attive</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">{stats.completed}</span>
            <span className="stat-label">Completate</span>
          </div>
        </div>

        {/* Form per aggiungere task */}
        <div className="add-task-form">
          <input
            type="text"
            placeholder="Aggiungi un nuovo task..."
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addTask()}
            className="task-input"
          />

          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="category-select"
          >
            <option value="lavoro">💼 Lavoro</option>
            <option value="personale">👤 Personale</option>
            <option value="studio">📚 Studio</option>
            <option value="salute">💪 Salute</option>
            <option value="altre">📌 Altre</option>
          </select>

          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="priority-select"
          >
            <option value="alta">🔴 Alta</option>
            <option value="media">🟡 Media</option>
            <option value="bassa">🟢 Bassa</option>
          </select>

          <button onClick={addTask} className="add-button">
            ➕ Aggiungi
          </button>
        </div>

        {/* Filtri e ricerca */}
        <div className="filters">
          <div className="filter-buttons">
            <button
              className={`filter-btn ${filter === 'tutte' ? 'active' : ''}`}
              onClick={() => setFilter('tutte')}
            >
              Tutte
            </button>
            <button
              className={`filter-btn ${filter === 'attive' ? 'active' : ''}`}
              onClick={() => setFilter('attive')}
            >
              Attive
            </button>
            <button
              className={`filter-btn ${filter === 'completate' ? 'active' : ''}`}
              onClick={() => setFilter('completate')}
            >
              Completate
            </button>
          </div>

          <input
            type="text"
            placeholder="🔍 Cerca task..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        {/* Lista task */}
        <div className="tasks-list">
          {sortedTasks.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📝</div>
              <p>Nessun task trovato</p>
              <p className="empty-hint">Aggiungi un nuovo task per iniziare!</p>
            </div>
          ) : (
            sortedTasks.map(task => (
              <div key={task.id} className={`task-card ${task.completed ? 'completed' : ''}`}>
                <div className="task-header">
                  <button
                    onClick={() => toggleComplete(task.id)}
                    className={`checkbox ${task.completed ? 'checked' : ''}`}
                  >
                    {task.completed ? '✓' : ''}
                  </button>

                  <div className="task-content">
                    <h3 className={task.completed ? 'task-text-done' : 'task-text'}>
                      {task.text}
                    </h3>
                    <div className="task-meta">
                      <span className={`category-badge category-${task.category}`}>
                        {getCategoryEmoji(task.category)} {capitalizeFirst(task.category)}
                      </span>
                      <span className={`priority-badge priority-${task.priority}`}>
                        {getPriorityEmoji(task.priority)} {capitalizeFirst(task.priority)}
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={() => deleteTask(task.id)}
                    className="delete-button"
                    title="Elimina task"
                  >
                    🗑️
                  </button>
                </div>

                <div className="task-date">
                  {new Date(task.createdAt).toLocaleDateString('it-IT', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <footer className="footer">
          <p>
            {stats.completed === stats.total && stats.total > 0
              ? '🎉 Complimenti! Hai completato tutti i task!'
              : `${stats.active} task da completare`}
          </p>
        </footer>
      </div>
    </div>
  );
}

// Funzioni helper
function getCategoryEmoji(category) {
  const emojis = {
    lavoro: '💼',
    personale: '👤',
    studio: '📚',
    salute: '💪',
    altre: '📌'
  };
  return emojis[category] || '📌';
}

function getPriorityEmoji(priority) {
  const emojis = {
    alta: '🔴',
    media: '🟡',
    bassa: '🟢'
  };
  return emojis[priority] || '⚪';
}

function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export default App;
