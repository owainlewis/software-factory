from conftest import deal
def test_board(api, web):
    deal(api, title="Alpha deal", value=12345)
    deal(api, title="Beta deal", stage="won")
    page = web.get("/deals")
    assert page.status_code == 200
    for word in ["Alpha deal", "Beta deal", "lead", "won"]:
        assert word.lower() in page.text.lower()
