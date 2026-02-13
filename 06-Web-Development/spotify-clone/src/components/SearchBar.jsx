import React from 'react';
import { FiSearch } from 'react-icons/fi';
import { useMusic } from '../contexts/MusicContext';

const SearchBar = ({ placeholder = "Cosa vuoi ascoltare?" }) => {
  const { searchQuery, setSearchQuery } = useMusic();

  return (
    <div className="search-container">
      <div className="search-bar" style={{ position: 'relative' }}>
        <input
          type="text"
          className="search-input"
          placeholder={placeholder}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <div className="search-icon">
          <FiSearch />
        </div>
      </div>
    </div>
  );
};

export default SearchBar;
