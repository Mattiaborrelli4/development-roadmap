# 🏗️ Architettura Spotify Clone

## 📊 Diagramma Architettura

```
┌─────────────────────────────────────────────────────────────┐
│                        BROWSER                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     index.html                              │
│                        (root)                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    React App                                 │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌──────────────────────┐         ┌──────────────────────┐
│   MusicProvider      │         │   BrowserRouter       │
│   (Context)         │         │   (Router)           │
└──────────────────────┘         └──────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       App Layout                             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────────────────────────────┐  │
│  │          │  │                                       │  │
│  │ Sidebar  │  │         Main Content Area            │  │
│  │          │  │  ┌────────────────────────────────┐  │  │
│  │ - Home   │  │  │                                │  │  │
│  │ - Search │  │  │   <Routes>                    │  │  │
│  │ - Library│  │  │     /          → Home          │  │  │
│  │ - Liked  │  │  │     /search    → Search        │  │  │
│  │          │  │  │     /library   → Library       │  │  │
│  │ Playlists│  │  │     /playlist/:id → Detail     │  │  │
│  │          │  │  │     /liked     → Liked        │  │  │
│  └──────────┘  │  │   </Routes>                   │  │  │
│               │  │                                │  │  │
│               │  └────────────────────────────────┘  │  │
│               │                                       │  │
└───────────────┴───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Player Bar                                │
│  [◀] [▶] [▶▶] [Progress] [Volume]                           │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### 1. App Initialization
```
index.js → App.jsx → MusicProvider → BrowserRouter → Routes
```

### 2. State Management Flow
```
Component → useContext(MusicContext) → Context State → UI Update
```

### 3. Navigation Flow
```
User Click → NavLink → Router Match → Page Render
```

### 4. Player Control Flow
```
User Action → Handler Function → Context Dispatch → State Update → Re-render
```

## 🎯 Component Hierarchy

```
App
├── MusicProvider (Context)
│   └── Provides global music state
│
├── BrowserRouter (Router)
│   └── Routes
│       ├── Route: "/" → Home
│       ├── Route: "/search" → Search
│       ├── Route: "/library" → Library
│       ├── Route: "/playlist/:id" → PlaylistDetail
│       └── Route: "/liked" → Liked
│
├── Sidebar
│   ├── Navigation Links
│   ├── Playlist List
│   └── Create Playlist Modal
│
├── Pages
│   ├── Home
│   │   ├── Playlist Cards
│   │   ├── Artist Cards
│   │   └── Track List
│   │
│   ├── Search
│   │   ├── SearchBar
│   │   ├── Category Cards
│   │   └── Search Results
│   │
│   ├── Library
│   │   ├── Playlist Cards
│   │   └── Artist Cards
│   │
│   ├── PlaylistDetail
│   │   ├── Playlist Header
│   │   └── TrackList
│   │
│   └── Liked
│       └── TrackList
│
└── Player
    ├── Current Track Info
    ├── Playback Controls
    ├── Progress Bar
    └── Volume Controls
```

## 📦 Module Dependencies

### Core Dependencies
```
┌────────────────────────────────────────┐
│           App.jsx                      │
├────────────────────────────────────────┤
│  ├─ React Router DOM                   │
│  ├─ MusicContext (Provider)            │
│  ├─ Sidebar                           │
│  ├─ Pages (Home, Search, etc.)        │
│  └─ Player                            │
└────────────────────────────────────────┘
```

### Component Dependencies
```
┌────────────────────────────────────────┐
│           Pages                        │
├────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────┐  │
│  │ Home        │  │ PlaylistDetail  │  │
│  ├─────────────┤  ├─────────────────┤  │
│  │ PlaylistCard│  │ TrackList       │  │
│  │ TrackList   │  └─────────────────┘  │
│  └─────────────┘                        │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│           Components                  │
├────────────────────────────────────────┤
│  Player        │ Uses MusicContext     │
│  Sidebar       │ Uses MusicContext     │
│  TrackList     │ Uses MusicContext     │
│  Playlist      │ Independent           │
│  SearchBar     │ Uses MusicContext     │
└────────────────────────────────────────┘
```

### Context Dependencies
```
┌────────────────────────────────────────┐
│         MusicContext                   │
├────────────────────────────────────────┤
│  ┌──────────────────────────────────┐  │
│  │      State (useReducer)          │  │
│  ├──────────────────────────────────┤  │
│  │ • currentTrack                   │  │
│  │ • isPlaying                      │  │
│  │ • playlist                       │  │
│  │ • volume                         │  │
│  │ • progress                       │  │
│  │ • shuffle                        │  │
│  │ • repeat                         │  │
│  │ • likedTracks (useState)         │  │
│  │ • userPlaylists                  │  │
│  └──────────────────────────────────┘  │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │      Methods                      │  │
│  ├──────────────────────────────────┤  │
│  │ • playTrack()                    │  │
│  │ • togglePlay()                   │  │
│  │ • nextTrack()                    │  │
│  │ • prevTrack()                    │  │
│  │ • setVolume()                    │  │
│  │ • toggleMute()                   │  │
│  │ • toggleShuffle()                │  │
│  │ • toggleRepeat()                 │  │
│  │ • toggleLike()                   │  │
│  │ • createPlaylist()               │  │
│  │ • deletePlaylist()               │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

## 🔄 State Flow Examples

### Play Track Flow
```
1. User clicks track in TrackList
2. TrackList calls handleTrackClick()
3. handleTrackClick() calls playTrack(track, playlist, index)
4. playTrack() dispatches SET_TRACK, SET_PLAYING, SET_PLAYLIST
5. MusicReducer updates state
6. Player component re-renders with new state
7. UI shows new track in playing state
```

### Create Playlist Flow
```
1. User clicks "Crea Playlist" in Sidebar
2. Modal appears
3. User fills form and submits
4. handleSubmit() calls createPlaylist(name, description)
5. createPlaylist() dispatches ADD_PLAYLIST
6. MusicReducer updates userPlaylists state
7. Sidebar re-renders with new playlist
```

### Search Flow
```
1. User types in SearchBar
2. onChange calls setSearchQuery()
3. Search page re-renders with new query
4. useMemo recalculates filtered results
5. Results display in real-time
```

## 🎨 CSS Architecture

### CSS Custom Properties (Variables)
```
:root
├── Colors
│   ├── --bg-black
│   ├── --bg-dark
│   ├── --bg-elevated
│   ├── --bg-light
│   ├── --text-primary
│   ├── --text-secondary
│   └── --spotify-green
│
├── Spacing
│   ├── --spacing-xs (8px)
│   ├── --spacing-sm (16px)
│   ├── --spacing-md (24px)
│   └── --spacing-lg (32px)
│
└── Layout
    ├── --sidebar-width (280px)
    ├── --player-height (90px)
    └── --border-radius (4px, 8px, 500px)
```

### Component Styling
```
App.css
├── Reset & Base
├── Layout
│   ├── .app-container
│   ├── .sidebar
│   ├── .main-content
│   └── .player-bar
├── Components
│   ├── .playlist-card
│   ├── .track-item
│   ├── .nav-item
│   └── .modal
├── Utilities
│   ├── .text-truncate
│   ├── .mt-2, .mt-4
│   └── .mb-2, .mb-4
└── Responsive
    └── @media queries
```

## 🔐 Security Considerations

### Current State
- No authentication (demo app)
- No API keys needed
- Client-side only
- Sample data included

### Future Improvements
- [ ] Implement OAuth 2.0
- [ ] Add environment variables
- [ ] Secure API endpoints
- [ ] XSS prevention
- [ ] CSRF protection

## ⚡ Performance Optimization

### Current Optimizations
- React.memo ready (future)
- Lazy loading ready (future)
- Virtual scrolling ready (future)
- CSS animations (GPU accelerated)

### Future Optimizations
- [ ] Code splitting per route
- [ ] Image lazy loading
- [ ] State persistence with IndexedDB
- [ ] Service worker caching
- [ ] CDN for static assets

## 🧪 Testing Strategy (Future)

### Unit Tests
```javascript
describe('MusicContext', () => {
  it('should play track', () => {})
  it('should toggle play', () => {})
  it('should add playlist', () => {})
})
```

### Integration Tests
```javascript
describe('Player', () => {
  it('should update on track change', () => {})
  it('should control playback', () => {})
})
```

### E2E Tests
```javascript
test('user journey: create playlist', () => {
  click('Create Playlist')
  fill('Name', 'My Playlist')
  click('Create')
  expect(text('My Playlist')).toExist()
})
```

## 📈 Scalability

### Current Scale
- 30 tracks
- 6 playlists
- 6 artists
- Single user

### Scalable To
- 1000+ tracks (with virtual scrolling)
- 100+ playlists
- 10,000+ users (with backend)
- Millions of tracks (with Spotify API)

---

**Architecture Version**: 1.0
**Last Updated**: February 2024
**Status**: Production Ready (Demo)
