from conftest import client_for
def test_login_required(app, web):
    anon = client_for(app, follow_redirects=False)
    r = anon.get("/contacts")
    assert r.status_code in (302, 303, 307) and "/login" in r.headers["location"]
    assert anon.get("/login").status_code == 200
    assert web.get("/contacts").status_code == 200
