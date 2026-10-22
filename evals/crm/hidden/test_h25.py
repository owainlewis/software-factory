from conftest import client_for, deal
def test_dashboard(app, api, web):
    deal(api, value=4242)
    page = web.get("/")
    assert page.status_code == 200 and ("4242" in page.text or "42.42" in page.text)
    r = client_for(app, follow_redirects=False).get("/")
    assert r.status_code in (302, 303, 307)
