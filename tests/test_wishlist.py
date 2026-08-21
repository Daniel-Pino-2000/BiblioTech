def _create_book(client, admin_headers, isbn="978-0-596-00712-6"):
    payload = {"isbn": isbn, "title": "Head First Design Patterns", "price": "44.99"}
    resp = client.post("/books/create-book", json=payload, headers=admin_headers)
    assert resp.status_code == 201
    return resp.json()


def test_create_wishlist(client, auth_headers):
    resp = client.post("/wishlist/", json={"name": "Summer Reading"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Summer Reading"


def test_create_wishlist_empty_name_rejected(client, auth_headers):
    resp = client.post("/wishlist/", json={"name": "   "}, headers=auth_headers)
    assert resp.status_code == 400


def test_max_three_wishlists(client, auth_headers):
    for i in range(3):
        resp = client.post("/wishlist/", json={"name": f"List {i}"}, headers=auth_headers)
        assert resp.status_code == 200

    resp = client.post("/wishlist/", json={"name": "One Too Many"}, headers=auth_headers)
    assert resp.status_code == 400


def test_add_book_to_wishlist(client, admin_headers, auth_headers):
    book = _create_book(client, admin_headers)
    wishlist = client.post("/wishlist/", json={"name": "To Read"}, headers=auth_headers).json()

    resp = client.post(
        "/wishlist/items",
        json={"wishlist_id": wishlist["id"], "book_id": book["id"]},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["book_id"] == book["id"]

    duplicate = client.post(
        "/wishlist/items",
        json={"wishlist_id": wishlist["id"], "book_id": book["id"]},
        headers=auth_headers,
    )
    assert duplicate.status_code == 400


def test_cannot_add_to_another_users_wishlist(client, admin_headers, auth_headers, make_user):
    book = _create_book(client, admin_headers)
    wishlist = client.post("/wishlist/", json={"name": "To Read"}, headers=auth_headers).json()

    bob_headers = make_user("bob")
    resp = client.post(
        "/wishlist/items",
        json={"wishlist_id": wishlist["id"], "book_id": book["id"]},
        headers=bob_headers,
    )
    assert resp.status_code == 403


def test_remove_book_from_wishlist(client, admin_headers, auth_headers):
    book = _create_book(client, admin_headers)
    wishlist = client.post("/wishlist/", json={"name": "To Read"}, headers=auth_headers).json()
    client.post(
        "/wishlist/items",
        json={"wishlist_id": wishlist["id"], "book_id": book["id"]},
        headers=auth_headers,
    )

    resp = client.delete(f"/wishlist/{wishlist['id']}/items/{book['id']}", headers=auth_headers)
    assert resp.status_code == 200

    items = client.get(f"/wishlist/{wishlist['id']}", headers=auth_headers).json()
    assert items == []
