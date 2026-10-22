"""Robustness probes run against both finished apps. Neither arm saw these.

Each test is one probe. The score is how many pass.
"""

from conftest import client_for, company, contact, deal

MANY = "x" * 10_000


def test_duplicate_email_ignores_case(api):
    contact(api, email="Dup@Example.com")
    r = api.post("/api/contacts", json={"first_name": "A", "last_name": "B", "email": "dup@example.com"})
    assert r.status_code == 409


def test_huge_id_is_not_a_server_error(api):
    assert api.get("/api/contacts/99999999999999999999999").status_code in (404, 422)


def test_bad_paging_is_not_a_server_error(api):
    for params in ({"limit": -1}, {"limit": 0}, {"offset": -5}, {"limit": "abc"}):
        assert api.get("/api/contacts", params=params).status_code in (200, 422)


def test_malformed_json_is_422(api):
    r = api.post("/api/contacts", content=b"{not json", headers={"Content-Type": "application/json"})
    assert r.status_code == 422


def test_very_long_name_is_not_a_server_error(api):
    r = api.post("/api/contacts", json={"first_name": MANY, "last_name": "B", "email": "long@example.com"})
    assert r.status_code in (201, 422)


def test_negative_deal_value_rejected(api):
    assert api.post("/api/deals", json={"title": "x", "value": -5}).status_code == 422


def test_bad_activity_date_rejected(api):
    c = contact(api)
    r = api.post("/api/activities", json={"type": "note", "body": "x", "contact_id": c["id"], "occurred_at": "2026-02-30T10:00:00Z"})
    assert r.status_code == 422


def test_timeline_of_missing_contact_is_404(api):
    assert api.get("/api/contacts/987654/timeline").status_code == 404


def test_search_with_sql_text_is_safe(api):
    contact(api, last_name="Visible")
    r = api.get("/api/search", params={"q": "' OR 1=1 --"})
    assert r.status_code == 200
    assert r.json()["contacts"] == []


def test_deal_board_escapes_html(api, web):
    deal(api, title="<img src=x onerror=alert(1)>")
    page = web.get("/deals")
    assert "<img src=x onerror=alert(1)>" not in page.text


def test_contact_page_escapes_company_and_activity(api, web):
    co = company(api, name="<b>Bold Co</b>")
    c = contact(api, company_id=co["id"])
    api.post("/api/activities", json={"type": "note", "body": "<script>x()</script>", "contact_id": c["id"]})
    page = web.get(f"/contacts/{c['id']}").text
    assert "<b>Bold Co</b>" not in page and "<script>x()</script>" not in page


def test_export_needs_auth(app):
    anon = client_for(app)
    assert anon.get("/api/contacts/export").status_code == 401


def test_import_rejects_garbage_cleanly(api):
    r = api.post("/api/contacts/import", files={"file": ("x.csv", b"\xff\xfe\x00garbage\x00", "text/csv")})
    assert r.status_code in (200, 400, 422)


def test_login_does_not_reveal_which_emails_exist(app):
    c = client_for(app)
    c.post("/api/auth/register", json={"email": "known@example.com", "password": "pass-word-123"})
    wrong = c.post("/api/auth/login", json={"email": "known@example.com", "password": "nope-nope-1"})
    unknown = c.post("/api/auth/login", json={"email": "ghost@example.com", "password": "nope-nope-1"})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()


def test_session_cookie_is_httponly(app):
    c = client_for(app, follow_redirects=False)
    c.post("/api/auth/register", json={"email": "cookie@example.com", "password": "pass-word-123"})
    r = c.post("/login", data={"email": "cookie@example.com", "password": "pass-word-123"})
    cookies = [v for k, v in r.headers.multi_items() if k.lower() == "set-cookie"]
    assert cookies and all("httponly" in v.lower() for v in cookies)


def test_login_does_not_redirect_offsite(app):
    c = client_for(app, follow_redirects=False)
    c.post("/api/auth/register", json={"email": "redir@example.com", "password": "pass-word-123"})
    r = c.post("/login?next=https://evil.example.com/", data={"email": "redir@example.com", "password": "pass-word-123", "next": "https://evil.example.com/"})
    assert "evil.example.com" not in r.headers.get("location", "")
