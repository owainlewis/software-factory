from conftest import company, deal, items
def test_deals(api):
    co = company(api)
    d = deal(api, title="Big one", value=500000, company_id=co["id"])
    assert d["stage"] == "lead" and d["currency"] == "USD"
    assert api.patch(f"/api/deals/{d['id']}", json={"stage": "qualified"}).status_code == 200
    q = items(api.get("/api/deals", params={"stage": "qualified"}))
    assert [x["id"] for x in q] == [d["id"]]
    assert api.post("/api/deals", json={"title": "x", "value": 1, "stage": "maybe"}).status_code == 422
