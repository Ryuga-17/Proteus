import './PurchaseHistory.css';

const PurchaseHistory = ({ history }) => {
  if (!history) {
    return <div className="history-empty">No purchase history available</div>;
  }

  if (!history.orders || history.orders.length === 0) {
    return (
      <div className="history-empty">
        <p>No past purchases found</p>
      </div>
    );
  }

  return (
    <div className="purchase-history">
      <div className="history-summary">
        <div className="summary-item">
          <span>Total Orders:</span>
          <span className="value">{history.total_orders}</span>
        </div>
        <div className="summary-item total">
          <span>Total Spent:</span>
          <span className="value">${history.total_spent.toFixed(2)}</span>
        </div>
      </div>
      <div className="history-orders">
        {history.orders.map((order) => (
          <div key={order.order_id} className="order-item">
            <div className="order-header">
              <div className="order-id">
                <strong>Order:</strong> {order.order_id}
              </div>
              <span className={`order-status status-${order.status}`}>
                {order.status}
              </span>
            </div>
            <div className="order-date">
              {new Date(order.order_date).toLocaleString()}
            </div>
            <div className="order-items">
              {order.items && order.items.map((item, idx) => (
                <div key={idx} className="order-item-detail">
                  <span>{item.title || item.product_id}</span>
                  <span>Qty: {item.quantity}</span>
                  <span>${(item.price || 0).toFixed(2)}</span>
                </div>
              ))}
            </div>
            <div className="order-total">
              <strong>Total: ${order.total_amount.toFixed(2)}</strong>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PurchaseHistory;

