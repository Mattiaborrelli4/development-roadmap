import React, { useState } from 'react';
import { useChat } from '../contexts/ChatContext';
import './Login.css';

export default function Login() {
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const { login, loading } = useChat();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!username.trim()) {
      setError('Inserisci un nome utente');
      return;
    }

    if (username.length < 3) {
      setError('Il nome utente deve avere almeno 3 caratteri');
      return;
    }

    try {
      await login(username.trim());
    } catch (err) {
      setError('Errore durante il login. Riprova.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>💬 React Chat</h1>
          <p>Entra nella chat in tempo reale</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Nome utente</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => {
                setUsername(e.target.value);
                setError('');
              }}
              placeholder="Il tuo nome..."
              maxLength={20}
              autoComplete="off"
              autoFocus
            />
            {error && <span className="error-message">{error}</span>}
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Connessione...
              </>
            ) : (
              'Entra in Chat'
            )}
          </button>
        </form>

        <div className="login-footer">
          <p>💡 Suggerimento: Scegli un nome unico!</p>
        </div>
      </div>
    </div>
  );
}
