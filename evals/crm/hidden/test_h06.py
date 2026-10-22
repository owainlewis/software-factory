from conftest import company, contact
def test_domain_link(api):
    acme = company(api, name="Acme", domain="acme.com")
    other = company(api, name="Other")
    assert contact(api, email="pat@acme.com")["company_id"] == acme["id"]
    assert contact(api, email="sam@acme.com", company_id=other["id"])["company_id"] == other["id"]
    assert contact(api, email="lee@elsewhere.com")["company_id"] is None
