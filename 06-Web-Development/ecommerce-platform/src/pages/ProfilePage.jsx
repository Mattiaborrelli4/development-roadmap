import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './ProfilePage.css';

const ProfilePage = () => {
  const { user, logout, updateProfile, getOrders } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('profile');
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    fullName: user?.fullName || '',
    address: user?.address || '',
    phone: user?.phone || ''
  });

  const orders = getOrders();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleSaveProfile = () => {
    updateProfile(editData);
    setIsEditing(false);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('it-IT', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatPrice = (price) => {
    return parseFloat(price).toFixed(2);
  };

  if (!user) {
    return (
      <div className="profile-not-authenticated">
        <h2>Accedi per visualizzare il tuo profilo</h2>
        <button onClick={() => navigate('/login')}>Vai al Login</button>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="container">
        <div className="profile-header">
          <div className="profile-avatar">
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div className="profile-info">
            <h1>{user.fullName || user.name}</h1>
            <p>{user.email}</p>
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            Logout
          </button>
        </div>

        <div className="profile-content">
          {/* Tabs */}
          <div className="profile-tabs">
            <button
              className={`tab ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              Profilo
            </button>
            <button
              className={`tab ${activeTab === 'orders' ? 'active' : ''}`}
              onClick={() => setActiveTab('orders')}
            >
              Ordini
            </button>
          </div>

          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <div className="profile-section">
              <div className="section-header">
                <h2>Informazioni Personali</h2>
                {!isEditing && (
                  <button className="edit-btn" onClick={() => setIsEditing(true)}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                    Modifica
                  </button>
                )}
              </div>

              <div className="info-grid">
                <div className="info-item">
                  <label>Nome Completo</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editData.fullName}
                      onChange={(e) => setEditData({ ...editData, fullName: e.target.value })}
                    />
                  ) : (
                    <span>{user.fullName || '-'}</span>
                  )}
                </div>

                <div className="info-item">
                  <label>Email</label>
                  <span>{user.email}</span>
                </div>

                <div className="info-item">
                  <label>Indirizzo</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editData.address}
                      onChange={(e) => setEditData({ ...editData, address: e.target.value })}
                      placeholder="Via, numero, città"
                    />
                  ) : (
                    <span>{user.address || 'Non specificato'}</span>
                  )}
                </div>

                <div className="info-item">
                  <label>Telefono</label>
                  {isEditing ? (
                    <input
                      type="tel"
                      value={editData.phone}
                      onChange={(e) => setEditData({ ...editData, phone: e.target.value })}
                      placeholder="+39 ..."
                    />
                  ) : (
                    <span>{user.phone || 'Non specificato'}</span>
                  )}
                </div>

                <div className="info-item">
                  <label>Membro dal</label>
                  <span>{formatDate(user.createdAt)}</span>
                </div>
              </div>

              {isEditing && (
                <div className="edit-actions">
                  <button className="btn-secondary" onClick={() => {
                    setIsEditing(false);
                    setEditData({
                      fullName: user?.fullName || '',
                      address: user?.address || '',
                      phone: user?.phone || ''
                    });
                  }}>
                    Annulla
                  </button>
                  <button className="btn-primary" onClick={handleSaveProfile}>
                    Salva Modifiche
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Orders Tab */}
          {activeTab === 'orders' && (
            <div className="profile-section">
              <h2>I Miei Ordini</h2>

              {orders.length === 0 ? (
                <div className="no-orders">
                  <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ddd" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <path d="M16 10a4 4 0 0 1-8 0"></path>
                  </svg>
                  <p>Nessun ordine effettuato</p>
                  <button onClick={() => navigate('/products')} className="btn-primary">
                    Inizia a Fare Shopping
                  </button>
                </div>
              ) : (
                <div className="orders-list">
                  {orders.map(order => (
                    <div key={order.id} className="order-card">
                      <div className="order-header">
                        <div>
                          <h3>Ordine #{order.id}</h3>
                          <p>{formatDate(order.date)}</p>
                        </div>
                        <span className="order-status">{order.status}</span>
                      </div>

                      <div className="order-items">
                        {order.items.map((item, index) => (
                          <div key={index} className="order-item">
                            <img src={item.image} alt={item.name} />
                            <div className="item-details">
                              <div className="item-name">{item.name}</div>
                              <div className="item-quantity">Quantità: {item.quantity}</div>
                            </div>
                            <div className="item-price">€{formatPrice(item.price * item.quantity)}</div>
                          </div>
                        ))}
                      </div>

                      <div className="order-footer">
                        <div className="order-total">
                          <span>Totale:</span>
                          <strong>€{formatPrice(order.total)}</strong>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
