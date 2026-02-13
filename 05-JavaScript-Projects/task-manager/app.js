// ============================================
// CLASSE TASK MANAGER
// ============================================
class TaskManager {
    constructor() {
        // Carica task dal localStorage o inizializza array vuoto
        this.tasks = this.loadTasks();
        this.currentFilter = 'all';
        this.currentSort = 'date';
        this.editingTaskId = null;

        // Inizializza l'applicazione
        this.init();
    }

    // ============================================
    // INIZIALIZZAZIONE
    // ============================================
    init() {
        this.bindEvents();
        this.render();
        this.updateStatistics();
    }

    bindEvents() {
        // Form aggiungi task
        document.getElementById('add-task-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTask();
        });

        // Filtri
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });

        // Ordinamento
        document.getElementById('sort-select').addEventListener('change', (e) => {
            this.setSort(e.target.value);
        });

        // Rimuovi completate
        document.getElementById('clear-completed').addEventListener('click', () => {
            this.clearCompleted();
        });

        // Modal modifica
        document.querySelector('.close-modal').addEventListener('click', () => {
            this.closeEditModal();
        });

        document.querySelector('.cancel-edit').addEventListener('click', () => {
            this.closeEditModal();
        });

        document.getElementById('edit-task-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveEditedTask();
        });

        // Chiudi modal cliccando fuori
        document.getElementById('edit-modal').addEventListener('click', (e) => {
            if (e.target.id === 'edit-modal') {
                this.closeEditModal();
            }
        });
    }

    // ============================================
    // OPERAZIONI CRUD
    // ============================================

    // CREATE - Aggiungi nuovo task
    addTask() {
        const title = document.getElementById('task-title').value.trim();
        const description = document.getElementById('task-description').value.trim();
        const category = document.getElementById('task-category').value;
        const priority = document.getElementById('task-priority').value;
        const dueDate = document.getElementById('task-due-date').value;

        // Validazione
        if (!title) {
            alert('Inserisci un titolo per l\'attività!');
            return;
        }

        // Crea nuovo task con spread operator
        const newTask = {
            id: Date.now().toString(),
            title,
            description,
            category,
            priority,
            dueDate,
            completed: false,
            createdAt: new Date().toISOString()
        };

        // Aggiungi all'array (spread operator per immutabilità)
        this.tasks = [...this.tasks, newTask];

        // Salva e aggiorna UI
        this.saveTasks();
        this.render();
        this.updateStatistics();

        // Reset form
        document.getElementById('add-task-form').reset();
    }

    // READ - Ottieni task filtrati e ordinati
    getFilteredTasks() {
        // FILTER - Filtra per stato
        const filtered = this.tasks.filter(task => {
            if (this.currentFilter === 'active') return !task.completed;
            if (this.currentFilter === 'completed') return task.completed;
            return true;
        });

        // SORT - Ordina i task
        const sorted = [...filtered].sort((a, b) => {
            switch (this.currentSort) {
                case 'priority':
                    return this.sortByPriority(a, b);
                case 'title':
                    return a.title.localeCompare(b.title);
                case 'date':
                default:
                    return this.sortByDate(a, b);
            }
        });

        return sorted;
    }

    // UPDATE - Modifica task esistente
    updateTask(id, updates) {
        // MAP - Trova e aggiorna il task
        this.tasks = this.tasks.map(task => {
            if (task.id === id) {
                return { ...task, ...updates };
            }
            return task;
        });

        this.saveTasks();
        this.render();
        this.updateStatistics();
    }

    // DELETE - Rimuovi task
    deleteTask(id) {
        if (!confirm('Sei sicuro di voler eliminare questa attività?')) return;

        // FILTER - Rimuovi il task
        this.tasks = this.tasks.filter(task => task.id !== id);

        this.saveTasks();
        this.render();
        this.updateStatistics();
    }

    // Toggle stato completato
    toggleTask(id) {
        this.updateTask(id, { completed: !this.tasks.find(t => t.id === id).completed });
    }

    // DELETE - Rimuovi tutti i task completati
    clearCompleted() {
        const completedCount = this.tasks.filter(t => t.completed).length;

        if (completedCount === 0) {
            alert('Non ci sono attività completate da rimuovere.');
            return;
        }

        if (!confirm(`Sei sicuro di voler rimuovere ${completedCount} attività completate?`)) return;

        // FILTER - Mantieni solo i task non completati
        this.tasks = this.tasks.filter(task => !task.completed);

        this.saveTasks();
        this.render();
        this.updateStatistics();
    }

    // ============================================
    // ORDINAMENTO
    // ============================================
    sortByPriority(a, b) {
        const priorityOrder = { alta: 0, media: 1, bassa: 2 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
    }

    sortByDate(a, b) {
        // Prima ordina per scadenza, poi per data di creazione
        if (a.dueDate && b.dueDate) {
            return new Date(a.dueDate) - new Date(b.dueDate);
        }
        if (a.dueDate) return -1;
        if (b.dueDate) return 1;
        return new Date(b.createdAt) - new Date(a.createdAt);
    }

    // ============================================
    // FILTRI E ORDINAMENTO
    // ============================================
    setFilter(filter) {
        this.currentFilter = filter;

        // Aggiorna UI bottoni filtro
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });

        this.render();
    }

    setSort(sort) {
        this.currentSort = sort;
        this.render();
    }

    // ============================================
    // MODALE MODIFICA
    // ============================================
    openEditModal(id) {
        const task = this.tasks.find(t => t.id === id);
        if (!task) return;

        this.editingTaskId = id;

        // Popola il form
        document.getElementById('edit-task-id').value = id;
        document.getElementById('edit-title').value = task.title;
        document.getElementById('edit-description').value = task.description || '';
        document.getElementById('edit-category').value = task.category;
        document.getElementById('edit-priority').value = task.priority;
        document.getElementById('edit-due-date').value = task.dueDate || '';

        // Mostra modal
        document.getElementById('edit-modal').classList.add('active');
    }

    closeEditModal() {
        document.getElementById('edit-modal').classList.remove('active');
        this.editingTaskId = null;
    }

    saveEditedTask() {
        const id = this.editingTaskId;
        const title = document.getElementById('edit-title').value.trim();
        const description = document.getElementById('edit-description').value.trim();
        const category = document.getElementById('edit-category').value;
        const priority = document.getElementById('edit-priority').value;
        const dueDate = document.getElementById('edit-due-date').value;

        if (!title) {
            alert('Il titolo è obbligatorio!');
            return;
        }

        this.updateTask(id, {
            title,
            description,
            category,
            priority,
            dueDate
        });

        this.closeEditModal();
    }

    // ============================================
    // STATISTICHE (REDUCE)
    // ============================================
    updateStatistics() {
        // REDUCE - Calcola le statistiche
        const stats = this.tasks.reduce((acc, task) => {
            acc.total++;
            if (task.completed) {
                acc.completed++;
            } else {
                acc.active++;
            }
            return acc;
        }, { total: 0, active: 0, completed: 0 });

        // Anima i numeri
        this.animateNumber('stat-total', stats.total);
        this.animateNumber('stat-active', stats.active);
        this.animateNumber('stat-completed', stats.completed);
    }

    animateNumber(elementId, target) {
        const element = document.getElementById(elementId);
        const current = parseInt(element.textContent) || 0;
        const increment = target > current ? 1 : -1;
        const duration = 300;
        const steps = Math.abs(target - current);
        const stepDuration = duration / steps;

        if (steps === 0) return;

        let value = current;
        const timer = setInterval(() => {
            value += increment;
            element.textContent = value;
            if (value === target) {
                clearInterval(timer);
            }
        }, stepDuration);
    }

    // ============================================
    // RENDERING (MAP)
    // ============================================
    render() {
        const tasksList = document.getElementById('tasks-list');
        const filteredTasks = this.getFilteredTasks();

        // Se non ci sono task
        if (filteredTasks.length === 0) {
            tasksList.innerHTML = '<p class="empty-state">Nessuna attività presente. Aggiungine una nuova!</p>';
            return;
        }

        // MAP - Genera HTML per ogni task
        const tasksHTML = filteredTasks.map(task => this.createTaskHTML(task)).join('');

        tasksList.innerHTML = tasksHTML;

        // Aggiungi event listeners ai task dinamici
        this.attachTaskEventListeners();
    }

    createTaskHTML(task) {
        const isOverdue = task.dueDate && new Date(task.dueDate) < new Date() && !task.completed;

        const categoryLabels = {
            lavoro: '💼 Lavoro',
            personale: '👤 Personale',
            studio: '📚 Studio',
            salute: '💪 Salute',
            altro: '📌 Altro'
        };

        const priorityLabels = {
            alta: '🔴 Alta',
            media: '🟡 Media',
            bassa: '🟢 Bassa'
        };

        const formattedDate = task.dueDate
            ? new Date(task.dueDate).toLocaleDateString('it-IT', {
                day: '2-digit',
                month: 'short',
                year: 'numeric'
            })
            : '';

        return `
            <div class="task-card ${task.completed ? 'completed' : ''}" data-task-id="${task.id}">
                <div class="task-header">
                    <input
                        type="checkbox"
                        class="task-checkbox"
                        ${task.completed ? 'checked' : ''}
                        onchange="taskManager.toggleTask('${task.id}')">
                    <h3 class="task-title">${this.escapeHTML(task.title)}</h3>
                </div>

                ${task.description ? `<p class="task-description">${this.escapeHTML(task.description)}</p>` : ''}

                <div class="task-meta">
                    <span class="meta-tag category-tag ${task.category}">
                        ${categoryLabels[task.category]}
                    </span>
                    <span class="meta-tag priority-tag ${task.priority}">
                        ${priorityLabels[task.priority]}
                    </span>
                    ${task.dueDate ? `
                        <span class="meta-tag due-date-tag ${isOverdue ? 'overdue' : ''}">
                            📅 ${formattedDate} ${isOverdue ? '(Scaduto!)' : ''}
                        </span>
                    ` : ''}
                </div>

                <div class="task-actions">
                    <button class="action-btn edit-btn" onclick="taskManager.openEditModal('${task.id}')">
                        ✏️ Modifica
                    </button>
                    <button class="action-btn delete-btn" onclick="taskManager.deleteTask('${task.id}')">
                        🗑️ Elimina
                    </button>
                </div>
            </div>
        `;
    }

    attachTaskEventListeners() {
        // Event listeners sono già aggiunti via inline onclick e onchange
        // Questo metodo è disponibile per future espansioni
    }

    // ============================================
    // LOCAL STORAGE
    // ============================================
    saveTasks() {
        localStorage.setItem('taskManagerTasks', JSON.stringify(this.tasks));
    }

    loadTasks() {
        const stored = localStorage.getItem('taskManagerTasks');
        return stored ? JSON.parse(stored) : [];
    }

    // ============================================
    // UTILITY
    // ============================================
    escapeHTML(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// ============================================
// INIZIALIZZAZIONE APP
// ============================================
const taskManager = new TaskManager();

// Rendi globale per accesso dagli event handlers inline
window.taskManager = taskManager;
