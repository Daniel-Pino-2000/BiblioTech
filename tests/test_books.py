def _create_book(client, headers, isbn="978-0-13-468599-1", **overrides):
    payload = {
        "isbn": isbn,
        "title": "Clean Architecture",
        "description": "A craftsman's guide",
        "price": "39.99",
        "genre": "Software Engineering",
        "publisher": "Prentice Hall",
        "year_published": 2017,
        "copies_sold": 0,
    }
    payload.update(overrides)
    return client.post("/books/create-book", json=payload, headers=headers)


def test_create_book_requires_admin(client, auth_headers):
    resp = _create_book(client, auth_headers)
    assert resp.status_code == 403


def test_create_book_as_admin_succeeds(client, admin_headers):
    resp = _create_book(client, admin_headers)
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Clean Architecture"
    assert body["isbn"] == "978-0-13-468599-1"


def test_get_book_by_isbn_not_found(client):
    resp = client.get("/books/000-0-00-000000-0")
    assert resp.status_code == 404


def test_get_book_by_isbn_found(client, admin_headers):
    _create_book(client, admin_headers)
    resp = client.get("/books/978-0-13-468599-1")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Clean Architecture"


def test_list_books_search_and_pagination(client, admin_headers):
    _create_book(client, admin_headers, isbn="978-0-00-000000-1", title="Clean Code")
    _create_book(client, admin_headers, isbn="978-0-00-000000-2", title="Clean Architecture")
    _create_book(client, admin_headers, isbn="978-0-00-000000-3", title="Refactoring")

    resp = client.get("/books", params={"search": "clean"})
    assert resp.status_code == 200
    titles = {b["title"] for b in resp.json()}
    assert titles == {"Clean Code", "Clean Architecture"}

    limited = client.get("/books", params={"limit": 1})
    assert len(limited.json()) == 1


def test_browse_by_genre(client, admin_headers):
    _create_book(client, admin_headers)
    resp = client.get("/books/genre/Software Engineering")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_discount_requires_admin(client, auth_headers, admin_headers):
    _create_book(client, admin_headers)

    forbidden = client.patch(
        "/books/discount",
        params={"publisher": "Prentice Hall", "discount": 10},
        headers=auth_headers,
    )
    assert forbidden.status_code == 403

    ok = client.patch(
        "/books/discount",
        params={"publisher": "Prentice Hall", "discount": 10},
        headers=admin_headers,
    )
    assert ok.status_code == 200

    book = client.get("/books/978-0-13-468599-1").json()
    assert float(book["price"]) == 35.99
