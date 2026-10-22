from conftest import contact
def test_email_case(api):
    contact(api, email="Alice@Acme.com")
    assert len(api.get("/api/search", params={"q": "alice@acme.com"}).json()["contacts"]) == 1
