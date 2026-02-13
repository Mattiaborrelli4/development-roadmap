# Blog Platform - Struttura Progetto

## 📂 Albero del Progetto

```
blog-platform/
│
├── 📄 server.js                 # Backend: Express server + API routes
├── 📄 package.json              # Dipendenze npm e script
├── 📄 package-lock.json         # Lockfile dipendenze
├── 📄 README.md                 # Documentazione completa
├── 📄 .gitignore                # File ignorati da git
├── 📄 start.bat                 # Quick Start (Windows)
├── 📄 start.sh                  # Quick Start (Linux/Mac)
│
├── 📁 public/                   # Frontend: Client-side files
│   ├── 📄 index.html             # HTML structure
│   ├── 📄 styles.css             # CSS styling
│   └── 📄 app.js                 # JavaScript SPA logic
│
└── 📄 database.json             # Database JSON (auto-generato)
```

## 📋 File Descrizione

### Backend (`server.js`)
- Express server configuration
- API REST endpoints
- Session management
- JSON database operations
- Authentication middleware

### Frontend (`public/`)

#### `index.html`
- Single page application structure
- Navigation header
- Main content container
- Footer

#### `styles.css`
- Modern gradient design
- Responsive layout
- Card-based UI
- Form styling
- Alert messages

#### `app.js`
- SPA routing
- API communication
- State management
- View rendering
- Event handling

### Configuration Files

#### `package.json`
```json
{
  "dependencies": {
    "express": "^4.18.2",        // Web framework
    "bcryptjs": "^2.4.3",         // Password hashing
    "cookie-parser": "^1.4.6",    // Cookie parsing
    "express-session": "^1.17.3"  // Session management
  }
}
```

#### `database.json`
```json
{
  "users": [...],   // Utenti registrati
  "posts": [...]    // Post del blog
}
```

## 🔄 Data Flow

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Browser   │────────▶│   Express   │────────▶│ database.json│
│ (Frontend)  │◀────────│   Server    │◀────────│  (Storage)   │
└─────────────┘         └─────────────┘         └──────────────┘
     │                          │
     │                          │
     └── SPA: app.js ───────────┘
          Views:
          - home (post list)
          - post (single post)
          - create (new post)
          - edit (update post)
          - login (auth)
```

## 🛣️ Routes

### Frontend Routes (SPA)
- `/` - Home page (post list)
- `/post/:id` - Single post view
- `/create` - Create new post (auth required)
- `/edit/:id` - Edit post (auth required)
- `/login` - Login page

### Backend API Routes
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/status` - Check auth status
- `GET /api/posts` - Get all posts
- `GET /api/posts/:id` - Get single post
- `POST /api/posts` - Create post (auth)
- `PUT /api/posts/:id` - Update post (auth)
- `DELETE /api/posts/:id` - Delete post (auth)

## 🔐 Authentication Flow

```
User → Login Form → POST /api/auth/login
                       ↓
                  Verify credentials
                  against database.json
                       ↓
                  Create session
                       ↓
                  Return success
                       ↓
                  Redirect to home
```

## 📝 Post CRUD Operations

```
CREATE → POST /api/posts
READ   → GET /api/posts
       → GET /api/posts/:id
UPDATE → PUT /api/posts/:id
DELETE → DELETE /api/posts/:id
```

## 🎨 UI Components

### Header
- Logo/Title
- Navigation links
- Auth status display

### Main Content
- Post list (card-based)
- Post detail view
- Post editor (create/edit)
- Login form

### Footer
- Copyright info
- Credits

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start server
npm start

# Or use quick start scripts
./start.bat    # Windows
./start.sh     # Linux/Mac
```

Server runs at: http://localhost:3000

## 🔧 Development

### File Watching (Optional)
For auto-reload during development:
```bash
npm install -g nodemon
nodemon server.js
```

### Database Management
```bash
# Reset database
rm database.json
# Server will recreate on next start
```

---

**Note:** This is a simplified architecture suitable for learning and small projects.
For production, consider:
- Proper database (PostgreSQL, MongoDB)
- Environment variables
- Rate limiting
- Input validation library
- Error handling middleware
- Logging system
- Testing framework
