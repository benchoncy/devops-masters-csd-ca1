import pytest
import re
from bpcalc.bpplot import xlimit, make_plot
from bpcalc.bpenums import BPLimits


@pytest.fixture(scope='module', params=[None, (BPLimits.HIGH_XSTART, BPLimits.IDEAL_YSTART)])
def plot(request):
    return make_plot(request.param)


def test_xlimit():
    half_way_point = ((BPLimits.XMAX - BPLimits.XMIN) / 2) + BPLimits.XMIN
    assert xlimit(BPLimits.XMAX) == 1
    assert xlimit(half_way_point) == 0.5
    assert xlimit(BPLimits.XMIN) == 0


def test_make_plot(plot):
    assert type(plot) is bytes
    assert re.match(b".*PNG.*", plot)
