// main.js - Script principale che collega prodotti e carrello

import { products } from './products.js';
import {
  initCart,
  addToCart,
  getCart,
  calculateTotal,
  formatPrice,
  processCheckout
} from './cart.js';

/**
 * Inizializza l'applicazione
 */
const initApp = () => {
  initCart();
  renderProducts();
  setupEventListeners();
};

/**
 * Renderizza la griglia dei prodotti
 */
const renderProducts = () => {
  const productsGrid = document.getElementById('products-grid');

  productsGrid.innerHTML = products.map(product => `
    <article class="product-card">
      <img src="${product.image}" alt="${product.name}" class="product-image">
      <div class="product-info">
        <span class="product-category">${product.category}</span>
        <h3 class="product-name">${product.name}</h3>
        <p class="product-description">${product.description}</p>
        <div class="product-footer">
          <span class="product-price">${formatPrice(product.price)}</span>
          <button class="add-to-cart-btn" onclick="window.handleAddToCart(${product.id})">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
            Aggiungi
          </button>
        </div>
      </div>
    </article>
  `).join('');
};

/**
 * Gestisce l'aggiunta di un prodotto al carrello
 */
window.handleAddToCart = (productId) => {
  const product = products.find(p => p.id === productId);
  if (product) {
    addToCart(product);
  }
};

/**
 * Configura gli event listeners
 */
const setupEventListeners = () => {
  // Toggle carrello
  const cartToggle = document.getElementById('cart-toggle');
  const cartSidebar = document.getElementById('cart-sidebar');
  const overlay = document.getElementById('overlay');
  const closeCart = document.getElementById('close-cart');

  cartToggle.addEventListener('click', () => {
    cartSidebar.classList.add('open');
    overlay.classList.add('active');
  });

  closeCart.addEventListener('click', closeCartSidebar);
  overlay.addEventListener('click', closeCartSidebar);

  // Checkout modal
  const checkoutBtn = document.getElementById('checkout-btn');
  const checkoutModal = document.getElementById('checkout-modal');
  const closeModal = document.getElementById('close-modal');
  const checkoutForm = document.getElementById('checkout-form');

  checkoutBtn.addEventListener('click', openCheckoutModal);
  closeModal.addEventListener('click', () => {
    checkoutModal.classList.remove('active');
    clearFormErrors();
  });

  checkoutForm.addEventListener('submit', handleCheckoutSubmit);

  // Success modal
  const continueShopping = document.getElementById('continue-shopping');
  const successModal = document.getElementById('success-modal');

  continueShopping.addEventListener('click', () => {
    successModal.classList.remove('active');
    overlay.classList.remove('active');
  });

  // Chiudi modali con overlay
  overlay.addEventListener('click', () => {
    checkoutModal.classList.remove('active');
    successModal.classList.remove('active');
  });
};

/**
 * Chiude la sidebar del carrello
 */
const closeCartSidebar = () => {
  const cartSidebar = document.getElementById('cart-sidebar');
  const overlay = document.getElementById('overlay');

  cartSidebar.classList.remove('open');
  overlay.classList.remove('active');
};

/**
 * Apre la modal del checkout
 */
const openCheckoutModal = () => {
  const checkoutModal = document.getElementById('checkout-modal');
  const overlay = document.getElementById('overlay');
  const checkoutItems = document.getElementById('checkout-items');
  const checkoutTotalAmount = document.getElementById('checkout-total-amount');

  // Popola il riepilogo ordine
  const cart = getCart();
  checkoutItems.innerHTML = cart.map(item => `
    <div class="order-summary-item">
      <span>${item.name} × ${item.quantity}</span>
      <span>${formatPrice(item.price * item.quantity)}</span>
    </div>
  `).join('');

  checkoutTotalAmount.textContent = formatPrice(calculateTotal());

  checkoutModal.classList.add('active');
  overlay.classList.add('active');
};

/**
 * Gestisce il submit del form di checkout
 */
const handleCheckoutSubmit = (event) => {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);

  // Pulisci errori precedenti
  clearFormErrors();

  // Processa il checkout
  const result = processCheckout(formData);

  if (result.success) {
    // Mostra modal di successo
    showSuccessModal(result.order);
    form.reset();
  } else {
    // Mostra errori
    displayFormErrors(result.errors);
  }
};

/**
 * Mostra la modal di successo
 */
const showSuccessModal = (order) => {
  const checkoutModal = document.getElementById('checkout-modal');
  const successModal = document.getElementById('success-modal');
  const orderId = document.getElementById('order-id');
  const orderEmail = document.getElementById('order-email');

  orderId.textContent = order.id;
  orderEmail.textContent = order.customer.email;

  checkoutModal.classList.remove('active');
  successModal.classList.add('active');

  // Chiudi la sidebar del carrello
  closeCartSidebar();
};

/**
 * Mostra gli errori del form
 */
const displayFormErrors = (errors) => {
  errors.forEach(error => {
    const errorElement = document.getElementById(`error-${error.field}`);
    const inputElement = document.getElementById(error.field);

    if (errorElement) {
      errorElement.textContent = error.message;
    }

    if (inputElement) {
      inputElement.classList.add('error');
    }
  });
};

/**
 * Pulisci gli errori del form
 */
const clearFormErrors = () => {
  const errorElements = document.querySelectorAll('.error-message');
  const inputElements = document.querySelectorAll('.checkout-form input');

  errorElements.forEach(element => {
    element.textContent = '';
  });

  inputElements.forEach(element => {
    element.classList.remove('error');
  });
};

// Inizializza l'applicazione quando il DOM è caricato
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
