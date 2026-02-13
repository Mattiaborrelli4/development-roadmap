import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import './Cart.css';

const Cart = ({ isPage = false }) => {
  const { items, removeItem, updateQuantity, getCartTotal, clearCart } = useCart();
  const navigate = useNavigate();

  const handleQuantityChange = (itemId, newQuantity) => {
    if (newQuantity < 1) {
      removeItem(itemId);
    } else {
      updateQuantity(itemId, newQuantity);
    }
  };

  const handleCheckout = () => {
    navigate('/checkout');
  };

  if (items.length === 0) {
    return (
      <div className={`cart-empty ${isPage ? 'page' : 'sidebar'}`}>
        <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#ddd" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        <h3>Il tuo carrello è vuoto</h3>
        <p>Aggiungi prodotti per iniziare lo shopping</p>
        <Link to="/products" className="continue-shopping-btn">
          Esplora Prodotti
        </Link>
      </div>
    );
  }

  return (
    <div className={`cart ${isPage ? 'cart-page' : 'cart-sidebar'}`}>
      <div className="cart-header">
        <h2>Carrello ({items.length} {items.length === 1 ? 'prodotto' : 'prodotti'})</h2>
        {items.length > 0 && (
          <button className="clear-cart-btn" onClick={clearCart}>
            Svuota Carrello
          </button>
        )}
      </div>

      <div className="cart-items">
        {items.map(item => (
          <div key={item.id} className="cart-item">
            <Link to={`/product/${item.id}`} className="item-image">
              <img src={item.image} alt={item.name} />
            </Link>

            <div className="item-details">
              <Link to={`/product/${item.id}`} className="item-name">
                {item.name}
              </Link>
              <span className="item-category">{item.category}</span>
              <div className="item-price">€{item.price.toFixed(2)}</div>
            </div>

            <div className="item-quantity">
              <button
                onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                disabled={item.quantity <= 1}
              >
                -
              </button>
              <input
                type="number"
                value={item.quantity}
                onChange={(e) => handleQuantityChange(item.id, parseInt(e.target.value) || 1)}
                min="1"
              />
              <button
                onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
              >
                +
              </button>
            </div>

            <div className="item-total">
              €{(item.price * item.quantity).toFixed(2)}
            </div>

            <button
              className="remove-item-btn"
              onClick={() => removeItem(item.id)}
              aria-label="Rimuovi prodotto"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <div className="summary-row">
          <span>Subtotale</span>
          <span>€{getCartTotal().toFixed(2)}</span>
        </div>
        <div className="summary-row">
          <span>Spedizione</span>
          <span>{getCartTotal() > 50 ? 'GRATIS' : '€5.99'}</span>
        </div>
        <div className="summary-row total">
          <span>Totale</span>
          <span>€{(getCartTotal() + (getCartTotal() > 50 ? 0 : 5.99)).toFixed(2)}</span>
        </div>

        <button className="checkout-btn" onClick={handleCheckout}>
          Procedi al Checkout
        </button>

        <Link to="/products" className="continue-shopping">
          Continua lo Shopping
        </Link>

        {getCartTotal() < 50 && (
          <div className="free-shipping-banner">
            Aggiungi €{(50 - getCartTotal()).toFixed(2)} per avere la spedizione gratuita!
          </div>
        )}
      </div>
    </div>
  );
};

export default Cart;
