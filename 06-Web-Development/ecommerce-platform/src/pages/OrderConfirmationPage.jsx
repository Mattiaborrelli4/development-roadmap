import React from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import './OrderConfirmationPage.css';

const OrderConfirmationPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { order } = location.state || {};

  if (!order) {
    navigate('/');
    return null;
  }

  return (
    <div className="order-confirmation">
      <div className="container">
        <div className="confirmation-card">
          <div className="success-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>

          <h1>Ordine Confermato!</h1>
          <p className="order-number">Ordine #{order.id}</p>

          <p className="confirmation-message">
            Grazie per il tuo acquisto! Riceverai una email di conferma con i dettagli dell'ordine.
          </p>

          <div className="order-summary">
            <h2>Riepilogo Ordine</h2>

            <div className="summary-items">
              {order.items.map((item, index) => (
                <div key={index} className="summary-item">
                  <img src={item.image} alt={item.name} />
                  <div className="item-info">
                    <div className="item-name">{item.name}</div>
                    <div className="item-quantity">x{item.quantity}</div>
                  </div>
                  <div className="item-price">€{(item.price * item.quantity).toFixed(2)}</div>
                </div>
              ))}
            </div>

            <div className="summary-totals">
              <div className="total-row">
                <span>Subtotale</span>
                <span>€{order.subtotal.toFixed(2)}</span>
              </div>
              <div className="total-row">
                <span>Spedizione</span>
                <span>{order.shipping === 0 ? 'GRATIS' : `€${order.shipping.toFixed(2)}`}</span>
              </div>
              <div className="total-row final">
                <span>Totale</span>
                <span>€{order.total.toFixed(2)}</span>
              </div>
            </div>
          </div>

          <div className="shipping-info">
            <h3>Indirizzo di Spedizione</h3>
            <p><strong>{order.shipping.fullName}</strong></p>
            <p>{order.shipping.address}</p>
            <p>{order.shipping.city}, {order.shipping.postalCode}</p>
            <p>{order.shipping.phone}</p>
          </div>

          <div className="actions">
            <Link to="/products" className="btn-secondary">
              Continua lo Shopping
            </Link>
            <Link to="/profile" className="btn-primary">
              Vai ai Miei Ordini
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderConfirmationPage;
