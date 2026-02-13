import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import './Checkout.css';

const Checkout = () => {
  const navigate = useNavigate();
  const { items, getCartTotal, clearCart } = useCart();
  const { user, isAuthenticated, saveOrder } = useAuth();

  const [shippingData, setShippingData] = useState({
    fullName: user?.fullName || '',
    email: user?.email || '',
    address: user?.address || '',
    city: '',
    postalCode: '',
    phone: user?.phone || ''
  });

  const [paymentData, setPaymentData] = useState({
    cardNumber: '',
    cardName: '',
    expiryDate: '',
    cvv: ''
  });

  const [errors, setErrors] = useState({});
  const [isProcessing, setIsProcessing] = useState(false);

  if (items.length === 0) {
    return (
      <div className="checkout-empty">
        <h2>Il tuo carrello è vuoto</h2>
        <button onClick={() => navigate('/products')}>Torna ai prodotti</button>
      </div>
    );
  }

  const subtotal = getCartTotal();
  const shipping = subtotal > 50 ? 0 : 5.99;
  const total = subtotal + shipping;

  const validateShipping = () => {
    const newErrors = {};

    if (!shippingData.fullName.trim()) newErrors.fullName = 'Nome obbligatorio';
    if (!shippingData.email.trim()) newErrors.email = 'Email obbligatoria';
    if (!shippingData.address.trim()) newErrors.address = 'Indirizzo obbligatorio';
    if (!shippingData.city.trim()) newErrors.city = 'Città obbligatoria';
    if (!shippingData.postalCode.trim()) newErrors.postalCode = 'CAP obbligatorio';
    if (!shippingData.phone.trim()) newErrors.phone = 'Telefono obbligatorio';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validatePayment = () => {
    const newErrors = {};

    if (!paymentData.cardNumber.trim()) newErrors.cardNumber = 'Numero carta obbligatorio';
    if (!paymentData.cardName.trim()) newErrors.cardName = 'Nome intestatario obbligatorio';
    if (!paymentData.expiryDate.trim()) newErrors.expiryDate = 'Data scadenza obbligatoria';
    if (!paymentData.cvv.trim()) newErrors.cvv = 'CVV obbligatorio';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateShipping() || !validatePayment()) {
      return;
    }

    setIsProcessing(true);

    // Simula elaborazione pagamento
    await new Promise(resolve => setTimeout(resolve, 2000));

    const orderData = {
      items: items.map(item => ({
        id: item.id,
        name: item.name,
        price: item.price,
        quantity: item.quantity,
        image: item.image
      })),
      subtotal,
      shipping,
      total,
      shipping: shippingData
    };

    const order = saveOrder(orderData);
    clearCart();

    navigate('/order-confirmation', { state: { order } });
  };

  const handleInputChange = (section, field, value) => {
    if (section === 'shipping') {
      setShippingData(prev => ({ ...prev, [field]: value }));
    } else {
      setPaymentData(prev => ({ ...prev, [field]: value }));
    }

    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const formatCardNumber = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = (matches && matches[0]) || '';
    const parts = [];

    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }

    if (parts.length) {
      return parts.join(' ');
    } else {
      return v;
    }
  };

  const formatExpiryDate = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    if (v.length >= 2) {
      return v.substring(0, 2) + '/' + v.substring(2, 4);
    }
    return v;
  };

  return (
    <div className="checkout-container">
      <h1>Checkout</h1>

      <div className="checkout-content">
        {/* Form */}
        <form className="checkout-form" onSubmit={handleSubmit}>
          {/* Spedizione */}
          <section className="checkout-section">
            <h2>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              Indirizzo di Spedizione
            </h2>

            <div className="form-grid">
              <div className="form-group">
                <label>Nome Completo *</label>
                <input
                  type="text"
                  value={shippingData.fullName}
                  onChange={(e) => handleInputChange('shipping', 'fullName', e.target.value)}
                  className={errors.fullName ? 'error' : ''}
                />
                {errors.fullName && <span className="error-message">{errors.fullName}</span>}
              </div>

              <div className="form-group">
                <label>Email *</label>
                <input
                  type="email"
                  value={shippingData.email}
                  onChange={(e) => handleInputChange('shipping', 'email', e.target.value)}
                  className={errors.email ? 'error' : ''}
                />
                {errors.email && <span className="error-message">{errors.email}</span>}
              </div>

              <div className="form-group full-width">
                <label>Indirizzo *</label>
                <input
                  type="text"
                  value={shippingData.address}
                  onChange={(e) => handleInputChange('shipping', 'address', e.target.value)}
                  placeholder="Via, numero civico"
                  className={errors.address ? 'error' : ''}
                />
                {errors.address && <span className="error-message">{errors.address}</span>}
              </div>

              <div className="form-group">
                <label>Città *</label>
                <input
                  type="text"
                  value={shippingData.city}
                  onChange={(e) => handleInputChange('shipping', 'city', e.target.value)}
                  className={errors.city ? 'error' : ''}
                />
                {errors.city && <span className="error-message">{errors.city}</span>}
              </div>

              <div className="form-group">
                <label>CAP *</label>
                <input
                  type="text"
                  value={shippingData.postalCode}
                  onChange={(e) => handleInputChange('shipping', 'postalCode', e.target.value)}
                  className={errors.postalCode ? 'error' : ''}
                />
                {errors.postalCode && <span className="error-message">{errors.postalCode}</span>}
              </div>

              <div className="form-group full-width">
                <label>Telefono *</label>
                <input
                  type="tel"
                  value={shippingData.phone}
                  onChange={(e) => handleInputChange('shipping', 'phone', e.target.value)}
                  className={errors.phone ? 'error' : ''}
                />
                {errors.phone && <span className="error-message">{errors.phone}</span>}
              </div>
            </div>
          </section>

          {/* Pagamento */}
          <section className="checkout-section">
            <h2>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                <line x1="1" y1="10" x2="23" y2="10"></line>
              </svg>
              Pagamento
            </h2>

            <div className="payment-methods">
              <div className="payment-method active">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                  <line x1="1" y1="10" x2="23" y2="10"></line>
                </svg>
                <span>Carta di Credito/Debito</span>
              </div>
            </div>

            <div className="form-grid">
              <div className="form-group full-width">
                <label>Numero Carta *</label>
                <input
                  type="text"
                  value={paymentData.cardNumber}
                  onChange={(e) => handleInputChange('payment', 'cardNumber', formatCardNumber(e.target.value))}
                  placeholder="1234 5678 9012 3456"
                  maxLength="19"
                  className={errors.cardNumber ? 'error' : ''}
                />
                {errors.cardNumber && <span className="error-message">{errors.cardNumber}</span>}
              </div>

              <div className="form-group full-width">
                <label>Nome Intestatario *</label>
                <input
                  type="text"
                  value={paymentData.cardName}
                  onChange={(e) => handleInputChange('payment', 'cardName', e.target.value)}
                  placeholder="MARIO ROSSI"
                  className={errors.cardName ? 'error' : ''}
                />
                {errors.cardName && <span className="error-message">{errors.cardName}</span>}
              </div>

              <div className="form-group">
                <label>Scadenza *</label>
                <input
                  type="text"
                  value={paymentData.expiryDate}
                  onChange={(e) => handleInputChange('payment', 'expiryDate', formatExpiryDate(e.target.value))}
                  placeholder="MM/YY"
                  maxLength="5"
                  className={errors.expiryDate ? 'error' : ''}
                />
                {errors.expiryDate && <span className="error-message">{errors.expiryDate}</span>}
              </div>

              <div className="form-group">
                <label>CVV *</label>
                <input
                  type="text"
                  value={paymentData.cvv}
                  onChange={(e) => handleInputChange('payment', 'cvv', e.target.value.replace(/[^0-9]/g, ''))}
                  placeholder="123"
                  maxLength="4"
                  className={errors.cvv ? 'error' : ''}
                />
                {errors.cvv && <span className="error-message">{errors.cvv}</span>}
              </div>
            </div>

            <div className="security-note">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
              <span>Pagamento sicuro e criptato</span>
            </div>
          </section>

          <button
            type="submit"
            className="place-order-btn"
            disabled={isProcessing}
          >
            {isProcessing ? (
              <>
                <span className="spinner"></span>
                Elaborazione in corso...
              </>
            ) : (
              `€${total.toFixed(2)} - Completa Ordine`
            )}
          </button>
        </form>

        {/* Riepilogo Ordine */}
        <div className="order-summary">
          <h2>Riepilogo Ordine</h2>

          <div className="summary-items">
            {items.map(item => (
              <div key={item.id} className="summary-item">
                <img src={item.image} alt={item.name} />
                <div className="summary-item-info">
                  <div className="summary-item-name">{item.name}</div>
                  <div className="summary-item-quantity">Qty: {item.quantity}</div>
                </div>
                <div className="summary-item-price">€{(item.price * item.quantity).toFixed(2)}</div>
              </div>
            ))}
          </div>

          <div className="summary-totals">
            <div className="summary-row">
              <span>Subtotale</span>
              <span>€{subtotal.toFixed(2)}</span>
            </div>
            <div className="summary-row">
              <span>Spedizione</span>
              <span>{shipping === 0 ? 'GRATIS' : `€${shipping.toFixed(2)}`}</span>
            </div>
            {shipping === 0 && (
              <div className="summary-row free-shipping">
                <span>Hai la spedizione gratuita!</span>
              </div>
            )}
            <div className="summary-row total">
              <span>Totale</span>
              <span>€{total.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
