def _create_book(client, admin_headers, isbn="978-1-59-327584-6"):
    payload = {
        "isbn": isbn,
        "title": "The Pragmatic Programmer",
        "price": "34.99",
        "genre": "Software Engineering",
    }
    resp = client.post("/books/create-book", json=payload, headers=admin_headers)
    assert resp.status_code == 201
    return resp.json()


def _my_id(client, headers):
    return client.get("/auth/me", headers=headers).json()["id"]


def test_add_and_list_cart_items(client, admin_headers, auth_headers):
    book = _create_book(client, admin_headers)
    user_id = _my_id(client, auth_headers)

    add_resp = client.post(
        "/cart/add", params={"user_id": user_id, "book_id": book["id"]}, headers=auth_headers
    )
    assert add_resp.status_code == 201

    items_resp = client.get(f"/cart/items/{user_id}", headers=auth_headers)
    assert items_resp.status_code == 200
    body = items_resp.json()
    assert body["items"][0]["book"]["id"] == book["id"]
    assert body["items"][0]["quantity"] == 1


def test_cart_subtotal_reflects_price_and_quantity(client, admin_headers, auth_headers):
    book = _create_book(client, admin_headers)
    user_id = _my_id(client, auth_headers)

    client.post("/cart/add", params={"user_id": user_id, "book_id": book["id"]}, headers=auth_headers)
    client.post("/cart/add", params={"user_id": user_id, "book_id": book["id"]}, headers=auth_headers)

    resp = client.get(f"/cart/subtotal/{user_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert float(resp.json()["subtotal"]) == 69.98


def test_remove_from_cart(client, admin_headers, auth_headers):
    book = _create_book(client, admin_headers)
    user_id = _my_id(client, auth_headers)

    client.post("/cart/add", params={"user_id": user_id, "book_id": book["id"]}, headers=auth_headers)
    remove_resp = client.delete(
        "/cart/remove", params={"user_id": user_id, "book_id": book["id"]}, headers=auth_headers
    )
    assert remove_resp.status_code == 200

    items_resp = client.get(f"/cart/items/{user_id}", headers=auth_headers)
    assert items_resp.json()["items"] == []


def test_cannot_access_another_users_cart(client, admin_headers, auth_headers, make_user):
    bob_headers = make_user("bob")
    user_id = _my_id(client, auth_headers)

    resp = client.get(f"/cart/items/{user_id}", headers=bob_headers)
    assert resp.status_code == 403
