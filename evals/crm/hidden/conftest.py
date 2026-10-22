"""Shared fixtures for the hidden CRM tests.

They work at every stage of the build: before and after accounts exist,
and before and after list endpoints return {"items", "total"}.
"""

import uuid

import pytest
from fastapi.testclient import TestClient

from crm.main import create_app


def client_for(app, **kwargs):
    """A TestClient with the app's startup hooks run, like a real server."""
    client = TestClient(app, **kwargs)
    client.__enter__()
    return client


@pytest.fixture
def app(tmp_path):
    return create_app(str(tmp_path / "crm.db"))


def _register_and_login(client):
    email = f"user-{uuid.uuid4().hex[:8]}@example.com"
    password = "correct horse battery staple"
    r = client.post("/api/auth/register", json={"email": email, "password": password})
    if r.status_code in (404, 405):
        return None
    assert r.status_code in (200, 201), r.text
    token = client.post("/api/auth/login", json={"email": email, "password": password}).json()["token"]
    return email, password, token


@pytest.fixture
def api(app):
    """A JSON API client, signed in if the app has accounts."""
    client = client_for(app)
    creds = _register_and_login(client)
    if creds:
        client.headers["Authorization"] = f"Bearer {creds[2]}"
        client.user_email = creds[0]
    return client


@pytest.fixture
def web(app):
    """A browser-like client, signed in to the web pages if they need it."""
    client = client_for(app, follow_redirects=True)
    creds = _register_and_login(client)
    if creds:
        client.headers["Authorization"] = f"Bearer {creds[2]}"
        page = client.get("/login")
        if page.status_code == 200:
            client.post("/login", data={"email": creds[0], "password": creds[1]})
    return client


def items(response):
    """The records in a list response, whatever its shape."""
    body = response.json()
    return body["items"] if isinstance(body, dict) else body


def contact(api, **fields):
    data = {"first_name": "Ada", "last_name": "Lovelace", "email": f"{uuid.uuid4().hex[:8]}@example.com"}
    data.update(fields)
    r = api.post("/api/contacts", json=data)
    assert r.status_code == 201, r.text
    return r.json()


def company(api, **fields):
    data = {"name": f"Co {uuid.uuid4().hex[:6]}"}
    data.update(fields)
    r = api.post("/api/companies", json=data)
    assert r.status_code == 201, r.text
    return r.json()


def deal(api, **fields):
    data = {"title": "Deal", "value": 1000}
    data.update(fields)
    r = api.post("/api/deals", json=data)
    assert r.status_code == 201, r.text
    return r.json()
