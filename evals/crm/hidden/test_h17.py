from conftest import items
def test_form(api, web):
    assert web.get("/contacts/new").status_code == 200
    r = web.post("/contacts/new", data={"first_name": "Form", "last_name": "User", "email": "form@example.com"})
    assert r.status_code == 200 and "Form" in r.text
    assert any(c["email"] == "form@example.com" for c in items(api.get("/api/contacts", params={"limit": 200})))
    bad = web.post("/contacts/new", data={"first_name": "X", "last_name": "Y", "email": "nope"})
    assert bad.status_code in (200, 400, 422) and "email" in bad.text.lower()
