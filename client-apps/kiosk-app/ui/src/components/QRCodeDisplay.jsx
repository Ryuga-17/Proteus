import { QRCodeSVG } from 'qrcode.react';
import './QRCodeDisplay.css';

const QRCodeDisplay = ({ sessionId }) => {
  const FRONTEND_URL = import.meta.env.VITE_API_URL?.replace(':8001', ':5174') || 'http://localhost:5174';
  const sessionUrl = `${FRONTEND_URL}/kiosk/link?session=${sessionId}`;

  return (
    <div className="qr-container">
      <div className="qr-card">
        <h2>Scan QR Code to Link Session</h2>
        <div className="qr-code-wrapper">
          <QRCodeSVG 
            value={sessionUrl} 
            size={300}
            level="H"
            includeMargin={true}
          />
        </div>
        <div className="qr-info">
          <p className="session-id">Session ID: {sessionId}</p>
          <p className="instruction">
            Scan this QR code with your WhatsApp/device to link your account
          </p>
        </div>
      </div>
    </div>
  );
};

export default QRCodeDisplay;

