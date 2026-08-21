import { apiRequest } from "./client";
import type { Cart } from "./types";

export function getCart(userId: number) {
  return apiRequest<Cart>(`/cart/items/${userId}`, { auth: true });
}

export function getSubtotal(userId: number) {
  return apiRequest<{ user_id: number; subtotal: number }>(`/cart/subtotal/${userId}`, { auth: true });
}

export function addToCart(userId: number, bookId: number) {
  return apiRequest<{ message: string }>("/cart/add", {
    method: "POST",
    auth: true,
    params: { user_id: userId, book_id: bookId },
  });
}

export function removeFromCart(userId: number, bookId: number) {
  return apiRequest<{ message: string }>("/cart/remove", {
    method: "DELETE",
    auth: true,
    params: { user_id: userId, book_id: bookId },
  });
}
