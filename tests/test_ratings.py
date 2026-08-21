def _create_book(client, admin_headers, isbn="978-1-4919-1889-0"):
    payload = {"isbn": isbn, "title": "Designing Data-Intensive Applications", "price": "49.99"}
    resp = client.post("/books/create-book", json=payload, headers=admin_headers)
    assert resp.status_code == 201
    return resp.json()


def test_add_and_update_rating(client, admin_headers, auth_headers):
    book = _create_book(client, admin_headers)

    first = client.post(f"/books/{book['id']}/ratings", json={"rating": 4}, headers=auth_headers)
    assert first.status_code == 200
    assert first.json()["rating"] == 4

    second = client.post(f"/books/{book['id']}/ratings", json={"rating": 5}, headers=auth_headers)
    assert second.status_code == 200
    assert second.json()["rating"] == 5

    avg = client.get(f"/books/{book['id']}/ratings/average")
    assert avg.status_code == 200
    assert avg.json()["average_rating"] == 5.0


def test_rating_requires_auth(client, admin_headers):
    book = _create_book(client, admin_headers)
    resp = client.post(f"/books/{book['id']}/ratings", json={"rating": 3})
    assert resp.status_code == 401


def test_add_and_list_comments(client, admin_headers, auth_headers):
    book = _create_book(client, admin_headers)

    resp = client.post(
        f"/books/{book['id']}/comments", json={"comment": "Great book!"}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["comment"] == "Great book!"

    listing = client.get(f"/books/{book['id']}/comments")
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_empty_comment_rejected(client, admin_headers, auth_headers):
    book = _create_book(client, admin_headers)
    resp = client.post(f"/books/{book['id']}/comments", json={"comment": "   "}, headers=auth_headers)
    assert resp.status_code == 400
