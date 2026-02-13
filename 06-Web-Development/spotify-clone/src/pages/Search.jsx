import React, { useMemo } from 'react';
import { playlists, tracks, artists } from '../data';
import PlaylistCard from '../components/Playlist';
import { useMusic } from '../contexts/MusicContext';
import TrackList from '../components/TrackList';

const categories = [
  { id: 1, name: 'Pop', image: 'https://picsum.photos/seed/cat1/300/200' },
  { id: 2, name: 'Hip-Hop', image: 'https://picsum.photos/seed/cat2/300/200' },
  { id: 3, name: 'Rock', image: 'https://picsum.photos/seed/cat3/300/200' },
  { id: 4, name: 'Electronica', image: 'https://picsum.photos/seed/cat4/300/200' },
  { id: 5, name: 'Latina', image: 'https://picsum.photos/seed/cat5/300/200' },
  { id: 6, name: 'Classica', image: 'https://picsum.photos/seed/cat6/300/200' },
  { id: 7, name: 'Jazz', image: 'https://picsum.photos/seed/cat7/300/200' },
  { id: 8, name: 'Indie', image: 'https://picsum.photos/seed/cat8/300/200' },
  { id: 9, name: 'R&B', image: 'https://picsum.photos/seed/cat9/300/200' },
  { id: 10, name: 'Metal', image: 'https://picsum.photos/seed/cat10/300/200' },
  { id: 11, name: 'Country', image: 'https://picsum.photos/seed/cat11/300/200' },
  { id: 12, name: 'Folk', image: 'https://picsum.photos/seed/cat12/300/200' }
];

const Search = () => {
  const { searchQuery, allTracks } = useMusic();

  const filteredTracks = useMemo(() => {
    if (!searchQuery) return [];
    return allTracks.filter(track =>
      track.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      track.artist.toLowerCase().includes(searchQuery.toLowerCase()) ||
      track.album.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [searchQuery, allTracks]);

  const filteredPlaylists = useMemo(() => {
    if (!searchQuery) return [];
    return playlists.filter(playlist =>
      playlist.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      playlist.description.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [searchQuery]);

  const filteredArtists = useMemo(() => {
    if (!searchQuery) return [];
    return artists.filter(artist =>
      artist.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [searchQuery]);

  return (
    <div className="main-content">
      <div className="content-header">
        <div className="content-nav">
          <button className="nav-arrow">
            <svg viewBox="0 0 24 24">
              <path d="M15.957 2.793a1 1 0 010 1.414L8.164 12l7.793 7.793a1 1 0 01-1.414 1.414L5.336 12l9.207-9.207a1 1 0 011.414 0z" />
            </svg>
          </button>
          <button className="nav-arrow" disabled>
            <svg viewBox="0 0 24 24">
              <path d="M8.043 2.793a1 1 0 000 1.414L15.836 12l-7.793 7.793a1 1 0 001.414 1.414L18.664 12 9.457 2.793a1 1 0 00-1.414 0z" />
            </svg>
          </button>
        </div>

        <div className="user-menu">
          <img
            src="https://i.pravatar.cc/150?img=68"
            alt="Utente"
          />
          <span>Matteo</span>
        </div>
      </div>

      {searchQuery ? (
        <div className="search-results">
          {(filteredTracks.length > 0 || filteredPlaylists.length > 0 || filteredArtists.length > 0) ? (
            <>
              {filteredTracks.length > 0 && (
                <section className="mb-4">
                  <h2 className="section-title">Brani</h2>
                  <TrackList tracks={filteredTracks} />
                </section>
              )}

              {filteredPlaylists.length > 0 && (
                <section className="mb-4">
                  <h2 className="section-title">Playlist</h2>
                  <div className="playlists-grid">
                    {filteredPlaylists.map(playlist => (
                      <PlaylistCard key={playlist.id} playlist={playlist} />
                    ))}
                  </div>
                </section>
              )}

              {filteredArtists.length > 0 && (
                <section className="mb-4">
                  <h2 className="section-title">Artisti</h2>
                  <div className="artists-grid">
                    {filteredArtists.map(artist => (
                      <div key={artist.id} className="artist-card">
                        <div className="artist-card-image">
                          <img src={artist.image} alt={artist.name} />
                        </div>
                        <div className="artist-card-name">{artist.name}</div>
                        <div className="artist-card-followers">{artist.followers} follower</div>
                      </div>
                    ))}
                  </div>
                </section>
              )}
            </>
          ) : (
            <div className="empty-state">
              <div className="empty-state-icon">🔍</div>
              <h3 className="empty-state-title">Nessun risultato</h3>
              <p className="empty-state-desc">
                Non siamo riusciti a trovare quello che cercavi.
              </p>
            </div>
          )}
        </div>
      ) : (
        <>
          <section className="mb-4">
            <h2 className="section-title">Esplora tutto</h2>
            <div className="browse-categories">
              {categories.map(category => (
                <div key={category.id} className="category-card">
                  <div className="category-card-name">{category.name}</div>
                </div>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
};

export default Search;
