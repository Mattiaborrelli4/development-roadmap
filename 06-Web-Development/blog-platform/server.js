/**
 * Blog Platform - Server
 * Full-Stack Blog con Node.js, Express e SQLite
 */

const express = require('express');
const path = require('path');
const fs = require('fs');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const bcrypt = require('bcryptjs');

const app = express();
const PORT = process.env.PORT || 3000;

// ==================== DATABASE MANAGEMENT ====================
// Sistema semplice basato su file JSON
const DB_FILE = path.join(__dirname, 'database.json');

// Inizializza database
function initDatabase() {
  if (!fs.existsSync(DB_FILE)) {
    const initialData = {
      users: [
        {
          id: 1,
          username: 'admin',
          password: bcrypt.hashSync('admin123', 10),
          created_at: new Date().toISOString()
        }
      ],
      posts: []
    };
    fs.writeFileSync(DB_FILE, JSON.stringify(initialData, null, 2));
    console.log('✅ Database creato - Admin account: admin / admin123');
  }
}

// Leggi database
function readDatabase() {
  const data = fs.readFileSync(DB_FILE, 'utf8');
  return JSON.parse(data);
}

// Scrivi database
function writeDatabase(data) {
  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
}

// Inizializza il database all'avvio
initDatabase();

// ==================== MIDDLEWARE ====================
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(session({
  secret: 'blog-secret-key-2024',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 24 * 60 * 60 * 1000 } // 24 ore
}));

// Serve file statici
app.use(express.static('public'));

// Middleware per autenticazione
const requireAuth = (req, res, next) => {
  if (req.session.userId) {
    next();
  } else {
    res.status(401).json({ error: 'Non autorizzato' });
  }
};

// ==================== API ROUTES ====================

// Auth - Login
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  const db = readDatabase();

  const user = db.users.find(u => u.username === username);

  if (user && bcrypt.compareSync(password, user.password)) {
    req.session.userId = user.id;
    req.session.username = user.username;
    res.json({ success: true, username: user.username });
  } else {
    res.status(401).json({ error: 'Credenziali non valide' });
  }
});

// Auth - Logout
app.post('/api/auth/logout', (req, res) => {
  req.session.destroy();
  res.json({ success: true });
});

// Auth - Status
app.get('/api/auth/status', (req, res) => {
  if (req.session.userId) {
    res.json({ authenticated: true, username: req.session.username });
  } else {
    res.json({ authenticated: false });
  }
});

// Posts - Ottieni tutti i post
app.get('/api/posts', (req, res) => {
  const db = readDatabase();
  const posts = db.posts.sort((a, b) =>
    new Date(b.created_at) - new Date(a.created_at)
  );
  res.json(posts);
});

// Posts - Ottieni singolo post
app.get('/api/posts/:id', (req, res) => {
  const db = readDatabase();
  const post = db.posts.find(p => p.id === parseInt(req.params.id));

  if (post) {
    res.json(post);
  } else {
    res.status(404).json({ error: 'Post non trovato' });
  }
});

// Posts - Crea nuovo post
app.post('/api/posts', requireAuth, (req, res) => {
  const { title, content } = req.body;

  if (!title || !content) {
    return res.status(400).json({ error: 'Titolo e contenuto obbligatori' });
  }

  const db = readDatabase();
  const newId = db.posts.length > 0 ? Math.max(...db.posts.map(p => p.id)) + 1 : 1;

  const newPost = {
    id: newId,
    title,
    content,
    author: req.session.username,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  db.posts.push(newPost);
  writeDatabase(db);

  res.status(201).json(newPost);
});

// Posts - Aggiorna post
app.put('/api/posts/:id', requireAuth, (req, res) => {
  const { title, content } = req.body;

  if (!title || !content) {
    return res.status(400).json({ error: 'Titolo e contenuto obbligatori' });
  }

  const db = readDatabase();
  const postIndex = db.posts.findIndex(p => p.id === parseInt(req.params.id));

  if (postIndex !== -1) {
    db.posts[postIndex].title = title;
    db.posts[postIndex].content = content;
    db.posts[postIndex].updated_at = new Date().toISOString();

    writeDatabase(db);
    res.json(db.posts[postIndex]);
  } else {
    res.status(404).json({ error: 'Post non trovato' });
  }
});

// Posts - Elimina post
app.delete('/api/posts/:id', requireAuth, (req, res) => {
  const db = readDatabase();
  const postIndex = db.posts.findIndex(p => p.id === parseInt(req.params.id));

  if (postIndex !== -1) {
    db.posts.splice(postIndex, 1);
    writeDatabase(db);
    res.json({ success: true });
  } else {
    res.status(404).json({ error: 'Post non trovato' });
  }
});

// Serve la homepage per tutte le altre route
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Avvio server
app.listen(PORT, () => {
  console.log(`\n🚀 Server avviato su http://localhost:${PORT}`);
  console.log(`📝 Blog Platform Ready!`);
  console.log(`🔑 Admin Login: admin / admin123\n`);
});
