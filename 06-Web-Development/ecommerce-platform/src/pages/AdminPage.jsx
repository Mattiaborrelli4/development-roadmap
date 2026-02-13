import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import AdminPanel from '../components/AdminPanel';

const AdminPage = () => {
  const { user, isAuthenticated } = useAuth();

  // Check if user is admin
  const isAdmin = isAuthenticated && user?.email === 'admin@shop.com';

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: { pathname: '/admin' }} } />;
  }

  if (!isAdmin) {
    return (
      <div className="admin-access-denied">
        <h2>Accesso Negato</h2>
        <p>Non hai i permessi per accedere a questa pagina.</p>
      </div>
    );
  }

  return <AdminPanel />;
};

export default AdminPage;
