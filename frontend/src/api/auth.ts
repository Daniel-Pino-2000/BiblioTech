import { apiRequest } from "./client";
import type { Token, User } from "./types";

// POST /auth/login expects OAuth2 form data (username/password), not JSON --
// that's a FastAPI/OAuth2PasswordRequestForm convention, not this app's choice.
export function login(username: string, password: string) {
  const form = new URLSearchParams();
  form.set("username", username);
  form.set("password", password);
  return apiRequest<Token>("/auth/login", { method: "POST", body: form.toString(), form: true });
}

export function register(data: { username: string; password: string; email?: string; name?: string }) {
  return apiRequest<User>("/users", { method: "POST", body: data });
}

export function getCurrentUser() {
  return apiRequest<User>("/auth/me", { auth: true });
}

export function updateProfile(username: string, data: { name?: string; address?: string; password?: string }) {
  return apiRequest<void>(`/users/${encodeURIComponent(username)}`, {
    method: "PATCH",
    body: data,
    auth: true,
  });
}
