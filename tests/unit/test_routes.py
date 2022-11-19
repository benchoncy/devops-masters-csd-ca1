import pytest
from bpcalc.bpenums import BPCategory, BPLimits


class TestIndexRoute():
    def test_get(self, client):
        response = client.get("/")
        assert b"BPCalculator" in response.data

    @pytest.mark.parametrize("systolic,diastolic,result", [
        (BPLimits.YMIN, BPLimits.XMIN, BPCategory.LOW),
        (BPLimits.IDEAL_YSTART, BPLimits.IDEAL_XSTART, BPCategory.IDEAL),
        (BPLimits.PRE_HIGH_YSTART, BPLimits.PRE_HIGH_XSTART, BPCategory.PRE_HIGH),
        (BPLimits.HIGH_YSTART, BPLimits.HIGH_XSTART, BPCategory.HIGH)
    ])
    def test_post(self, client, systolic, diastolic, result):
        response = client.post("/", data={
            "bpsystolic": systolic.value,
            "bpdiastolic": diastolic.value
        })
        print(response.data)
        assert str.encode(result.value) in response.data
