import { Link } from "react-router-dom";
import type { Book } from "../api/types";

export function BookCard({ book }: { book: Book }) {
  return (
    <Link to={`/books/${encodeURIComponent(book.isbn)}`} className="book-card">
      <div className="book-card-genre">{book.genre || "General"}</div>
      <h3 className="book-card-title">{book.title}</h3>
      <div className="book-card-footer">
        <span className="book-card-price">${Number(book.price).toFixed(2)}</span>
        {book.average_rating != null && (
          <span className="book-card-rating">★ {book.average_rating.toFixed(1)}</span>
        )}
      </div>
    </Link>
  );
}
