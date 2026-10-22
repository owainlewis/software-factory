from conftest import company, contact, deal
def test_summary(api):
    contact(api); company(api)
    deal(api, value=100); deal(api, value=250, stage="proposal")
    deal(api, value=1000, stage="won"); deal(api, value=7, stage="lost")
    s = api.get("/api/reports/summary").json()
    assert s["open_deals"] == 2 and s["open_value"] == 350 and s["won_value_this_month"] == 1000
    assert s["contacts"] >= 1 and s["companies"] >= 1
