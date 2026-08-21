import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import * as booksApi from "../api/books";
import * as cartApi from "../api/cart";
import * as wishlistApi from "../api/wishlist";
import { useAuth } from "../context/AuthContext";
import { StarRating } from "../components/StarRating";
import { ApiError } from "../api/client";
import type { Book, Comment, Wishlist } from "../api/types";

export function BookDetailPage() {
  const { isbn } = useParams<{ isbn: string }>();
  const { user } = useAuth();

  const [book, setBook] = useState<Book | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [avgRating, setAvgRating] = useState<number>(0);
  const [myRating, setMyRating] = useState(0);
  const [commentText, setCommentText] = useState("");
  const [wishlists, setWishlists] = useState<Wishlist[]>([]);
  const [selectedWishlist, setSelectedWishlist] = useState<number | "">("");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isbn) return;
    booksApi.getBookByIsbn(isbn).then((b) => {
      setBook(b);
      booksApi.getAverageRating(b.id).then((r) => setAvgRating(r.average_rating));
      booksApi.getComments(b.id).then(setComments);
    });
  }, [isbn]);

  useEffect(() => {
    if (!user) return;
    wishlistApi.getUserWishlists(user.id).then((lists) => {
      setWishlists(lists);
      if (lists.length > 0) setSelectedWishlist(lists[0].id);
    });
  }, [user]);

  async function handleAddToCart() {
    if (!user || !book) return;
    setStatus(null);
    setError(null);
    try {
      await cartApi.addToCart(user.id, book.id);
      setStatus("Added to cart!");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to add to cart");
    }
  }

  async function handleAddToWishlist() {
    if (!book || selectedWishlist === "") return;
    setStatus(null);
    setError(null);
    try {
      await wishlistApi.addBookToWishlist(selectedWishlist, book.id);
      setStatus("Added to wishlist!");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to add to wishlist");
    }
  }

  async function handleRate(rating: number) {
    if (!book) return;
    setMyRating(rating);
    try {
      await booksApi.rateBook(book.id, rating);
      const updated = await booksApi.getAverageRating(book.id);
      setAvgRating(updated.average_rating);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to submit rating");
    }
  }

  async function handleComment(e: React.FormEvent) {
    e.preventDefault();
    if (!book || !commentText.trim()) return;
    try {
      const created = await booksApi.addComment(book.id, commentText);
      setComments((prev) => [created, ...prev]);
      setCommentText("");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to post comment");
    }
  }

  if (!book) return <div className="page-status">Loading...</div>;

  return (
    <div className="page book-detail">
      <div className="book-detail-header">
        <div>
          <div className="book-card-genre">{book.genre || "General"}</div>
          <h1>{book.title}</h1>
          <p className="book-detail-meta">
            {book.publisher} {book.year_published ? `· ${book.year_published}` : ""} · ISBN {book.isbn}
          </p>
          <div className="book-detail-rating">
            <StarRating value={Math.round(avgRating)} />
            <span>{avgRating.toFixed(1)} average</span>
          </div>
        </div>
        <div className="book-detail-buy">
          <div className="book-detail-price">${Number(book.price).toFixed(2)}</div>
          {user ? (
            <button className="btn btn-primary" onClick={handleAddToCart}>
              Add to cart
            </button>
          ) : (
            <Link className="btn btn-primary" to="/login">
              Log in to purchase
            </Link>
          )}
        </div>
      </div>

      {book.description && <p className="book-detail-description">{book.description}</p>}

      {status && <div className="form-success">{status}</div>}
      {error && <div className="form-error">{error}</div>}

      {user && (
        <section className="detail-section">
          <h2>Your rating</h2>
          <StarRating value={myRating} onChange={handleRate} />
        </section>
      )}

      {user && (
        <section className="detail-section">
          <h2>Wishlist</h2>
          {wishlists.length === 0 ? (
            <p>
              You don't have a wishlist yet. <Link to="/wishlist">Create one</Link>.
            </p>
          ) : (
            <div className="wishlist-add-row">
              <select
                value={selectedWishlist}
                onChange={(e) => setSelectedWishlist(Number(e.target.value))}
              >
                {wishlists.map((w) => (
                  <option key={w.id} value={w.id}>
                    {w.name}
                  </option>
                ))}
              </select>
              <button className="btn btn-ghost" onClick={handleAddToWishlist}>
                Add to wishlist
              </button>
            </div>
          )}
        </section>
      )}

      <section className="detail-section">
        <h2>Comments</h2>
        {user && (
          <form className="comment-form" onSubmit={handleComment}>
            <textarea
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              placeholder="Share your thoughts on this book..."
              rows={3}
            />
            <button className="btn btn-primary" type="submit">
              Post comment
            </button>
          </form>
        )}
        <ul className="comment-list">
          {comments.map((c) => (
            <li key={c.id} className="comment-item">
              <p>{c.comment}</p>
              <span className="comment-meta">{new Date(c.created_at).toLocaleDateString()}</span>
            </li>
          ))}
          {comments.length === 0 && <p className="page-status">No comments yet.</p>}
        </ul>
      </section>
    </div>
  );
}
