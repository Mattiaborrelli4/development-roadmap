// cart.js - Gestione stato carrello, localStorage e reduce

// Chiave per localStorage
const CART_STORAGE_KEY = 'shopping_cart';

// Stato iniziale del carrello
let cart = [];

/**
 * Carica il carrello dal localStorage
 */
const loadCartFromStorage = () => {
  try {
    const savedCart = localStorage.getItem(CART_STORAGE_KEY);
    if (savedCart) {
      cart = JSON.parse(savedCart);
    }
  } catch (error) {
    console.error('Errore nel caricamento del carrello:', error);
    cart = [];
  }
};

/**
 * Salva il carrello nel localStorage
 */
const saveCartToStorage = () => {
  try {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
  } catch (error) {
    console.error('Errore nel salvataggio del carrello:', error);
  }
};

/**
 * Aggiunge un prodotto al carrello
 * @param {Object} product - Prodotto da aggiungere
 * @param {number} quantity - Quantità (default: 1)
 */
export const addToCart = (product, quantity = 1) => {
  const existingItemIndex = cart.findIndex(item => item.id === product.id);

  if (existingItemIndex !== -1) {
    // Prodotto già nel carrello, aggiorna la quantità
    cart[existingItemIndex].quantity += quantity;
  } else {
    // Nuovo prodotto, usa spread operator per creare oggetto
    cart.push({
      ...product,
      quantity
    });
  }

  saveCartToStorage();
  updateCartUI();
  showNotification(`${product.name} aggiunto al carrello!`);
};

/**
 * Rimuove un prodotto dal carrello
 * @param {number} productId - ID del prodotto da rimuovere
 */
export const removeFromCart = (productId) => {
  const product = cart.find(item => item.id === productId);
  cart = cart.filter(item => item.id !== productId);
  saveCartToStorage();
  updateCartUI();
  if (product) {
    showNotification(`${product.name} rimosso dal carrello`);
  }
};

/**
 * Aggiorna la quantità di un prodotto nel carrello
 * @param {number} productId - ID del prodotto
 * @param {number} change - Cambiamento quantità (+1 o -1)
 */
export const updateQuantity = (productId, change) => {
  const itemIndex = cart.findIndex(item => item.id === productId);

  if (itemIndex !== -1) {
    const newQuantity = cart[itemIndex].quantity + change;

    if (newQuantity <= 0) {
      // Se la quantità va a 0, rimuovi il prodotto
      removeFromCart(productId);
    } else {
      cart[itemIndex].quantity = newQuantity;
      saveCartToStorage();
      updateCartUI();
    }
  }
};

/**
 * Calcola il totale del carrello usando reduce
 * @returns {number} Totale del carrello
 */
export const calculateTotal = () => {
  return cart.reduce((total, item) => {
    return total + (item.price * item.quantity);
  }, 0);
};

/**
 * Calcola il numero totale di articoli nel carrello
 * @returns {number} Numero totale di articoli
 */
export const getTotalItems = () => {
  return cart.reduce((total, item) => {
    return total + item.quantity;
  }, 0);
};

/**
 * Svuota completamente il carrello
 */
export const clearCart = () => {
  cart = [];
  saveCartToStorage();
  updateCartUI();
  showNotification('Carrello svuotato');
};

/**
 * Ottieni il carrello corrente
 * @returns {Array} Array con gli elementi del carrello
 */
export const getCart = () => {
  return [...cart];
};

/**
 * Formatta il prezzo in Euro
 * @param {number} price - Prezzo da formattare
 * @returns {string} Prezzo formattato
 */
export const formatPrice = (price) => {
  return new Intl.NumberFormat('it-IT', {
    style: 'currency',
    currency: 'EUR'
  }).format(price);
};

/**
 * Mostra una notifica
 * @param {string} message - Messaggio da mostrare
 */
const showNotification = (message) => {
  const notification = document.getElementById('notification');
  if (notification) {
    notification.textContent = message;
    notification.classList.add('show');

    setTimeout(() => {
      notification.classList.remove('show');
    }, 3000);
  }
};

/**
 * Aggiorna l'interfaccia del carrello
 */
const updateCartUI = () => {
  // Aggiorna contatore carrello
  const cartCount = document.getElementById('cart-count');
  if (cartCount) {
    const totalItems = getTotalItems();
    cartCount.textContent = totalItems;
    cartCount.classList.toggle('hidden', totalItems === 0);
  }

  // Aggiorna lista prodotti nel carrello
  const cartItems = document.getElementById('cart-items');
  if (cartItems) {
    if (cart.length === 0) {
      cartItems.innerHTML = `
        <div class="empty-cart">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
          <p>Il tuo carrello è vuoto</p>
        </div>
      `;
    } else {
      cartItems.innerHTML = cart.map(item => `
        <div class="cart-item" data-id="${item.id}">
          <img src="${item.image}" alt="${item.name}" class="cart-item-image">
          <div class="cart-item-details">
            <h4>${item.name}</h4>
            <p class="cart-item-price">${formatPrice(item.price)}</p>
          </div>
          <div class="cart-item-actions">
            <div class="quantity-controls">
              <button class="quantity-btn minus" onclick="window.handleQuantityChange(${item.id}, -1)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
              <span class="quantity">${item.quantity}</span>
              <button class="quantity-btn plus" onclick="window.handleQuantityChange(${item.id}, 1)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
            </div>
            <button class="remove-btn" onclick="window.handleRemoveFromCart(${item.id})">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        </div>
      `).join('');
    }
  }

  // Aggiorna totale
  const cartTotal = document.getElementById('cart-total');
  if (cartTotal) {
    cartTotal.textContent = formatPrice(calculateTotal());
  }

  // Aggiorna stato pulsante checkout
  const checkoutBtn = document.getElementById('checkout-btn');
  if (checkoutBtn) {
    checkoutBtn.disabled = cart.length === 0;
  }
};

/**
 * Gestisce il cambio di quantità
 */
window.handleQuantityChange = (productId, change) => {
  updateQuantity(productId, change);
};

/**
 * Gestisce la rimozione dal carrello
 */
window.handleRemoveFromCart = (productId) => {
  removeFromCart(productId);
};

/**
 * Processa il checkout
 */
export const processCheckout = (formData) => {
  // Validazione del form
  const errors = validateCheckoutForm(formData);

  if (errors.length > 0) {
    return {
      success: false,
      errors
    };
  }

  // Simula elaborazione ordine
  const order = {
    id: generateOrderId(),
    items: [...cart],
    total: calculateTotal(),
    customer: {
      name: formData.get('name'),
      email: formData.get('email'),
      address: formData.get('address'),
      city: formData.get('city'),
      zip: formData.get('zip')
    },
    date: new Date().toISOString()
  };

  // Salva ordine in localStorage (storico)
  saveOrder(order);

  // Svuota il carrello
  clearCart();

  return {
    success: true,
    order
  };
};

/**
 * Valida il form di checkout
 */
const validateCheckoutForm = (formData) => {
  const errors = [];
  const requiredFields = ['name', 'email', 'address', 'city', 'zip'];

  requiredFields.forEach(field => {
    const value = formData.get(field);
    if (!value || value.trim() === '') {
      errors.push({
        field,
        message: `Il campo ${field} è obbligatorio`
      });
    }
  });

  // Validazione email
  const email = formData.get('email');
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (email && !emailRegex.test(email)) {
    errors.push({
      field: 'email',
      message: 'Inserisci un indirizzo email valido'
    });
  }

  // Validazione CAP (deve essere numerico)
  const zip = formData.get('zip');
  if (zip && !/^\d{5}$/.test(zip)) {
    errors.push({
      field: 'zip',
      message: 'Il CAP deve essere di 5 cifre'
    });
  }

  return errors;
};

/**
 * Genera un ID ordine univoco
 */
const generateOrderId = () => {
  return 'ORD-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9).toUpperCase();
};

/**
 * Salva un ordine nello storico
 */
const saveOrder = (order) => {
  try {
    const orders = JSON.parse(localStorage.getItem('orders') || '[]');
    orders.push(order);
    localStorage.setItem('orders', JSON.stringify(orders));
  } catch (error) {
    console.error('Errore nel salvataggio dell\'ordine:', error);
  }
};

/**
 * Inizializza il carrello all'avvio
 */
export const initCart = () => {
  loadCartFromStorage();
  updateCartUI();
};
