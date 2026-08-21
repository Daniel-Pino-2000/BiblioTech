import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base
from app.api.deps import get_db
from app.main import app
from app.models.user import User
from app.core.security import hash_password

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def _reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def _register_and_login(client, username="alice", password="hunter22", is_admin=False):
    resp = client.post(
        "/users",
        json={"username": username, "password": password, "email": f"{username}@example.com"},
    )
    assert resp.status_code == 201, resp.text

    if is_admin:
        db = TestingSessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            user.is_admin = True
            db.commit()
        finally:
            db.close()

    login_resp = client.post(
        "/auth/login",
        data={"username": username, "password": password},
    )
    assert login_resp.status_code == 200, login_resp.text
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers(client):
    return _register_and_login(client, username="alice", password="hunter2222")


@pytest.fixture
def admin_headers(client):
    return _register_and_login(client, username="admin_user", password="adminpass1", is_admin=True)


@pytest.fixture
def make_user(client):
    def _make(username, password="hunter2222", is_admin=False):
        return _register_and_login(client, username=username, password=password, is_admin=is_admin)

    return _make
