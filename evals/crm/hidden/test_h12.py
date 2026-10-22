from conftest import company, contact, deal
def test_search(api):
    contact(api, first_name="Margaret", last_name="Hamilton", email="mh@apollo.org")
    company(api, name="Apollo Labs", domain="apollo.org")
    deal(api, title="Apollo renewal")
    body = api.get("/api/search", params={"q": "APOLLO"}).json()
    assert len(body["contacts"]) == 1 and len(body["companies"]) == 1 and len(body["deals"]) == 1
    assert api.get("/api/search", params={"q": "hamil"}).json()["contacts"][0]["last_name"] == "Hamilton"
