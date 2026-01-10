import './ShoppingCart.css';

const ShoppingCart = ({ cart }) => {
  if (!cart) {
    return <div className="cart-empty">No shopping cart data available</div>;
  }

  if (!cart.items || cart.items.length === 0) {
    return (
      <div className="cart-empty">
        <p>Your shopping cart is empty</p>
      </div>
    );
  }

  return (
    <div className="shopping-cart">
      <div className="cart-summary">
        <div className="summary-item">
          <span>Total Items:</span>
          <span className="value">{cart.total_items}</span>
        </div>
        <div className="summary-item total">
          <span>Subtotal:</span>
          <span className="value">${cart.subtotal.toFixed(2)}</span>
        </div>
      </div>
      <div className="cart-items">
        {cart.items.map((item, index) => (
          <div key={index} className="cart-item">
            <div className="item-info">
              <h4>{item.title || item.product_id}</h4>
              {item.sku && <p className="item-sku">SKU: {item.sku}</p>}
              {item.size && <p className="item-size">Size: {item.size}</p>}
            </div>
            <div className="item-quantity">
              <span>Qty: {item.quantity}</span>
            </div>
            <div className="item-price">
              ${((item.price || 0) * (item.quantity || 1)).toFixed(2)}
            </div>
          </div>
        ))}
      </div>
      {cart.updated_at && (
        <div className="cart-footer">
          <p>Last updated: {new Date(cart.updated_at).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default ShoppingCart;

