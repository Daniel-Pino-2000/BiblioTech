import { apiRequest } from "./client";
import type { Wishlist, WishlistItem } from "./types";

export function getUserWishlists(userId: number) {
  return apiRequest<Wishlist[]>(`/wishlist/user/${userId}`, { auth: true });
}

export function createWishlist(name: string) {
  return apiRequest<Wishlist>("/wishlist/", { method: "POST", body: { name }, auth: true });
}

export function getWishlistItems(wishlistId: number) {
  return apiRequest<WishlistItem[]>(`/wishlist/${wishlistId}`, { auth: true });
}

export function addBookToWishlist(wishlistId: number, bookId: number) {
  return apiRequest<WishlistItem>("/wishlist/items", {
    method: "POST",
    body: { wishlist_id: wishlistId, book_id: bookId },
    auth: true,
  });
}

export function removeBookFromWishlist(wishlistId: number, bookId: number) {
  return apiRequest<{ message: string }>(`/wishlist/${wishlistId}/items/${bookId}`, {
    method: "DELETE",
    auth: true,
  });
}
