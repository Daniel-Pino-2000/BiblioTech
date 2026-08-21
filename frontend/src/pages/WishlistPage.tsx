import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router-dom";
import * as wishlistApi from "../api/wishlist";
import { useAuth } from "../context/AuthContext";
import type { Wishlist, WishlistItem } from "../api/types";
import { ApiError } from "../api/client";

export function WishlistPage() {
  const { user } = useAuth();
  const [wishlists, setWishlists] = useState<Wishlist[]>([]);
  const [selected, setSelected] = useState<Wishlist | null>(null);
  const [items, setItems] = useState<WishlistItem[]>([]);
  const [newName, setNewName] = useState("");
  const [error, setError] = useState<string | null>(null);

  function loadWishlists() {
    if (!user) return;
    wishlistApi.getUserWishlists(user.id).then((lists) => {
      setWishlists(lists);
      if (lists.length > 0 && !selected) setSelected(lists[0]);
    });
  }

  useEffect(loadWishlists, [user]);

  useEffect(() => {
    if (!selected) {
      setItems([]);
      return;
    }
    wishlistApi.getWishlistItems(selected.id).then(setItems);
  }, [selected]);

  async function handleCreate(e: FormEvent) {
    e.preventDefault();
    if (!newName.trim()) return;
    setError(null);
    try {
      const created = await wishlistApi.createWishlist(newName);
      setNewName("");
      setWishlists((prev) => [...prev, created]);
      setSelected(created);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to create wishlist");
    }
  }

  async function handleRemove(bookId: number) {
    if (!selected) return;
    try {
      await wishlistApi.removeBookFromWishlist(selected.id, bookId);
      setItems((prev) => prev.filter((i) => i.book_id !== bookId));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to remove item");
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Your wishlists</h1>
      </div>

      <form className="inline-form" onSubmit={handleCreate}>
        <input
          className="search-input"
          placeholder="New wishlist name..."
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <button className="btn btn-primary" type="submit" disabled={wishlists.length >= 3}>
          Create
        </button>
      </form>
      {wishlists.length >= 3 && <p className="page-status">Maximum of 3 wishlists reached.</p>}
      {error && <div className="form-error">{error}</div>}

      {wishlists.length > 0 && (
        <div className="wishlist-tabs">
          {wishlists.map((w) => (
            <button
              key={w.id}
              className={`tab ${selected?.id === w.id ? "active" : ""}`}
              onClick={() => setSelected(w)}
            >
              {w.name}
            </button>
          ))}
        </div>
      )}

      {selected && (
        <ul className="cart-list">
          {items.map((item) => (
            <li key={item.id} className="cart-item">
              <Link to={`/books/${item.book.isbn}`} className="cart-item-title">
                {item.book.title}
              </Link>
              <button className="btn btn-ghost" onClick={() => handleRemove(item.book_id)}>
                Remove
              </button>
            </li>
          ))}
          {items.length === 0 && <li className="page-status">This wishlist is empty.</li>}
        </ul>
      )}
    </div>
  );
}
