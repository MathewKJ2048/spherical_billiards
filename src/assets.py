# all cosmetic stuff
from conf import *

BACKGROUND = (0,0,0)
TURF = (0,150,0)
WHITE = (255,255,255)
RED = (190,0,0)
BLUE = (0,0,190)

TRACER = (200,200,0)
HOLE = (150,0,150)

BORDER_WIDTH = 2

def get_border(color):
    if color == HOLE:
        return WHITE
    r, g, b = color
    f = 0.5
    return (r*f,g*f,b*f)