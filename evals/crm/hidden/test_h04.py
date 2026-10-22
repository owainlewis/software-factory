from conftest import company, items
def test_companies(api):
    c = company(api, name="Acme", domain="acme.com")
    assert api.get(f"/api/companies/{c['id']}").json()["domain"] == "acme.com"
    assert api.post("/api/companies", json={"name": "ACME"}).status_code == 409
    assert any(x["id"] == c["id"] for x in items(api.get("/api/companies")))
    assert api.patch(f"/api/companies/{c['id']}", json={"domain": "acme.io"}).status_code == 200
    assert api.delete(f"/api/companies/{c['id']}").status_code == 204
