from enum import Enum

class NodeType(Enum):
    SENSOR = 1
    HIDDEN = 2
    OUT = 3

class ActivationType(Enum):
    SIGMOID = 1
    IDENTITY = 2

def clamp(val, min_val, max_val):
    return min(max(val, min_val), max_val)