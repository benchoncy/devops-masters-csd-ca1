import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from bpcalc.bpenums import BPCategory, BPLimits


def xlimit(cord):
    return (cord - BPLimits.XMIN) / (BPLimits.XMAX - BPLimits.XMIN)


def make_plot(cords=None):
    def label_offset(x):
        return x + 2
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(BPLimits.XMIN, BPLimits.XMAX)
    ax.set_ylim(BPLimits.YMIN, BPLimits.YMAX)
    ax.set_title('Blood Pressure Graph')
    ax.set_xlabel('Diastolic')
    ax.set_ylabel('Systolic')
    ax.annotate(BPCategory.HIGH, (label_offset(BPLimits.XMIN), label_offset(BPLimits.HIGH_YSTART)))
    ax.annotate(BPCategory.PRE_HIGH, (label_offset(BPLimits.XMIN), label_offset(BPLimits.PRE_HIGH_YSTART)))
    ax.annotate(BPCategory.IDEAL, (label_offset(BPLimits.XMIN), label_offset(BPLimits.IDEAL_YSTART)))
    ax.annotate(BPCategory.LOW, (label_offset(BPLimits.XMIN), label_offset(BPLimits.YMIN)))
    ax.axhspan(BPLimits.YMIN, BPLimits.YMAX, xmax=1, facecolor='red', alpha=0.5)
    ax.axhspan(BPLimits.YMIN, BPLimits.HIGH_YSTART, xmax=xlimit(BPLimits.HIGH_XSTART), facecolor='yellow', alpha=0.5)
    ax.axhspan(BPLimits.YMIN, BPLimits.PRE_HIGH_YSTART, xmax=xlimit(BPLimits.PRE_HIGH_XSTART), facecolor='green', alpha=0.5)
    ax.axhspan(BPLimits.YMIN, BPLimits.IDEAL_YSTART, xmax=xlimit(BPLimits.IDEAL_XSTART), facecolor='purple', alpha=0.5)
    if cords:
        ax.plot(cords[0], cords[1], marker="o", markersize=10, markerfacecolor="blue")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output.getvalue()
