import React from 'react';
import Cart from '../components/Cart';
import './CartPage.css';

const CartPage = () => {
  return (
    <div className="cart-page-wrapper">
      <div className="container">
        <h1>Il Tuo Carrello</h1>
        <Cart isPage={true} />
      </div>
    </div>
  );
};

export default CartPage;
