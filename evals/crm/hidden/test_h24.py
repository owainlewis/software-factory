from conftest import contact, deal
def test_history_kept(api):
    c = contact(api)
    d = deal(api, contact_id=c["id"])
    a = api.post("/api/activities", json={"type": "note", "body": "keep me", "contact_id": c["id"], "deal_id": d["id"]}).json()
    assert api.delete(f"/api/contacts/{c['id']}").status_code == 204
    kept = api.get(f"/api/deals/{d['id']}")
    assert kept.status_code == 200 and kept.json()["contact_id"] is None
    assert api.get(f"/api/activities/{a['id']}").status_code == 200
