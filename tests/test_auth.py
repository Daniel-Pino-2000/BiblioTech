def test_register_creates_user(client):
    resp = client.post(
        "/users",
        json={"username": "newuser", "password": "supersecret1", "email": "new@example.com"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["username"] == "newuser"
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_duplicate_username_rejected(client):
    payload = {"username": "dupeuser", "password": "supersecret1"}
    first = client.post("/users", json=payload)
    assert first.status_code == 201

    second = client.post("/users", json=payload)
    assert second.status_code == 400


def test_login_success_returns_token(client):
    client.post("/users", json={"username": "loginuser", "password": "correcthorse1"})

    resp = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "correcthorse1"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password_rejected(client):
    client.post("/users", json={"username": "loginuser2", "password": "correcthorse1"})

    resp = client.post(
        "/auth/login",
        data={"username": "loginuser2", "password": "wrongpassword"},
    )
    assert resp.status_code == 401


def test_me_requires_valid_token(client, auth_headers):
    resp = client.get("/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["username"] == "alice"

    unauthenticated = client.get("/auth/me")
    assert unauthenticated.status_code == 401


def test_update_user_requires_self(client, auth_headers, make_user):
    make_user("bob")

    resp = client.patch(
        "/users/bob",
        json={"name": "Hacked Name"},
        headers=auth_headers,
    )
    assert resp.status_code == 403
