import pygame
import math
from conf import *
from board import *
from assets import *
from vectors import *

class Sphere:
    def __init__(self,r,radius,color):
        self.r = r
        self.radius = radius
        self.color = color

alpha = 0
beta = 0
gamma = 0
def reset():
    global alpha, beta, gamma
    alpha = 0
    beta = 0
    gamma = 0
def rotate_alpha(invert=False):
    global alpha
    if invert:
        alpha+=CAMERA_SENSITIVITY
    else:
        alpha-=CAMERA_SENSITIVITY

def rotate_beta(invert=False):
    global beta
    if invert:
        beta+=CAMERA_SENSITIVITY
    else:
        beta-=CAMERA_SENSITIVITY

def rotate_gamma(invert=False):
    global gamma
    if invert:
        gamma+=CAMERA_SENSITIVITY
    else:
        gamma-=CAMERA_SENSITIVITY

def render():
    surface = pygame.Surface((width, height))

    spheres = []

    for b in balls:
        color = b.color
        if not b.active:
            color = HOLE
        s = Sphere(shift_position(b.r),ball_radius,color)
        spheres.append(s)
    spheres.append(Sphere(Vector(0,0,0),radius,color=TURF))
    if get_tracer_set():
        for i in range(len(TRACER_POSITIONS)):
            tracer_r = get_striker().r + get_tracer()*(ball_radius+TRACER_POSITIONS[i]*get_power())
            r = shift_position(tracer_r).normalize()*PLANE_RADIUS
            spheres.append(Sphere(r,TRACER_RADII[i],TRACER))
    for i in range(len(hole_positions)):
        hr = hole_positions[i]
        rin = ring(hr,hole_bases[i],NUM_RING,hole_radius, get_time()*SPIN)
        for r in rin:
            spheres.append(Sphere(shift_position((hr+r).normalize()*radius),hole_rotator_radius,HOLE))
    
    def key(s):
        return s.r.k
    spheres = sorted(spheres,key=key)

    for s in spheres:
        pygame.draw.circle(surface, s.color, get_surface_coord(s.r.i,s.r.j), int(s.radius*SCALE))
        pygame.draw.circle(surface, get_border(s.color), get_surface_coord(s.r.i, s.r.j), int(s.radius*SCALE), width=BORDER_WIDTH)


    return surface

def get_surface_coord(x,y):
    return width/2+x*SCALE, height/2-y*SCALE

def rotate(u, v, theta):
    return u*math.cos(theta)-v*math.sin(theta), u*math.sin(theta)+v*math.cos(theta)

def shift_position(r):
    x, y, z = r.i, r.j, r.k
    y, z = rotate(y, z, gamma)
    x, z = rotate(x, z, -beta)
    x, y = rotate(x, y, alpha)
    return Vector(x, y, z)

    