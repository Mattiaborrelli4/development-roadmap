const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Inizializza database SQLite
const dbPath = path.join(__dirname, 'database.sqlite');
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Errore connessione database:', err.message);
  } else {
    console.log('Connesso al database SQLite');
    initDatabase();
  }
});

// Crea tabella todos se non esiste
function initDatabase() {
  const createTableSQL = `
    CREATE TABLE IF NOT EXISTS todos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      description TEXT,
      completed INTEGER DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `;

  db.run(createTableSQL, (err) => {
    if (err) {
      console.error('Errore creazione tabella:', err.message);
    } else {
      console.log('Tabella todos pronta');
    }
  });
}

// ================= ROUTES API =================

// GET /api/todos - Ottieni tutti i todos
app.get('/api/todos', (req, res) => {
  const sql = 'SELECT * FROM todos ORDER BY created_at DESC';

  db.all(sql, [], (err, rows) => {
    if (err) {
      res.status(500).json({
        success: false,
        error: err.message
      });
      return;
    }

    // Converti completed da 0/1 a boolean
    const todos = rows.map(todo => ({
      ...todo,
      completed: todo.completed === 1
    }));

    res.json({
      success: true,
      count: todos.length,
      data: todos
    });
  });
});

// GET /api/todos/:id - Ottieni un todo specifico
app.get('/api/todos/:id', (req, res) => {
  const { id } = req.params;
  const sql = 'SELECT * FROM todos WHERE id = ?';

  db.get(sql, [id], (err, row) => {
    if (err) {
      res.status(500).json({
        success: false,
        error: err.message
      });
      return;
    }

    if (!row) {
      res.status(404).json({
        success: false,
        error: 'Todo non trovato'
      });
      return;
    }

    res.json({
      success: true,
      data: {
        ...row,
        completed: row.completed === 1
      }
    });
  });
});

// POST /api/todos - Crea nuovo todo
app.post('/api/todos', (req, res) => {
  const { title, description, completed } = req.body;

  // Validazione
  if (!title || title.trim() === '') {
    res.status(400).json({
      success: false,
      error: 'Il titolo è obbligatorio'
    });
    return;
  }

  const sql = `
    INSERT INTO todos (title, description, completed)
    VALUES (?, ?, ?)
  `;
  const params = [
    title.trim(),
    description || '',
    completed ? 1 : 0
  ];

  db.run(sql, params, function(err) {
    if (err) {
      res.status(500).json({
        success: false,
        error: err.message
      });
      return;
    }

    // Recupera il todo creato
    db.get('SELECT * FROM todos WHERE id = ?', [this.lastID], (err, row) => {
      if (err) {
        res.status(500).json({
          success: false,
          error: err.message
        });
        return;
      }

      res.status(201).json({
        success: true,
        message: 'Todo creato con successo',
        data: {
          ...row,
          completed: row.completed === 1
        }
      });
    });
  });
});

// PUT /api/todos/:id - Aggiorna todo esistente
app.put('/api/todos/:id', (req, res) => {
  const { id } = req.params;
  const { title, description, completed } = req.body;

  // Verifica che il todo esista
  db.get('SELECT * FROM todos WHERE id = ?', [id], (err, row) => {
    if (err) {
      res.status(500).json({
        success: false,
        error: err.message
      });
      return;
    }

    if (!row) {
      res.status(404).json({
        success: false,
        error: 'Todo non trovato'
      });
      return;
    }

    // Costruisci query di aggiornamento dinamica
    const updates = [];
    const params = [];

    if (title !== undefined) {
      updates.push('title = ?');
      params.push(title.trim());
    }
    if (description !== undefined) {
      updates.push('description = ?');
      params.push(description);
    }
    if (completed !== undefined) {
      updates.push('completed = ?');
      params.push(completed ? 1 : 0);
    }

    if (updates.length === 0) {
      res.status(400).json({
        success: false,
        error: 'Nessun campo da aggiornare'
      });
      return;
    }

    updates.push('updated_at = CURRENT_TIMESTAMP');
    params.push(id);

    const sql = `UPDATE todos SET ${updates.join(', ')} WHERE id = ?`;

    db.run(sql, params, function(err) {
      if (err) {
        res.status(500).json({
          success: false,
          error: err.message
        });
        return;
      }

      // Recupera il todo aggiornato
      db.get('SELECT * FROM todos WHERE id = ?', [id], (err, updatedRow) => {
        if (err) {
          res.status(500).json({
            success: false,
            error: err.message
          });
          return;
        }

        res.json({
          success: true,
          message: 'Todo aggiornato con successo',
          data: {
            ...updatedRow,
            completed: updatedRow.completed === 1
          }
        });
      });
    });
  });
});

// PATCH /api/todos/:id/toggle - Toggle completed status
app.patch('/api/todos/:id/toggle', (req, res) => {
  const { id } = req.params;

  db.get('SELECT * FROM todos WHERE id = ?', [id], (err, row) => {
    if (err) {
      res.status(500).json({
        success: false,
        error: err.message
      });
      return;
    }

    if (!row) {
      res.status(404).json({
        success: false,
        error: 'Todo non trovato'
      });
      return;
    }

    const newCompleted = row.completed === 0 ? 1 : 0;
    const sql = `
      UPDATE todos
      SET completed = ?, updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `;

    db.run(sql, [newCompleted, id], function(err) {
      if (err) {
        res.status(500).json({
          success: false,
          error: err.message
        });
        return;
      }

      db.get('SELECT * FROM todos WHERE id = ?', [id], (err, updatedRow) => {
        if (err) {
          res.status(500).json({
            success: false,
            error: err.message
          });
          return;
        }

        res.json({
          success: true,
          message: 'Todo toggle completato',
          data: {
            ...updatedRow,
            completed: updatedRow.completed === 1
          }
        });
      });
    });
  });
});

// DELETE /api/todos/:id - Elimina todo
app.delete('/api/todos/:id', (req, res) => {
  const { id } = req.params;

  db.get('SELECT * FROM todos WHERE id = ?', [id], (err, row) => {
    if (err) {
      res.status(500).json({
        success: false,
        error: err.message
      });
      return;
    }

    if (!row) {
      res.status(404).json({
        success: false,
        error: 'Todo non trovato'
      });
      return;
    }

    const sql = 'DELETE FROM todos WHERE id = ?';

    db.run(sql, [id], function(err) {
      if (err) {
        res.status(500).json({
          success: false,
          error: err.message
        });
        return;
      }

      res.json({
        success: true,
        message: 'Todo eliminato con successo',
        data: {
          id: parseInt(id),
          deleted: true
        }
      });
    });
  });
});

// DELETE /api/todos - Elimina tutti i todos (opzionale)
app.delete('/api/todos', (req, res) => {
  const sql = 'DELETE FROM todos';

  db.run(sql, [], function(err) {
    if (err) {
      res.status(500).json({
        success: false,
        error: err.message
      });
      return;
    }

    res.json({
      success: true,
      message: `Eliminati ${this.changes} todos`,
      data: {
        deletedCount: this.changes
      }
    });
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Benvenuto nella TODO API',
    version: '1.0.0',
    endpoints: {
      'GET /api/todos': 'Ottieni tutti i todos',
      'GET /api/todos/:id': 'Ottieni un todo specifico',
      'POST /api/todos': 'Crea nuovo todo',
      'PUT /api/todos/:id': 'Aggiorna todo esistente',
      'PATCH /api/todos/:id/toggle': 'Toggle completed status',
      'DELETE /api/todos/:id': 'Elimina todo',
      'DELETE /api/todos': 'Elimina tutti i todos'
    }
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint non trovato'
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    error: 'Errore interno del server'
  });
});

// Avvia server
app.listen(PORT, () => {
  console.log(`\n=================================`);
  console.log(`🚀 Server TODO API in esecuzione`);
  console.log(`📡 Porta: ${PORT}`);
  console.log(`🌐 URL: http://localhost:${PORT}`);
  console.log(`💾 Database: ${dbPath}`);
  console.log(`=================================\n`);
});

// Gestione chiusura graceful
process.on('SIGINT', () => {
  console.log('\nChiusura database...');
  db.close((err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Database chiuso.');
    process.exit(0);
  });
});

module.exports = app;
