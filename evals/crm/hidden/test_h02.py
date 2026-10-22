from conftest import contact, items
def test_crud(api):
    c = contact(api, first_name="Grace", last_name="Hopper", email="grace@navy.mil", phone="555")
    assert c["id"] and c["email"] == "grace@navy.mil"
    assert api.get(f"/api/contacts/{c['id']}").json()["last_name"] == "Hopper"
    assert any(x["id"] == c["id"] for x in items(api.get("/api/contacts")))
    r = api.patch(f"/api/contacts/{c['id']}", json={"phone": "999"})
    assert r.status_code == 200 and api.get(f"/api/contacts/{c['id']}").json()["phone"] == "999"
    assert api.delete(f"/api/contacts/{c['id']}").status_code == 204
    assert api.get(f"/api/contacts/{c['id']}").status_code == 404
def test_validation(api):
    contact(api, email="dup@example.com")
    assert api.post("/api/contacts", json={"first_name": "A", "last_name": "B", "email": "dup@example.com"}).status_code == 409
    assert api.post("/api/contacts", json={"first_name": "A", "last_name": "B", "email": "not-an-email"}).status_code == 422
    assert api.post("/api/contacts", json={"first_name": "A", "last_name": "B"}).status_code == 422
