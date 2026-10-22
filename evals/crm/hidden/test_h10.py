from conftest import contact, items
def test_activities(api):
    c = contact(api)
    r = api.post("/api/activities", json={"type": "call", "body": "Intro call", "contact_id": c["id"]})
    assert r.status_code == 201
    a = r.json()
    assert a["occurred_at"]
    assert api.get(f"/api/activities/{a['id']}").json()["body"] == "Intro call"
    assert api.post("/api/activities", json={"type": "note", "body": "orphan"}).status_code == 422
    assert api.post("/api/activities", json={"type": "fax", "body": "x", "contact_id": c["id"]}).status_code == 422
