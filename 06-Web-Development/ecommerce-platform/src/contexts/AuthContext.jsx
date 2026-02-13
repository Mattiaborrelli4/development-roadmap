import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Carica l'utente dal localStorage
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Errore nel caricamento dell\'utente:', error);
      }
    }
    setIsLoading(false);
  }, []);

  const login = (email, password) => {
    // Simulazione del login
    // In produzione, questo verrebbe da un API
    const mockUser = {
      id: 1,
      email: email,
      name: email.split('@')[0],
      fullName: 'Mario Rossi',
      address: 'Via Roma 123, 00100 Roma',
      phone: '+39 333 1234567',
      createdAt: new Date().toISOString()
    };

    setUser(mockUser);
    setIsAuthenticated(true);
    localStorage.setItem('user', JSON.stringify(mockUser));

    return { success: true, user: mockUser };
  };

  const register = (userData) => {
    // Simulazione della registrazione
    const mockUser = {
      id: Date.now(),
      email: userData.email,
      name: userData.name,
      fullName: `${userData.name} ${userData.surname}`,
      address: '',
      phone: '',
      createdAt: new Date().toISOString()
    };

    setUser(mockUser);
    setIsAuthenticated(true);
    localStorage.setItem('user', JSON.stringify(mockUser));

    return { success: true, user: mockUser };
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('user');
    localStorage.removeItem('orders');
  };

  const updateProfile = (updates) => {
    const updatedUser = { ...user, ...updates };
    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));
  };

  // Simula il salvataggio degli ordini
  const saveOrder = (orderData) => {
    const orders = JSON.parse(localStorage.getItem('orders') || '[]');
    const newOrder = {
      id: `ORD-${Date.now()}`,
      ...orderData,
      date: new Date().toISOString(),
      status: 'Confermato'
    };
    localStorage.setItem('orders', JSON.stringify([newOrder, ...orders]));
    return newOrder;
  };

  // Recupera gli ordini dell'utente
  const getOrders = () => {
    return JSON.parse(localStorage.getItem('orders') || '[]');
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    updateProfile,
    saveOrder,
    getOrders
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve essere usato all\'interno di AuthProvider');
  }
  return context;
};
