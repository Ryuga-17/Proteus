import './SessionStatus.css';

const SessionStatus = ({ session }) => {
  if (!session) {
    return <div className="session-status">Loading session status...</div>;
  }

  const statusColors = {
    pending: '#ffa500',
    linked: '#4caf50',
    expired: '#f44336',
  };

  const statusLabels = {
    pending: '⏳ Waiting for QR Scan',
    linked: '✅ Session Linked',
    expired: '❌ Session Expired',
  };

  return (
    <div className="session-status">
      <div className="status-header">
        <h3>Session Status</h3>
        <span 
          className="status-badge" 
          style={{ backgroundColor: statusColors[session.status] || '#666' }}
        >
          {statusLabels[session.status] || session.status}
        </span>
      </div>
      {session.user_id && (
        <div className="session-details">
          <p><strong>User ID:</strong> {session.user_id}</p>
          {session.linked_at && (
            <p><strong>Linked At:</strong> {new Date(session.linked_at).toLocaleString()}</p>
          )}
          <p><strong>Expires At:</strong> {new Date(session.expires_at).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default SessionStatus;

