import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const { addItem } = useCart();
  const discount = Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100);

  const handleAddToCart = (e) => {
    e.preventDefault();
    addItem(product, 1);

    // Mostra notifica
    const notification = document.createElement('div');
    notification.className = 'notification success';
    notification.textContent = `${product.name} aggiunto al carrello!`;
    notification.style.position = 'fixed';
    notification.style.bottom = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
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
    <div className="product-card">
      <Link to={`/product/${product.id}`} className="product-link">
        <div className="product-image">
          <img src={product.image} alt={product.name} />
          {discount > 0 && (
            <span className="discount-badge">-{discount}%</span>
          )}
          {product.stock < 10 && product.stock > 0 && (
            <span className="stock-badge">Solo {product.stock} left!</span>
          )}
          {product.stock === 0 && (
            <span className="out-of-stock-badge">Esaurito</span>
          )}
        </div>
        <div className="product-info">
          <span className="product-category">{product.category}</span>
          <h3 className="product-name">{product.name}</h3>
          <div className="product-rating">
            {renderStars(product.rating)}
            <span className="reviews">({product.reviews})</span>
          </div>
          <div className="product-price">
            <span className="current-price">€{product.price.toFixed(2)}</span>
            {product.originalPrice > product.price && (
              <span className="original-price">€{product.originalPrice.toFixed(2)}</span>
            )}
          </div>
        </div>
      </Link>
      <button
        className="add-to-cart-btn"
        onClick={handleAddToCart}
        disabled={product.stock === 0}
      >
        {product.stock === 0 ? 'Esaurito' : 'Aggiungi al Carrello'}
      </button>
    </div>
  );
};

export default ProductCard;
