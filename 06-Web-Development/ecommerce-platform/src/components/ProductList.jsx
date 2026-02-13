import React, { useState, useMemo } from 'react';
import ProductCard from './ProductCard';
import './ProductList.css';

const ProductList = ({ products, title }) => {
  const [sortBy, setSortBy] = useState('default');
  const [priceRange, setPriceRange] = useState('all');

  const sortedAndFilteredProducts = useMemo(() => {
    let filtered = [...products];

    // Filtro per prezzo
    if (priceRange === 'under-50') {
      filtered = filtered.filter(p => p.price < 50);
    } else if (priceRange === '50-100') {
      filtered = filtered.filter(p => p.price >= 50 && p.price < 100);
    } else if (priceRange === '100-500') {
      filtered = filtered.filter(p => p.price >= 100 && p.price < 500);
    } else if (priceRange === 'over-500') {
      filtered = filtered.filter(p => p.price >= 500);
    }

    // Ordinamento
    if (sortBy === 'price-asc') {
      filtered.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-desc') {
      filtered.sort((a, b) => b.price - a.price);
    } else if (sortBy === 'name') {
      filtered.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === 'rating') {
      filtered.sort((a, b) => b.rating - a.rating);
    }

    return filtered;
  }, [products, sortBy, priceRange]);

  return (
    <div className="product-list-container">
      {title && <h2 className="product-list-title">{title}</h2>}

      <div className="filters-bar">
        <div className="filters-left">
          <span className="results-count">
            {sortedAndFilteredProducts.length} prodotti
          </span>
        </div>

        <div className="filters-right">
          <select
            value={priceRange}
            onChange={(e) => setPriceRange(e.target.value)}
            className="filter-select"
          >
            <option value="all">Tutti i prezzi</option>
            <option value="under-50">Sotto €50</option>
            <option value="50-100">€50 - €100</option>
            <option value="100-500">€100 - €500</option>
            <option value="over-500">Oltre €500</option>
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="filter-select"
          >
            <option value="default">Ordina per</option>
            <option value="price-asc">Prezzo: crescente</option>
            <option value="price-desc">Prezzo: decrescente</option>
            <option value="name">Nome: A-Z</option>
            <option value="rating">Valutazione</option>
          </select>
        </div>
      </div>

      {sortedAndFilteredProducts.length > 0 ? (
        <div className="products-grid">
          {sortedAndFilteredProducts.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      ) : (
        <div className="no-products">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ddd" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
          <p>Nessun prodotto trovato</p>
          <p>Prova a cambiare i filtri di ricerca</p>
        </div>
      )}
    </div>
  );
};

export default ProductList;
