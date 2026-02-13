import React from 'react';
import { Link } from 'react-router-dom';
import { products, featuredProducts, categories } from '../data/products';
import ProductList from '../components/ProductList';
import './Home.css';

const Home = () => {
  const electronics = products.filter(p => p.category === 'Elettronica').slice(0, 4);
  const clothing = products.filter(p => p.category === 'Abbigliamento').slice(0, 4);

  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Benvenuto in ShopOnline</h1>
          <p>Scopri i migliori prodotti a prezzi imperdibili</p>
          <div className="hero-actions">
            <Link to="/products" className="btn-primary">
              Esplora Prodotti
            </Link>
            <Link to="/products?category=Elettronica" className="btn-secondary">
              Novità
            </Link>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="categories-section">
        <div className="container">
          <h2>Categorie</h2>
          <div className="categories-grid">
            {categories.filter(c => c !== 'Tutti').map(category => (
              <Link
                key={category}
                to={`/products?category=${encodeURIComponent(category)}`}
                className="category-card"
              >
                <div className="category-icon">
                  {category === 'Elettronica' && (
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect>
                      <rect x="9" y="9" width="6" height="6"></rect>
                      <line x1="9" y1="1" x2="9" y2="4"></line>
                      <line x1="15" y1="1" x2="15" y2="4"></line>
                      <line x1="9" y1="20" x2="9" y2="23"></line>
                      <line x1="15" y1="20" x2="15" y2="23"></line>
                      <line x1="20" y1="9" x2="23" y2="9"></line>
                      <line x1="20" y1="14" x2="23" y2="14"></line>
                      <line x1="1" y1="9" x2="4" y2="9"></line>
                      <line x1="1" y1="14" x2="4" y2="14"></line>
                    </svg>
                  )}
                  {category === 'Abbigliamento' && (
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M20.38 3.46L16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"></path>
                    </svg>
                  )}
                  {category === 'Casa' && (
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                      <polyline points="9 22 9 12 15 12 15 22"></polyline>
                    </svg>
                  )}
                  {category === 'Accessori' && (
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="8" x2="12" y2="12"></line>
                      <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                  )}
                </div>
                <span>{category}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="featured-section">
        <div className="container">
          <h2>Prodotti in Evidenza</h2>
          <ProductList products={featuredProducts} />
        </div>
      </section>

      {/* Electronics Preview */}
      <section className="preview-section">
        <div className="container">
          <div className="section-header">
            <h2>Elettronica</h2>
            <Link to="/products?category=Elettronica" className="view-all">
              Vedi tutti →
            </Link>
          </div>
          <ProductList products={electronics} />
        </div>
      </section>

      {/* Clothing Preview */}
      <section className="preview-section">
        <div className="container">
          <div className="section-header">
            <h2>Abbigliamento</h2>
            <Link to="/products?category=Abbigliamento" className="view-all">
              Vedi tutti →
            </Link>
          </div>
          <ProductList products={clothing} />
        </div>
      </section>

      {/* Features */}
      <section className="features-section">
        <div className="container">
          <div className="features-grid">
            <div className="feature">
              <div className="feature-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="1" y="3" width="15" height="13"></rect>
                  <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                  <circle cx="5.5" cy="18.5" r="2.5"></circle>
                  <circle cx="18.5" cy="18.5" r="2.5"></circle>
                </svg>
              </div>
              <h3>Spedizione Gratuita</h3>
              <p>Su ordini superiori a €50</p>
            </div>

            <div className="feature">
              <div className="feature-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
              </div>
              <h3>Pagamenti Sicuri</h3>
              <p>Transazioni 100% sicure</p>
            </div>

            <div className="feature">
              <div className="feature-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
              </div>
              <h3>Supporto 24/7</h3>
              <p>Assistenza sempre disponibile</p>
            </div>

            <div className="feature">
              <div className="feature-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M2.5 2v6h6M2.66 15.57a10 10 0 1 0 .57-8.38"></path>
                </svg>
              </div>
              <h3>Resi Gratuiti</h3>
              <p>30 giorni per cambiare idea</p>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter */}
      <section className="newsletter-section">
        <div className="container">
          <div className="newsletter">
            <h2>Iscriviti alla Newsletter</h2>
            <p>Ricevi offerte esclusive e aggiornamenti sui nuovi prodotti</p>
            <form className="newsletter-form">
              <input
                type="email"
                placeholder="La tua email"
                className="newsletter-input"
              />
              <button type="submit" className="newsletter-btn">
                Iscriviti
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
