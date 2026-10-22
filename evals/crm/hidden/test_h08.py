from conftest import deal
def test_closed(api):
    d = deal(api)
    won = api.patch(f"/api/deals/{d['id']}", json={"stage": "won"}).json()
    assert won["closed_at"]
    assert api.patch(f"/api/deals/{d['id']}", json={"value": 1}).status_code == 409
    reopened = api.patch(f"/api/deals/{d['id']}", json={"stage": "proposal"})
    assert reopened.status_code == 200 and reopened.json()["closed_at"] is None
