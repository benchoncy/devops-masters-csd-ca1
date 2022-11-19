import pytest
from bpcalc import validate_values, get_bp_category
from bpcalc.bpenums import BPCategory, BPLimits


@pytest.mark.parametrize("systolic,diastolic,result", [
    (BPLimits.YMAX, BPLimits.XMAX, type(None)),
    (BPLimits.YMIN, BPLimits.XMIN, type(None)),
    (BPLimits.YMAX + 1, BPLimits.XMAX, list),
    (BPLimits.YMAX, BPLimits.XMAX + 1, list),
    (BPLimits.YMIN - 1, BPLimits.XMIN, list),
    (BPLimits.YMIN, BPLimits.XMIN - 1, list),
    (BPLimits.YMIN, BPLimits.XMAX, list)
])
def test_validate_values(systolic, diastolic, result):
    assert type(validate_values(systolic, diastolic)) is result


@pytest.mark.parametrize("systolic,diastolic,result", [
    (BPLimits.YMIN, BPLimits.XMIN, BPCategory.LOW),
    (BPLimits.IDEAL_YSTART, BPLimits.IDEAL_XSTART, BPCategory.IDEAL),
    (BPLimits.PRE_HIGH_YSTART, BPLimits.PRE_HIGH_XSTART, BPCategory.PRE_HIGH),
    (BPLimits.HIGH_YSTART, BPLimits.HIGH_XSTART, BPCategory.HIGH),
    (BPLimits.YMIN, BPLimits.IDEAL_XSTART, BPCategory.IDEAL),
    (BPLimits.IDEAL_YSTART, BPLimits.XMIN, BPCategory.IDEAL)
])
def test_get_bp_category(systolic, diastolic, result):
    assert get_bp_category(systolic, diastolic) == result
