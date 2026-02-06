import { useState, useEffect } from 'react';
import { kioskAPI } from '../services/api';
import QRCodeDisplay from './QRCodeDisplay';
import SessionStatus from './SessionStatus';
import ShoppingCart from './ShoppingCart';
import PurchaseHistory from './PurchaseHistory';
import './KioskDashboard.css';

const KioskDashboard = ({ sessionId, onReset }) => {
  const [kioskData, setKioskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [qrData, setQrData] = useState(null);

  useEffect(() => {
    // Start polling for session status
    pollSessionStatus();
    const interval = setInterval(pollSessionStatus, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, [sessionId]);

  const pollSessionStatus = async () => {
    try {
      const data = await kioskAPI.getKioskData(sessionId);
      setKioskData(data);
      setLoading(false);
      setError(null);
    } catch (err) {
      console.error('Error fetching kiosk data:', err);
      setError('Failed to fetch session data');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="kiosk-container">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading kiosk session...</p>
        </div>
      </div>
    );
  }

  const session = kioskData?.session;
  const isLinked = session?.status === 'linked';

  return (
    <div className="kiosk-container">
      <header className="kiosk-header">
        <h1>🛍️ Kiosk System</h1>
        <button onClick={onReset} className="reset-button">
          New Session
        </button>
      </header>

      <div className="kiosk-content">
        {!isLinked ? (
          <div className="qr-section">
            <QRCodeDisplay sessionId={sessionId} />
            <SessionStatus session={session} />
          </div>
        ) : (
          <div className="data-section">
            <div className="session-info">
              <SessionStatus session={session} />
            </div>
            <div className="data-grid">
              <div className="data-panel">
                <h2>🛒 Shopping Cart</h2>
                <ShoppingCart cart={kioskData?.shopping_cart} />
              </div>
              <div className="data-panel">
                <h2>📜 Purchase History</h2>
                <PurchaseHistory history={kioskData?.purchase_history} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default KioskDashboard;

