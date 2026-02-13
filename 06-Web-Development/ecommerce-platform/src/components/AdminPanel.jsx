import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { products as initialProducts } from '../data/products';
import './AdminPanel.css';

const AdminPanel = () => {
  const [products, setProducts] = useState(initialProducts);
  const [view, setView] = useState('products'); // products, orders
  const [editingProduct, setEditingProduct] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);

  // Mock orders
  const [orders] = useState([
    {
      id: 'ORD-1234567890',
      date: '2024-01-15T10:30:00Z',
      customer: 'Mario Rossi',
      email: 'mario@email.com',
      items: [
        { id: 1, name: 'Smartphone Pro Max', quantity: 1, price: 899.99 },
        { id: 3, name: 'Cuffie Wireless Premium', quantity: 2, price: 299.99 }
      ],
      total: 1499.97,
      status: 'Confermato',
      shipping: {
        address: 'Via Roma 123',
        city: 'Roma',
        postalCode: '00100'
      }
    },
    {
      id: 'ORD-1234567891',
      date: '2024-01-14T14:20:00Z',
      customer: 'Laura Bianchi',
      email: 'laura@email.com',
      items: [
        { id: 6, name: 'T-Shirt Premium Cotton', quantity: 3, price: 39.99 }
      ],
      total: 119.97,
      status: 'In Spedizione',
      shipping: {
        address: 'Via Milano 45',
        city: 'Milano',
        postalCode: '20100'
      }
    }
  ]);

  const handleDeleteProduct = (productId) => {
    if (window.confirm('Sei sicuro di voler eliminare questo prodotto?')) {
      setProducts(products.filter(p => p.id !== productId));
    }
  };

  const handleEditProduct = (product) => {
    setEditingProduct(product);
    setShowAddModal(true);
  };

  const handleSaveProduct = (productData) => {
    if (editingProduct) {
      setProducts(products.map(p =>
        p.id === editingProduct.id ? { ...productData, id: editingProduct.id } : p
      ));
    } else {
      setProducts([...products, { ...productData, id: Date.now() }]);
    }
    setShowAddModal(false);
    setEditingProduct(null);
  };

  const stats = {
    totalProducts: products.length,
    totalOrders: orders.length,
    totalRevenue: orders.reduce((sum, order) => sum + order.total, 0),
    lowStock: products.filter(p => p.stock < 10).length
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Confermato':
        return '#2ecc71';
      case 'In Spedizione':
        return '#3498db';
      case 'Consegnato':
        return '#9b59b6';
      case 'Annullato':
        return '#e74c3c';
      default:
        return '#95a5a6';
    }
  };

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h1>Pannello Admin</h1>
        <Link to="/" className="back-to-site">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Torna al sito
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon products">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
          </div>
          <div className="stat-info">
            <div className="stat-value">{stats.totalProducts}</div>
            <div className="stat-label">Prodotti</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon orders">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
          </div>
          <div className="stat-info">
            <div className="stat-value">{stats.totalOrders}</div>
            <div className="stat-label">Ordini</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon revenue">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="1" x2="12" y2="23"></line>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
          </div>
          <div className="stat-info">
            <div className="stat-value">€{stats.totalRevenue.toFixed(2)}</div>
            <div className="stat-label">Revenue Totale</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon stock">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </div>
          <div className="stat-info">
            <div className="stat-value">{stats.lowStock}</div>
            <div className="stat-label">Scorte Basse</div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="admin-nav">
        <button
          className={view === 'products' ? 'active' : ''}
          onClick={() => setView('products')}
        >
          Prodotti
        </button>
        <button
          className={view === 'orders' ? 'active' : ''}
          onClick={() => setView('orders')}
        >
          Ordini
        </button>
      </div>

      {/* Products View */}
      {view === 'products' && (
        <div className="admin-section">
          <div className="section-header">
            <h2>Gestione Prodotti</h2>
            <button
              className="btn-primary"
              onClick={() => {
                setEditingProduct(null);
                setShowAddModal(true);
              }}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
              Aggiungi Prodotto
            </button>
          </div>

          <div className="admin-table-container">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Prodotto</th>
                  <th>Categoria</th>
                  <th>Prezzo</th>
                  <th>Stock</th>
                  <th>Azioni</th>
                </tr>
              </thead>
              <tbody>
                {products.map(product => (
                  <tr key={product.id}>
                    <td>
                      <div className="product-cell">
                        <img src={product.image} alt={product.name} />
                        <span>{product.name}</span>
                      </div>
                    </td>
                    <td>{product.category}</td>
                    <td>€{product.price.toFixed(2)}</td>
                    <td>
                      <span className={`stock-badge ${product.stock < 10 ? 'low' : ''}`}>
                        {product.stock}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button
                          className="btn-edit"
                          onClick={() => handleEditProduct(product)}
                          title="Modifica"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                          </svg>
                        </button>
                        <button
                          className="btn-delete"
                          onClick={() => handleDeleteProduct(product.id)}
                          title="Elimina"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Orders View */}
      {view === 'orders' && (
        <div className="admin-section">
          <div className="section-header">
            <h2>Gestione Ordini</h2>
          </div>

          <div className="orders-list">
            {orders.map(order => (
              <div key={order.id} className="order-card">
                <div className="order-header">
                  <div>
                    <h3>Ordine #{order.id}</h3>
                    <p>{new Date(order.date).toLocaleDateString('it-IT')}</p>
                  </div>
                  <div className="order-status" style={{ backgroundColor: getStatusColor(order.status) }}>
                    {order.status}
                  </div>
                </div>

                <div className="order-details">
                  <div className="order-customer">
                    <h4>Cliente</h4>
                    <p><strong>{order.customer}</strong></p>
                    <p>{order.email}</p>
                    <p>{order.shipping.address}, {order.shipping.city} ({order.shipping.postalCode})</p>
                  </div>

                  <div className="order-items">
                    <h4>Prodotti</h4>
                    {order.items.map((item, index) => (
                      <div key={index} className="order-item">
                        <span>{item.name} x{item.quantity}</span>
                        <span>€{(item.price * item.quantity).toFixed(2)}</span>
                      </div>
                    ))}
                  </div>

                  <div className="order-total">
                    <h4>Totale</h4>
                    <p className="total-amount">€{order.total.toFixed(2)}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Add/Edit Product Modal */}
      {showAddModal && (
        <ProductModal
          product={editingProduct}
          onSave={handleSaveProduct}
          onClose={() => {
            setShowAddModal(false);
            setEditingProduct(null);
          }}
        />
      )}
    </div>
  );
};

// Product Modal Component
const ProductModal = ({ product, onSave, onClose }) => {
  const [formData, setFormData] = useState(product || {
    name: '',
    category: 'Elettronica',
    price: '',
    originalPrice: '',
    image: '',
    description: '',
    features: '',
    stock: '',
    featured: false
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    const productData = {
      ...formData,
      price: parseFloat(formData.price),
      originalPrice: parseFloat(formData.originalPrice) || parseFloat(formData.price),
      stock: parseInt(formData.stock),
      features: formData.features.split(',').map(f => f.trim()).filter(f => f),
      rating: product?.rating || 4.5,
      reviews: product?.reviews || 0,
      images: formData.image ? [formData.image] : []
    };

    onSave(productData);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{product ? 'Modifica Prodotto' : 'Aggiungi Prodotto'}</h2>
          <button className="modal-close" onClick={onClose}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="product-form">
          <div className="form-row">
            <div className="form-group">
              <label>Nome Prodotto *</label>
              <input
                type="text"
                value={formData.name}
                onChange={e => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>Categoria *</label>
              <select
                value={formData.category}
                onChange={e => setFormData({ ...formData, category: e.target.value })}
                required
              >
                <option value="Elettronica">Elettronica</option>
                <option value="Abbigliamento">Abbigliamento</option>
                <option value="Casa">Casa</option>
                <option value="Accessori">Accessori</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Prezzo *</label>
              <input
                type="number"
                step="0.01"
                value={formData.price}
                onChange={e => setFormData({ ...formData, price: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>Prezzo Originale</label>
              <input
                type="number"
                step="0.01"
                value={formData.originalPrice}
                onChange={e => setFormData({ ...formData, originalPrice: e.target.value })}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Stock *</label>
              <input
                type="number"
                value={formData.stock}
                onChange={e => setFormData({ ...formData, stock: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>URL Immagine *</label>
              <input
                type="url"
                value={formData.image}
                onChange={e => setFormData({ ...formData, image: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Descrizione</label>
            <textarea
              value={formData.description}
              onChange={e => setFormData({ ...formData, description: e.target.value })}
              rows="3"
            />
          </div>

          <div className="form-group">
            <label>Caratteristiche (separate da virgola)</label>
            <input
              type="text"
              value={formData.features}
              onChange={e => setFormData({ ...formData, features: e.target.value })}
              placeholder="Feature 1, Feature 2, Feature 3"
            />
          </div>

          <div className="form-group checkbox">
            <label>
              <input
                type="checkbox"
                checked={formData.featured}
                onChange={e => setFormData({ ...formData, featured: e.target.checked })}
              />
              Prodotto in evidenza
            </label>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Annulla
            </button>
            <button type="submit" className="btn-primary">
              {product ? 'Salva Modifiche' : 'Aggiungi Prodotto'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdminPanel;
