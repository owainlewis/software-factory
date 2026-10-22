from conftest import client_for
def test_health(app):
    r = client_for(app).get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}
