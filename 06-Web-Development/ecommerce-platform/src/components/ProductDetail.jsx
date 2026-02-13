import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { products } from '../data/products';
import { useCart } from '../contexts/CartContext';
import ProductList from './ProductList';
import './ProductDetail.css';

const ProductDetail = () => {
  const { id } = useParams();
  const { addItem } = useCart();
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);
  const [selectedTab, setSelectedTab] = useState('description');

  const product = products.find(p => p.id === parseInt(id));

  if (!product) {
    return (
      <div className="product-not-found">
        <h2>Prodotto non trovato</h2>
        <Link to="/products">Torna ai prodotti</Link>
      </div>
    );
  }

  const relatedProducts = products
    .filter(p => p.category === product.category && p.id !== product.id)
    .slice(0, 4);

  const discount = Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100);

  const handleAddToCart = () => {
    for (let i = 0; i < quantity; i++) {
      addItem(product, 1);
    }

    const notification = document.createElement('div');
    notification.className = 'notification success';
    notification.textContent = `${quantity} x ${product.name} aggiunto al carrello!`;
    notification.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 9999;
      background: #2ecc71;
      color: white;
      padding: 1rem 1.5rem;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 3000);
  };

  const renderStars = (rating) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      if (i <= rating) {
        stars.push(<span key={i} className="star filled">★</span>);
      } else if (i - 0.5 <= rating) {
        stars.push(<span key={i} className="star half">★</span>);
      } else {
        stars.push(<span key={i} className="star">★</span>);
      }
    }
    return stars;
  };

  return (
    <div className="product-detail-container">
      {/* Breadcrumb */}
      <nav className="breadcrumb">
        <Link to="/">Home</Link>
        <span>/</span>
        <Link to="/products">Prodotti</Link>
        <span>/</span>
        <Link to={`/products?category=${product.category}`}>{product.category}</Link>
        <span>/</span>
        <span>{product.name}</span>
      </nav>

      <div className="product-detail">
        {/* Galleria immagini */}
        <div className="product-gallery">
          <div className="main-image">
            <img
              src={product.images ? product.images[selectedImage] : product.image}
              alt={product.name}
            />
            {discount > 0 && (
              <span className="discount-badge">-{discount}%</span>
            )}
          </div>
          {product.images && product.images.length > 1 && (
            <div className="thumbnail-gallery">
              {product.images.map((img, index) => (
                <button
                  key={index}
                  className={`thumbnail ${selectedImage === index ? 'active' : ''}`}
                  onClick={() => setSelectedImage(index)}
                >
                  <img src={img} alt={`${product.name} ${index + 1}`} />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Informazioni prodotto */}
        <div className="product-info">
          <span className="product-category">{product.category}</span>
          <h1 className="product-title">{product.name}</h1>

          <div className="product-rating">
            <div className="stars">{renderStars(product.rating)}</div>
            <span className="reviews">{product.reviews} recensioni</span>
            {product.stock < 10 && product.stock > 0 && (
              <span className="stock-warning">Solo {product.stock} disponibili!</span>
            )}
          </div>

          <div className="price-section">
            <span className="current-price">€{product.price.toFixed(2)}</span>
            {product.originalPrice > product.price && (
              <>
                <span className="original-price">€{product.originalPrice.toFixed(2)}</span>
                <span className="discount">-{discount}%</span>
              </>
            )}
          </div>

          <div className="quantity-selector">
            <label>Quantità:</label>
            <div className="quantity-controls">
              <button
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                disabled={quantity <= 1}
              >
                -
              </button>
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                min="1"
                max={product.stock}
              />
              <button
                onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                disabled={quantity >= product.stock}
              >
                +
              </button>
            </div>
          </div>

          <div className="action-buttons">
            <button
              className="add-to-cart-btn"
              onClick={handleAddToCart}
              disabled={product.stock === 0}
            >
              {product.stock === 0 ? 'Esaurito' : 'Aggiungi al Carrello'}
            </button>
          </div>

          {/* Tabs */}
          <div className="product-tabs">
            <div className="tabs-header">
              <button
                className={selectedTab === 'description' ? 'active' : ''}
                onClick={() => setSelectedTab('description')}
              >
                Descrizione
              </button>
              <button
                className={selectedTab === 'features' ? 'active' : ''}
                onClick={() => setSelectedTab('features')}
              >
                Caratteristiche
              </button>
            </div>
            <div className="tabs-content">
              {selectedTab === 'description' && (
                <div className="tab-pane">
                  <p>{product.description}</p>
                </div>
              )}
              {selectedTab === 'features' && (
                <div className="tab-pane">
                  <ul>
                    {product.features?.map((feature, index) => (
                      <li key={index}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Prodotti correlati */}
      {relatedProducts.length > 0 && (
        <div className="related-products">
          <h2>Prodotti Correlati</h2>
          <ProductList products={relatedProducts} />
        </div>
      )}
    </div>
  );
};

export default ProductDetail;
