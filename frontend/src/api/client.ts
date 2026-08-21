/**
 * Thin fetch wrapper shared by every module in api/*.ts: attaches the JWT
 * (when `auth: true`), serializes JSON or form bodies, builds query strings,
 * and turns a non-2xx response into a typed ApiError with the backend's
 * actual error message instead of a generic "Failed to fetch".
 */
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const TOKEN_KEY = "bibliotech_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function parseError(res: Response): Promise<string> {
  try {
    const body = await res.json();
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) {
      return body.detail.map((d: { msg?: string }) => d.msg).join(", ");
    }
    return res.statusText;
  } catch {
    return res.statusText;
  }
}

interface RequestOptions {
  method?: string;
  body?: unknown;
  auth?: boolean;
  form?: boolean;
  params?: Record<string, string | number | boolean | undefined>;
}

function buildQuery(params?: RequestOptions["params"]): string {
  if (!params) return "";
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") search.set(key, String(value));
  }
  const qs = search.toString();
  return qs ? `?${qs}` : "";
}

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, auth = false, form = false, params } = options;

  const headers: Record<string, string> = {};
  if (body && !form) headers["Content-Type"] = "application/json";
  if (form) headers["Content-Type"] = "application/x-www-form-urlencoded";

  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_URL}${path}${buildQuery(params)}`, {
    method,
    headers,
    body: form ? (body as string) : body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    throw new ApiError(res.status, await parseError(res));
  }

  if (res.status === 204 || res.headers.get("content-length") === "0") {
    return undefined as T;
  }

  return (await res.json()) as T;
}
