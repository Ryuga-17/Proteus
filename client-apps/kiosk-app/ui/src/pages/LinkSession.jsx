import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { kioskAPI } from '../services/api';
import './LinkSession.css';

const LinkSession = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const sessionId = searchParams.get('session');
  const [userId, setUserId] = useState('');
  const [linking, setLinking] = useState(false);
  const [linked, setLinked] = useState(false);
  const [error, setError] = useState(null);

  const handleLink = async () => {
    if (!userId.trim()) {
      setError('Please enter your user ID');
      return;
    }

    if (!sessionId) {
      setError('Invalid session');
      return;
    }

    setLinking(true);
    setError(null);

    try {
      await kioskAPI.linkSession(sessionId, userId, {
        user_agent: navigator.userAgent,
        platform: navigator.platform,
      });
      setLinked(true);
      setTimeout(() => {
        // Close or redirect after 3 seconds
        window.close();
      }, 3000);
    } catch (err) {
      console.error('Error linking session:', err);
      setError(err.response?.data?.detail || 'Failed to link session');
      setLinking(false);
    }
  };

  if (!sessionId) {
    return (
      <div className="link-container">
        <div className="link-card error">
          <h2>❌ Invalid Session</h2>
          <p>No session ID provided in the URL.</p>
        </div>
      </div>
    );
  }

  if (linked) {
    return (
      <div className="link-container">
        <div className="link-card success">
          <h2>✅ Session Linked!</h2>
          <p>Your device has been linked to the kiosk session.</p>
          <p className="sub-text">This window will close automatically.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="link-container">
      <div className="link-card">
        <h2>🔗 Link Kiosk Session</h2>
        <p className="instruction">
          Enter your User ID to link this device to the kiosk session.
        </p>
        <div className="session-info">
          <p><strong>Session ID:</strong> {sessionId}</p>
        </div>
        <div className="input-group">
          <label htmlFor="userId">User ID:</label>
          <input
            id="userId"
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="Enter your user ID"
            disabled={linking}
            onKeyPress={(e) => e.key === 'Enter' && handleLink()}
          />
        </div>
        {error && <div className="error-message">{error}</div>}
        <button
          onClick={handleLink}
          disabled={linking || !userId.trim()}
          className="link-button"
        >
          {linking ? 'Linking...' : 'Link Session'}
        </button>
      </div>
    </div>
  );
};

export default LinkSession;

