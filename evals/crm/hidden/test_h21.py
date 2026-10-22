from conftest import contact, items
CSV = "first_name,last_name,email,company\nAnn,One,ann@one.com,Initech\nBob,Two,dup@x.com,\nCat,Three,not-an-email,\n"
def test_import(api):
    contact(api, email="dup@x.com")
    r = api.post("/api/contacts/import", files={"file": ("c.csv", CSV, "text/csv")})
    assert r.status_code == 200, r.text
    body = r.json()
    assert (body["created"], body["skipped"]) == (1, 1)
    assert len(body["errors"]) == 1 and body["errors"][0]["row"]
    found = [c for c in items(api.get("/api/contacts", params={"limit": 200})) if c["email"] == "ann@one.com"]
    assert found and found[0]["company_id"]
