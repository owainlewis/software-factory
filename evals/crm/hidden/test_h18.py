from conftest import client_for
import sqlite3
def test_auth(app, tmp_path):
    c = client_for(app)
    assert c.post("/api/auth/register", json={"email": "a@b.com", "password": "s3cret-pass-123"}).status_code == 201
    assert c.post("/api/auth/register", json={"email": "a@b.com", "password": "other-pass-456"}).status_code == 409
    assert c.post("/api/auth/login", json={"email": "a@b.com", "password": "wrong"}).status_code == 401
    token = c.post("/api/auth/login", json={"email": "a@b.com", "password": "s3cret-pass-123"}).json()["token"]
    assert c.get("/api/contacts").status_code == 401
    assert c.get("/api/contacts", headers={"Authorization": f"Bearer {token}"}).status_code == 200
    assert c.get("/health").status_code == 200
    dump = "\n".join(sqlite3.connect(tmp_path / "crm.db").iterdump())
    assert "s3cret-pass-123" not in dump
