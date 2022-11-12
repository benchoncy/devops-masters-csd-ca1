import pytest
from bpcalc import validate_values, get_bp_category, BPCategory


def test_validate_values():
    assert validate_values(100, 80) is None
    assert validate_values(80, 100) is not None
    assert validate_values(60, 50) is not None
    assert validate_values(80, 110) is not None
    assert validate_values(50, 150) is not None


def test_get_bp_category():
    assert get_bp_category(80, 50) == BPCategory.LOW
    assert get_bp_category(110, 70) == BPCategory.IDEAL
    assert get_bp_category(130, 80) == BPCategory.PRE_HIGH
    assert get_bp_category(160, 90) == BPCategory.HIGH
    assert get_bp_category(90, 60) == BPCategory.IDEAL
    assert get_bp_category(90, 50) == BPCategory.IDEAL