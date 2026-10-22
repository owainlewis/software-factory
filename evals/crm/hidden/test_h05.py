from conftest import company, contact, items
def test_link(api):
    co = company(api)
    c = contact(api, company_id=co["id"])
    assert c["company_id"] == co["id"]
    assert [x["id"] for x in items(api.get(f"/api/companies/{co['id']}/contacts"))] == [c["id"]]
    assert api.post("/api/contacts", json={"first_name": "A", "last_name": "B", "email": "x@y.com", "company_id": 99999}).status_code == 422
    api.delete(f"/api/companies/{co['id']}")
    after = api.get(f"/api/contacts/{c['id']}")
    assert after.status_code == 200 and after.json()["company_id"] is None
