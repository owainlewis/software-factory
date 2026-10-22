from conftest import contact, deal
def test_timeline(api):
    c = contact(api)
    d = deal(api, contact_id=c["id"])
    api.post("/api/activities", json={"type": "note", "body": "first", "contact_id": c["id"], "occurred_at": "2026-01-01T10:00:00Z"})
    api.post("/api/activities", json={"type": "call", "body": "second", "deal_id": d["id"], "occurred_at": "2026-02-01T10:00:00Z"})
    other = contact(api)
    api.post("/api/activities", json={"type": "note", "body": "not mine", "contact_id": other["id"]})
    body = api.get(f"/api/contacts/{c['id']}/timeline").json()
    rows = body["items"] if isinstance(body, dict) else body
    assert [a["body"] for a in rows] == ["second", "first"]
