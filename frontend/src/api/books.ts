import { apiRequest } from "./client";
import type { Book, Comment, Rating } from "./types";

export interface BookCreateInput {
  isbn: string;
  title: string;
  description?: string;
  price: string;
  genre?: string;
  publisher?: string;
  year_published?: number;
  copies_sold?: number;
}

export function listBooks(params: { search?: string; genre?: string; skip?: number; limit?: number }) {
  return apiRequest<Book[]>("/books", { params });
}

export function createBook(data: BookCreateInput) {
  return apiRequest<Book>("/books/create-book", { method: "POST", body: data, auth: true });
}

export function getBookByIsbn(isbn: string) {
  return apiRequest<Book>(`/books/${encodeURIComponent(isbn)}`);
}

export function getTopSellers() {
  return apiRequest<Book[]>("/books/top-sellers");
}

export function getComments(bookId: number) {
  return apiRequest<Comment[]>(`/books/${bookId}/comments`);
}

export function addComment(bookId: number, comment: string) {
  return apiRequest<Comment>(`/books/${bookId}/comments`, {
    method: "POST",
    body: { comment },
    auth: true,
  });
}

export function getAverageRating(bookId: number) {
  return apiRequest<{ book_id: number; average_rating: number }>(`/books/${bookId}/ratings/average`);
}

export function rateBook(bookId: number, rating: number) {
  return apiRequest<Rating>(`/books/${bookId}/ratings`, {
    method: "POST",
    body: { rating },
    auth: true,
  });
}
