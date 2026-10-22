import csv, io
from conftest import company, contact
def test_export(api):
    co = company(api, name="Initech")
    contact(api, first_name="Ann", email="ann@one.com", company_id=co["id"])
    r = api.get("/api/contacts/export")
    assert r.status_code == 200 and "csv" in r.headers["content-type"]
    rows = list(csv.DictReader(io.StringIO(r.text)))
    assert list(rows[0].keys())[:4] == ["first_name", "last_name", "email", "company"]
    assert rows[0]["company"] == "Initech"
