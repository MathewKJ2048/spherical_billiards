import pygame
import math
from conf import *
from board import *

def ellipse(surface,centre,width_ellipse,height_ellipse):
    center_x, center_y = centre
    top_left_x = center_x - width_ellipse // 2
    top_left_y = center_y - height_ellipse // 2
    # Draw an ellipse
    pygame.draw.ellipse(surface, GRID_LINE_COLOR, (top_left_x, top_left_y, width_ellipse, height_ellipse), 2)

def render():
    surface = pygame.Surface((width, height))
    for b in active_balls:
        x = b.r.i
        y = b.r.j
        if b.r.k <= 0:
            pygame.draw.circle(surface, b.color, get_surface_coord(x,y), ball_radius)
    
    pygame.draw.circle(surface, TURF, get_surface_coord(0,0), radius)
    for I in range(GRID_LINES):
        i = I+1
        ellipse(surface,get_surface_coord(0,0),2*radius*i/GRID_LINES,2*radius)
        ellipse(surface,get_surface_coord(0,0),2*radius,2*radius*i/GRID_LINES)

    for b in active_balls:
        x = b.r.i
        y = b.r.j
        if b.r.k > 0:
            pygame.draw.circle(surface, b.color, get_surface_coord(x,y), ball_radius)

    if get_tracer_set():
        for i in range(len(TRACER_POSITIONS)):
            tracer_r = get_striker().r + get_tracer()*(ball_radius+TRACER_POSITIONS[i]*get_power())
            pygame.draw.circle(surface, TRACER, get_surface_coord(tracer_r.i, tracer_r.j), TRACER_RADII[i])
    return surface

def get_surface_coord(x,y):
    return width/2+x, height/2-y