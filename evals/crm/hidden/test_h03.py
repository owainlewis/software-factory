from conftest import contact
def test_pagination(api):
    for name in ["Cole", "Adams", "Baker"]:
        contact(api, last_name=name)
    body = api.get("/api/contacts", params={"limit": 2, "sort": "last_name"}).json()
    assert body["total"] == 3
    assert [c["last_name"] for c in body["items"]] == ["Adams", "Baker"]
    body = api.get("/api/contacts", params={"limit": 2, "offset": 2, "sort": "last_name"}).json()
    assert [c["last_name"] for c in body["items"]] == ["Cole"]
    newest = api.get("/api/contacts", params={"sort": "created_at"}).json()["items"]
    assert newest[0]["last_name"] == "Baker"
