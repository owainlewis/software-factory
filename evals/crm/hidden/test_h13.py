from conftest import contact, items
def test_tags(api):
    a = contact(api)
    b = contact(api)
    r = api.put(f"/api/contacts/{a['id']}/tags", json=["vip", "churn-risk"])
    assert r.status_code == 200
    assert sorted(api.get(f"/api/contacts/{a['id']}").json()["tags"]) == ["churn-risk", "vip"]
    assert [c["id"] for c in items(api.get("/api/contacts", params={"tag": "vip"}))] == [a["id"]]
