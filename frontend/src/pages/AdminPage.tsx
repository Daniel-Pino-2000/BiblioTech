import { useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router-dom";
import * as booksApi from "../api/books";
import type { Book } from "../api/types";
import { ApiError } from "../api/client";

const emptyForm = {
  isbn: "",
  title: "",
  description: "",
  price: "",
  genre: "",
  publisher: "",
  year_published: "",
  copies_sold: "",
};

export function AdminPage() {
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState<string | null>(null);
  const [added, setAdded] = useState<Book[]>([]);
  const [submitting, setSubmitting] = useState(false);

  function update<K extends keyof typeof emptyForm>(key: K, value: string) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const book = await booksApi.createBook({
        isbn: form.isbn.trim(),
        title: form.title.trim(),
        description: form.description.trim() || undefined,
        price: form.price,
        genre: form.genre.trim() || undefined,
        publisher: form.publisher.trim() || undefined,
        year_published: form.year_published ? Number(form.year_published) : undefined,
        copies_sold: form.copies_sold ? Number(form.copies_sold) : undefined,
      });
      setAdded((prev) => [book, ...prev]);
      setForm(emptyForm);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to create book");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Add a book</h1>
        <p className="page-subtitle">Admin-only. New books appear in the catalog immediately.</p>
      </div>

      <form className="auth-card admin-form" onSubmit={handleSubmit}>
        <div className="admin-grid">
          <label>
            Title
            <input value={form.title} onChange={(e) => update("title", e.target.value)} required />
          </label>
          <label>
            ISBN
            <input value={form.isbn} onChange={(e) => update("isbn", e.target.value)} required />
          </label>
          <label>
            Price
            <input
              inputMode="decimal"
              value={form.price}
              onChange={(e) => update("price", e.target.value)}
              placeholder="29.99"
              required
            />
          </label>
          <label>
            Genre
            <input value={form.genre} onChange={(e) => update("genre", e.target.value)} />
          </label>
          <label>
            Publisher
            <input value={form.publisher} onChange={(e) => update("publisher", e.target.value)} />
          </label>
          <label>
            Year published
            <input
              inputMode="numeric"
              value={form.year_published}
              onChange={(e) => update("year_published", e.target.value)}
            />
          </label>
        </div>

        <label>
          Description
          <textarea
            value={form.description}
            onChange={(e) => update("description", e.target.value)}
            rows={3}
          />
        </label>

        {error && <div className="form-error">{error}</div>}

        <button className="btn btn-primary" type="submit" disabled={submitting}>
          {submitting ? "Adding..." : "Create book"}
        </button>
      </form>

      {added.length > 0 && (
        <div className="detail-section">
          <h2>Added this session</h2>
          <ul className="cart-list">
            {added.map((book) => (
              <li key={book.id} className="cart-item">
                <Link to={`/books/${book.isbn}`} className="cart-item-title">
                  {book.title}
                </Link>
                <span className="cart-item-meta">${Number(book.price).toFixed(2)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
