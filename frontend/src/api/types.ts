export interface Book {
  id: number;
  isbn: string;
  title: string;
  description?: string | null;
  price: string;
  genre?: string | null;
  publisher?: string | null;
  year_published?: number | null;
  copies_sold: number;
  author_id?: number | null;
  average_rating?: number | null;
}

export interface User {
  id: number;
  username: string;
  name?: string | null;
  email?: string | null;
  address?: string | null;
  is_admin: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface Comment {
  id: number;
  user_id: number;
  book_id: number;
  comment: string;
  created_at: string;
}

export interface Rating {
  id: number;
  user_id: number;
  book_id: number;
  rating: number;
}

export interface CartItem {
  quantity: number;
  book: Book;
}

export interface Cart {
  user_id: number;
  user_name: string;
  items: CartItem[];
}

export interface Wishlist {
  id: number;
  user_id: number;
  name: string;
}

export interface WishlistItem {
  id: number;
  wishlist_id: number;
  book_id: number;
  book: Book;
}
