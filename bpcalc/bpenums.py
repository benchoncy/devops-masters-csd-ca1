from enum import IntEnum, Enum


class BPCategory(Enum):
    LOW = "low"
    IDEAL = "ideal"
    PRE_HIGH = "pre-high"
    HIGH = "high"

    def __str__(self):
        return self.value


class BPLimits(IntEnum):
    XMIN = 40
    XMAX = 100
    YMIN = 70
    YMAX = 190
    IDEAL_XSTART = 60
    IDEAL_YSTART = 90
    PRE_HIGH_XSTART = 80
    PRE_HIGH_YSTART = 120
    HIGH_XSTART = 90
    HIGH_YSTART = 140
