import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import * as cartApi from "../api/cart";
import { useAuth } from "../context/AuthContext";
import type { Cart } from "../api/types";
import { ApiError } from "../api/client";

export function CartPage() {
  const { user } = useAuth();
  const [cart, setCart] = useState<Cart | null>(null);
  const [subtotal, setSubtotal] = useState(0);
  const [error, setError] = useState<string | null>(null);

  function load() {
    if (!user) return;
    Promise.all([cartApi.getCart(user.id), cartApi.getSubtotal(user.id)])
      .then(([c, s]) => {
        setCart(c);
        setSubtotal(s.subtotal);
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : "Failed to load cart"));
  }

  useEffect(load, [user]);

  async function handleRemove(bookId: number) {
    if (!user) return;
    try {
      await cartApi.removeFromCart(user.id, bookId);
      load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to remove item");
    }
  }

  if (!cart) return <div className="page-status">Loading cart...</div>;

  return (
    <div className="page">
      <div className="page-header">
        <h1>Your cart</h1>
      </div>

      {error && <div className="form-error">{error}</div>}

      {cart.items.length === 0 ? (
        <div className="page-status">
          Your cart is empty. <Link to="/">Browse the catalog</Link>.
        </div>
      ) : (
        <>
          <ul className="cart-list">
            {cart.items.map((item) => (
              <li key={item.book.id} className="cart-item">
                <div>
                  <Link to={`/books/${item.book.isbn}`} className="cart-item-title">
                    {item.book.title}
                  </Link>
                  <div className="cart-item-meta">
                    Qty {item.quantity} · ${Number(item.book.price).toFixed(2)} each
                  </div>
                </div>
                <div className="cart-item-actions">
                  <span className="cart-item-line-total">
                    ${(Number(item.book.price) * item.quantity).toFixed(2)}
                  </span>
                  <button className="btn btn-ghost" onClick={() => handleRemove(item.book.id)}>
                    Remove one
                  </button>
                </div>
              </li>
            ))}
          </ul>

          <div className="cart-summary">
            <span>Subtotal</span>
            <span className="cart-subtotal">${Number(subtotal).toFixed(2)}</span>
          </div>
        </>
      )}
    </div>
  );
}
