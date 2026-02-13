/**
 * Blog Platform - Frontend
 * SPA con Vanilla JavaScript
 */

// ==================== STATE ====================
let currentView = 'home';
let isAuthenticated = false;
let currentUser = null;

// ==================== API HELPERS ====================
const API = {
  async request(url, options = {}) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        }
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Errore nella richiesta');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // Auth
  login: (username, password) =>
    API.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    }),

  logout: () =>
    API.request('/api/auth/logout', { method: 'POST' }),

  checkAuth: () =>
    API.request('/api/auth/status'),

  // Posts
  getPosts: () =>
    API.request('/api/posts'),

  getPost: (id) =>
    API.request(`/api/posts/${id}`),

  createPost: (postData) =>
    API.request('/api/posts', {
      method: 'POST',
      body: JSON.stringify(postData)
    }),

  updatePost: (id, postData) =>
    API.request(`/api/posts/${id}`, {
      method: 'PUT',
      body: JSON.stringify(postData)
    }),

  deletePost: (id) =>
    API.request(`/api/posts/${id}`, { method: 'DELETE' })
};

// ==================== VIEWS ====================
const Views = {
  // Home - Lista Post
  home: async () => {
    try {
      const posts = await API.getPosts();

      if (posts.length === 0) {
        return `
          <div class="post-list-header">
            <h2>📚 Tutti i Post</h2>
            ${isAuthenticated ? '<a href="#" class="btn btn-primary" data-view="create">➕ Nuovo Post</a>' : ''}
          </div>
          <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <h3>Nessun post ancora</h3>
            <p>Crea il tuo primo post per iniziare!</p>
            ${isAuthenticated ? '<br><br><a href="#" class="btn btn-primary" data-view="create">Crea Primo Post</a>' : ''}
          </div>
        `;
      }

      const postsHTML = posts.map(post => `
        <article class="post-card">
          <h3 class="post-card-title">${escapeHtml(post.title)}</h3>
          <div class="post-card-meta">
            👤 ${escapeHtml(post.author)} | 📅 ${formatDate(post.created_at)}
          </div>
          <div class="post-card-excerpt">
            ${escapeHtml(post.content.substring(0, 200))}${post.content.length > 200 ? '...' : ''}
          </div>
          <div class="post-card-actions">
            <a href="#" class="btn btn-primary" data-view="post" data-id="${post.id}">📖 Leggi Tutto</a>
            ${isAuthenticated ? `
              <a href="#" class="btn btn-secondary" data-view="edit" data-id="${post.id}">✏️ Modifica</a>
              <button class="btn btn-danger" onclick="deletePost(${post.id})">🗑️ Elimina</button>
            ` : ''}
          </div>
        </article>
      `).join('');

      return `
        <div class="post-list-header">
          <h2>📚 Tutti i Post (${posts.length})</h2>
          ${isAuthenticated ? '<a href="#" class="btn btn-primary" data-view="create">➕ Nuovo Post</a>' : ''}
        </div>
        <div class="posts-grid">
          ${postsHTML}
        </div>
      `;
    } catch (error) {
      return `<div class="alert alert-error">Errore nel caricamento dei post: ${error.message}</div>`;
    }
  },

  // Singolo Post
  post: async (id) => {
    try {
      const post = await API.getPost(id);

      return `
        <div class="post-detail">
          <div class="post-detail-header">
            <h1 class="post-detail-title">${escapeHtml(post.title)}</h1>
            <div class="post-detail-meta">
              👤 Autore: <strong>${escapeHtml(post.author)}</strong> |
              📅 Pubblicato: ${formatDate(post.created_at)} |
              ${post.updated_at !== post.created_at ? `✏️ Aggiornato: ${formatDate(post.updated_at)}` : ''}
            </div>
          </div>
          <div class="post-detail-content">${escapeHtml(post.content)}</div>
          ${isAuthenticated ? `
            <div class="post-detail-actions">
              <a href="#" class="btn btn-secondary" data-view="edit" data-id="${post.id}">✏️ Modifica Post</a>
              <button class="btn btn-danger" onclick="deletePost(${post.id})">🗑️ Elimina Post</button>
            </div>
          ` : ''}
          <div style="margin-top: 30px;">
            <a href="#" class="btn btn-primary" data-view="home">← Torna alla Lista</a>
          </div>
        </div>
      `;
    } catch (error) {
      return `
        <div class="alert alert-error">Post non trovato</div>
        <a href="#" class="btn btn-primary" data-view="home">← Torna alla Lista</a>
      `;
    }
  },

  // Create Post
  create: () => {
    if (!isAuthenticated) {
      return `
        <div class="alert alert-error">⚠️ Devi essere autenticato per creare un post</div>
        <div class="login-container">
          <h2>🔐 Accedi</h2>
          <form onsubmit="handleLogin(event)">
            <div class="form-group">
              <label for="username">Username:</label>
              <input type="text" id="username" class="form-control" required>
            </div>
            <div class="form-group">
              <label for="password">Password:</label>
              <input type="password" id="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">Accedi</button>
          </form>
        </div>
      `;
    }

    return `
      <div class="editor-container">
        <h2>✏️ Crea Nuovo Post</h2>
        <form onsubmit="handleCreatePost(event)">
          <div class="form-group">
            <label for="title">Titolo:</label>
            <input type="text" id="title" class="form-control" placeholder="Inserisci il titolo..." required>
          </div>
          <div class="form-group">
            <label for="content">Contenuto:</label>
            <textarea id="content" class="form-control" placeholder="Scrivi il contenuto del post..." required></textarea>
          </div>
          <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <button type="submit" class="btn btn-success">➕ Pubblica Post</button>
            <a href="#" class="btn btn-secondary" data-view="home">← Annulla</a>
          </div>
        </form>
      </div>
    `;
  },

  // Edit Post
  edit: async (id) => {
    if (!isAuthenticated) {
      return `<div class="alert alert-error">⚠️ Non autorizzato</div>`;
    }

    try {
      const post = await API.getPost(id);

      return `
        <div class="editor-container">
          <h2>✏️ Modifica Post</h2>
          <form onsubmit="handleUpdatePost(event, ${id})">
            <div class="form-group">
              <label for="title">Titolo:</label>
              <input type="text" id="title" class="form-control" value="${escapeHtml(post.title)}" required>
            </div>
            <div class="form-group">
              <label for="content">Contenuto:</label>
              <textarea id="content" class="form-control" required>${escapeHtml(post.content)}</textarea>
            </div>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
              <button type="submit" class="btn btn-success">💾 Salva Modifiche</button>
              <a href="#" class="btn btn-secondary" data-view="post" data-id="${id}">← Annulla</a>
            </div>
          </form>
        </div>
      `;
    } catch (error) {
      return `<div class="alert alert-error">Errore nel caricamento del post</div>`;
    }
  },

  // Login
  login: () => `
    <div class="login-container">
      <h2>🔐 Accedi al Blog</h2>
      <form onsubmit="handleLogin(event)">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary" style="width: 100%;">Accedi</button>
      </form>
      <div style="margin-top: 20px; text-align: center; color: #6c757d;">
        <small>Admin di default: admin / admin123</small>
      </div>
    </div>
  `
};

// ==================== HANDLERS ====================
async function handleLogin(event) {
  event.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
    await API.login(username, password);
    await checkAuth();
    navigateTo('home');
  } catch (error) {
    renderError(error.message);
  }
}

async function handleLogout() {
  try {
    await API.logout();
    isAuthenticated = false;
    currentUser = null;
    updateAuthNav();
    navigateTo('home');
  } catch (error) {
    renderError(error.message);
  }
}

async function handleCreatePost(event) {
  event.preventDefault();

  const title = document.getElementById('title').value;
  const content = document.getElementById('content').value;

  try {
    await API.createPost({ title, content });
    renderSuccess('Post creato con successo!');
    setTimeout(() => navigateTo('home'), 1000);
  } catch (error) {
    renderError(error.message);
  }
}

async function handleUpdatePost(event, id) {
  event.preventDefault();

  const title = document.getElementById('title').value;
  const content = document.getElementById('content').value;

  try {
    await API.updatePost(id, { title, content });
    renderSuccess('Post aggiornato con successo!');
    setTimeout(() => navigateTo('post', id), 1000);
  } catch (error) {
    renderError(error.message);
  }
}

async function deletePost(id) {
  if (!confirm('Sei sicuro di voler eliminare questo post?')) {
    return;
  }

  try {
    await API.deletePost(id);
    renderSuccess('Post eliminato con successo!');
    setTimeout(() => navigateTo('home'), 1000);
  } catch (error) {
    renderError(error.message);
  }
}

// ==================== NAVIGATION ====================
async function navigateTo(view, param = null) {
  currentView = view;

  const app = document.getElementById('app');
  app.innerHTML = '<div class="loading">Caricamento...</div>';

  try {
    const content = await Views[view](param);
    app.innerHTML = content;
    attachEventListeners();
  } catch (error) {
    app.innerHTML = `<div class="alert alert-error">Errore: ${error.message}</div>`;
  }
}

function attachEventListeners() {
  document.querySelectorAll('[data-view]').forEach(element => {
    element.addEventListener('click', (e) => {
      e.preventDefault();
      const view = element.dataset.view;
      const id = element.dataset.id;
      navigateTo(view, id);
    });
  });
}

// ==================== AUTH ====================
async function checkAuth() {
  try {
    const data = await API.checkAuth();
    isAuthenticated = data.authenticated;
    currentUser = data.username;
    updateAuthNav();
  } catch (error) {
    isAuthenticated = false;
    currentUser = null;
    updateAuthNav();
  }
}

function updateAuthNav() {
  const authNav = document.getElementById('authNav');

  if (isAuthenticated) {
    authNav.innerHTML = `
      <span style="margin-right: 10px;">👤 ${escapeHtml(currentUser)}</span>
      <a href="#" class="nav-link" onclick="handleLogout()">🚪 Logout</a>
    `;
  } else {
    authNav.innerHTML = '<a href="#" class="nav-link" data-view="login">🔐 Login</a>';
  }
  attachEventListeners();
}

// ==================== UTILITIES ====================
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('it-IT', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function renderSuccess(message) {
  const app = document.getElementById('app');
  app.innerHTML = `<div class="alert alert-success">✅ ${message}</div>`;
}

function renderError(message) {
  const app = document.getElementById('app');
  app.innerHTML = `<div class="alert alert-error">❌ ${message}</div>`;
}

// ==================== INIT ====================
document.addEventListener('DOMContentLoaded', async () => {
  await checkAuth();
  navigateTo('home');
});
