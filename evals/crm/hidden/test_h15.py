from conftest import contact
def test_pages(api, web):
    c = contact(api, first_name="Evil", last_name="<script>alert(1)</script>")
    api.post("/api/activities", json={"type": "note", "body": "Met at the conference", "contact_id": c["id"]})
    page = web.get("/contacts")
    assert page.status_code == 200 and "text/html" in page.headers["content-type"]
    assert "Evil" in page.text and "<script>alert(1)</script>" not in page.text
    detail = web.get(f"/contacts/{c['id']}")
    assert detail.status_code == 200 and "Met at the conference" in detail.text
