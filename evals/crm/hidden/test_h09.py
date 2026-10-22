from conftest import deal
def test_pipeline(api):
    deal(api, value=100)
    deal(api, value=200)
    deal(api, value=50, stage="won")
    stages = api.get("/api/pipeline").json()["stages"]
    assert [s["stage"] for s in stages] == ["lead", "qualified", "proposal", "won", "lost"]
    by = {s["stage"]: s for s in stages}
    assert (by["lead"]["count"], by["lead"]["value"]) == (2, 300)
    assert (by["won"]["count"], by["won"]["value"]) == (1, 50)
    assert by["lost"]["count"] == 0
