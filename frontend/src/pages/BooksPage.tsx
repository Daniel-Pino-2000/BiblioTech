import { useEffect, useState } from "react";
import { listBooks } from "../api/books";
import { BookCard } from "../components/BookCard";
import type { Book } from "../api/types";
import { ApiError } from "../api/client";

export function BooksPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [search, setSearch] = useState("");
  const [genre, setGenre] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    const handle = setTimeout(() => {
      listBooks({ search: search || undefined, genre: genre || undefined, limit: 40 })
        .then((results) => {
          if (!cancelled) setBooks(results);
        })
        .catch((err) => {
          if (!cancelled) setError(err instanceof ApiError ? err.message : "Failed to load books");
        })
        .finally(() => {
          if (!cancelled) setLoading(false);
        });
    }, 250);

    return () => {
      cancelled = true;
      clearTimeout(handle);
    };
  }, [search, genre]);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Browse the catalog</h1>
        <p className="page-subtitle">Technical books for developers, by developers.</p>
      </div>

      <div className="filters">
        <input
          className="search-input"
          placeholder="Search by title..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <input
          className="search-input"
          placeholder="Filter by genre..."
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
        />
      </div>

      {error && <div className="form-error">{error}</div>}
      {loading && <div className="page-status">Loading books...</div>}
      {!loading && !error && books.length === 0 && (
        <div className="page-status">No books match your search.</div>
      )}

      <div className="book-grid">
        {books.map((book) => (
          <BookCard key={book.id} book={book} />
        ))}
      </div>
    </div>
  );
}
