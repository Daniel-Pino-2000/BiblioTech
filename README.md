# BiblioTech

A full-stack bookstore application for technical books: a FastAPI + MySQL REST API and a
React + TypeScript frontend, with JWT authentication, catalog browsing, ratings/comments,
a shopping cart, and wishlists.

Originally built for **CEN 4010 – Software Engineering**, since hardened into a
production-shaped portfolio project: authenticated/authorized REST API, automated tests,
versioned database migrations, containerized local dev, and CI.

For a from-first-principles walkthrough of how and why this project is built the way it
is — REST design, auth vs. authorization, migrations, testing strategy, a Docker primer,
and a playbook for building something similar yourself — see
[`docs/BiblioTech-Development-Guide.pdf`](docs/BiblioTech-Development-Guide.pdf).

<table>
<tr>
<td width="50%"><img src="docs/screenshots/catalog.jpg" alt="Catalog page"><br><sub>Catalog — search/genre filter</sub></td>
<td width="50%"><img src="docs/screenshots/book-detail.jpg" alt="Book detail page"><br><sub>Book detail — rating, comments</sub></td>
</tr>
<tr>
<td width="50%"><img src="docs/screenshots/cart.jpg" alt="Cart page"><br><sub>Cart — quantity + live subtotal</sub></td>
<td width="50%"><img src="docs/screenshots/wishlist.jpg" alt="Wishlist page"><br><sub>Wishlist</sub></td>
</tr>
<tr>
<td width="50%"><img src="docs/screenshots/admin.jpg" alt="Admin add-a-book page"><br><sub>Admin — add a book</sub></td>
<td width="50%"><img src="docs/screenshots/login.jpg" alt="Login page"><br><sub>Login</sub></td>
</tr>
</table>

---

## Features

- **Catalog** — browse/search books by title and genre, paginated; top sellers; filter by
  minimum rating; admin page for adding books, plus per-publisher discounts via `/docs`.
- **Auth** — registration, JWT login (OAuth2 password flow), bcrypt-hashed passwords, and
  role-based access (regular users vs. admins who manage the catalog).
- **Ratings & comments** — one rating per user per book (create-or-update), threaded
  comments, computed average rating.
- **Shopping cart** — per-user cart with quantity aggregation and live subtotal.
- **Wishlists** — up to 3 named wishlists per user, each holding any number of books.
- **Authorization** — every endpoint that touches a user's data (cart, wishlist, profile,
  ratings, comments) verifies the request is authenticated as that user; catalog mutations
  are admin-only.

---

## Architecture

**Backend** — FastAPI, SQLAlchemy 2.0, MySQL, Alembic migrations, JWT auth (`python-jose` +
`passlib`), pytest.

```text
app/
├── main.py              # FastAPI app, CORS, router registration
├── database.py           # engine/session setup
├── core/
│   └── security.py       # password hashing, JWT encode/decode
├── api/
│   ├── deps.py            # get_db, get_current_user, get_current_admin_user
│   └── routers/           # HTTP layer — request/response handling only
├── services/               # business logic + DB queries
├── models/                  # SQLAlchemy ORM models
└── schemas/                  # Pydantic request/response models
alembic/                        # versioned schema migrations
tests/                            # pytest suite (SQLite, isolated per test)
```

The routers are a thin HTTP layer; business logic and query construction live in
`services/`, which keeps the routers testable and the ORM usage in one place per domain.

**Frontend** — React 19, TypeScript, Vite, React Router. A small typed `api/` client
wraps `fetch`, attaches the JWT from `localStorage`, and normalizes API errors; an
`AuthContext` exposes `login`/`register`/`logout`/`user` to the rest of the app.

```text
frontend/src/
├── api/            # typed fetch client + one module per resource
├── context/         # AuthContext (JWT + current user)
├── components/        # NavBar, BookCard, StarRating, ProtectedRoute
└── pages/               # Catalog, book detail, cart, wishlist, auth, profile
```

---

## Running locally

Backend setup is the same first four steps regardless of path — only the database
differs:

```bash
python -m venv .venv
.venv\Scripts\activate         # .venv/bin/activate on macOS/Linux
pip install -r requirements.txt

cp .env.example .env
```

### Option A — SQLite (fastest, zero external dependencies)

In `.env`, set:

```text
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=dev-secret-change-me
```

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

> **Windows PowerShell note:** if you write `.env` with `echo ... > .env` instead of
> editing it in a text editor, PowerShell's default redirection encoding is UTF-16,
> which `python-dotenv` can't parse and `alembic`/`uvicorn` will fail with a
> `UnicodeDecodeError`. Edit the file directly (or use `Set-Content -Encoding ascii`)
> instead of `echo >`.

### Option B — MySQL (matches production)

Either run MySQL yourself and fill in the `DB_*` values in `.env`, or use Docker Compose
to get both MySQL and the API in one step (migrations run automatically on container
start):

```bash
docker compose up --build
```

API is at `http://localhost:8000` either way; interactive docs at `/docs`.

> Docker Compose wasn't runnable in the environment this project was built in (no local
> Docker install to test against) — the Dockerfile and compose file were written and
> reviewed carefully, but if something's off, it hasn't been verified end-to-end.

### Frontend (either backend option)

```bash
cd frontend
cp .env.example .env.local   # VITE_API_URL defaults to http://localhost:8000, fine for local dev
npm install
npm run dev
```

Visit `http://localhost:5173`.

### Creating an admin user

Catalog writes require `is_admin`: adding a book through the frontend's `/admin` page
(`POST /books/create-book`), plus `PATCH /books/discount` and `POST /authors/create-author`
via `/docs` (there's no in-app UI for those two yet).

There is deliberately no API endpoint for granting admin — it's a privileged action, so it
shouldn't be reachable from the running app at all. Register a normal user, then promote
them with the CLI script instead:

```bash
python scripts/make_admin.py yourusername
```

It runs against whatever database `DATABASE_URL`/`.env` currently points at, so the same
script works locally or against a deployed database (point `DATABASE_URL` at it
temporarily). Once flagged, log back in (or refresh if already logged in) and an **Admin**
link appears in the navbar.

---

## Tests

```bash
pytest
```

The suite runs against an isolated in-memory SQLite database (see `tests/conftest.py`) and
covers auth, authorization boundaries (cross-user access, admin-only routes), the catalog,
cart, wishlist, ratings, and comments — 27 tests, no external services required.

CI (`.github/workflows/ci.yml`) runs the test suite, validates that Alembic migrations
apply cleanly, and builds the frontend on every push/PR to `main`.

---

## Database migrations

Schema changes are managed with Alembic rather than `create_all`:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

---

## Security notes

A few deliberate choices worth calling out, since this project began as a course
assignment where they weren't the default:

- Passwords are bcrypt-hashed (`app/core/security.py`), never stored or returned in plain
  text.
- Credit card numbers are **never persisted in full** — only the last 4 digits are stored,
  matching how real payment UIs display saved cards.
- Every user-scoped endpoint checks that the authenticated user matches the resource
  owner (e.g. you cannot read or modify another user's cart, wishlist, or profile).
- Catalog-mutating endpoints require an admin account, separate from regular users.

---

## Tech stack

| Layer | Tools |
|---|---|
| API | FastAPI, Pydantic v2, Uvicorn |
| ORM / DB | SQLAlchemy 2.0, MySQL, Alembic |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Testing | pytest, httpx, SQLite (test-only) |
| Frontend | React, TypeScript, Vite, React Router |
| Infra | Docker Compose, GitHub Actions |

---

## License

See [LICENSE](LICENSE).
