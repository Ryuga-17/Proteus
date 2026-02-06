import { useState, useEffect } from 'react';
import KioskDashboard from './components/KioskDashboard';
import './App.css';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Generate QR session on mount
    generateSession();
  }, []);

  const generateSession = async () => {
    try {
      const { kioskAPI } = await import('./services/api');
      const response = await kioskAPI.generateQRSession();
      setSessionId(response.session_id);
      setError(null);
    } catch (err) {
      console.error('Error generating session:', err);
      setError('Failed to generate QR session. Please refresh the page.');
    }
  };

  if (error) {
    return (
      <div className="error-container">
        <div className="error-message">{error}</div>
        <button onClick={generateSession} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  if (!sessionId) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Initializing kiosk session...</p>
      </div>
    );
  }

  return <KioskDashboard sessionId={sessionId} onReset={generateSession} />;
}

export default App;

