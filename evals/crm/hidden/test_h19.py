import uuid
from conftest import client_for, items
def login(c):
    email = f"{uuid.uuid4().hex[:6]}@x.com"
    c.post("/api/auth/register", json={"email": email, "password": "pass-word-123"})
    return {"Authorization": "Bearer " + c.post("/api/auth/login", json={"email": email, "password": "pass-word-123"}).json()["token"]}
def test_owner(app):
    c = client_for(app)
    me, you = login(c), login(c)
    mine = c.post("/api/deals", json={"title": "Mine", "value": 1}, headers=me).json()
    c.post("/api/deals", json={"title": "Yours", "value": 1}, headers=you)
    assert mine["owner_id"]
    assert [d["title"] for d in items(c.get("/api/deals", params={"owner": "me"}, headers=me))] == ["Mine"]
