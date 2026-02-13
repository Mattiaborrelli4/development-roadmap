import React, { createContext, useContext, useState, useEffect } from 'react';
import dataService from '../services/dataService';
import storageService from '../services/storageService';

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const currentUser = await dataService.getCurrentUser();
      const savedProfile = await storageService.getProfile();

      setUser(savedProfile || currentUser);
    } catch (error) {
      console.error('Errore nel caricamento utente:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateUser = async (updates) => {
    try {
      const updatedUser = { ...user, ...updates };
      setUser(updatedUser);
      await storageService.saveProfile(updatedUser);
      return updatedUser;
    } catch (error) {
      console.error('Errore aggiornamento utente:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await storageService.clear();
      setUser(null);
    } catch (error) {
      console.error('Errore logout:', error);
      throw error;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        updateUser,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve essere usato dentro AuthProvider');
  }
  return context;
};
