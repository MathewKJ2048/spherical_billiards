from vectors import *
from conf import *
import random

PLANE_RADIUS = radius+ball_radius


def to_position(R,theta,phi):
    r = Vector(0,0,0)
    r.i = R*math.cos(theta)*math.sin(phi)
    r.j = R*math.sin(theta)*math.sin(phi)
    r.k = R*math.cos(phi)
    return r

tracer_set = True
def get_tracer_set():
    return tracer_set
def set_tracer():
    global tracer_set
    tracer_set = True
def unset_tracer():
    global tracer_set
    tracer_set = False

power = 1
def increase_power():
    global power
    if power<=1:
        power+=POWER_SENSITIVITY
def decrease_power():
    global power
    if power>=0:
        power-=POWER_SENSITIVITY
def get_power():
    global power
    return power

class Ball:
    def __init__(self,color,r,v):
        self.r = r
        self.v = v
        self.color = color

active_balls = []
active_balls.append(Ball(WHITE,to_position(PLANE_RADIUS,0,math.pi/4),Vector(0,0,0))) # striker

def get_striker():
    return active_balls[0]
velocity_tracer = Vector(0,0,0)


def get_tracer():
    return velocity_tracer
def set_random_velocity():
    global velocity_tracer
    vt = Vector(0,0,0)
    vt.i = random.random()
    vt.j = random.random()
    vt.k = random.random()
    vt_parallel, vt_perpendicular = components(vt, get_striker().r)
    if vt_parallel.magnitude() != 0:
        velocity_tracer = vt_parallel.normalize()
    else:
        set_random_velocity()

set_random_velocity()

def launch():
    get_striker().v = velocity_tracer*LAUNCH_VELOCITY*power
    unset_tracer()

def turn_tracer(invert=False, fine=False):
    theta = ANGLE_SENSITIVITY
    if fine:
        theta = FINE_ANGLE_SENSITIVITY
    if invert:
        theta = -theta
    global velocity_tracer
    n = get_striker().r.vector_product(velocity_tracer).normalize()
    new_tracer = (velocity_tracer.normalize()*math.cos(theta)+n*math.sin(theta))*velocity_tracer.magnitude()
    velocity_tracer = new_tracer


def collide(b1, b2):
    n = b1.r - b2.r
    v_rel = b1.v - b2.v
    if n.scalar_product(v_rel) >= 0:
        return
    v1_par, v1_perp = components(b1.v, n)
    v2_par, v2_perp = components(b2.v, n)
    # if balls have equal mass, perpendicular velocities are exchanged
    b1.v = v1_par + v2_perp
    b2.v = v2_par + v1_perp

def evolve(dt):
    global velocity_tracer
    for b in active_balls:
        new_r = (b.r + b.v*dt).normalize()*PLANE_RADIUS
        mag = b.v.magnitude() - friction*dt
        if mag<=0:
            mag = 0
        new_v = b.r.vector_product(b.v).vector_product(new_r).normalize() * mag
        b.r = new_r
        b.v = new_v
        for b_ in active_balls:
            if b_ != b:
                dist = (b.r - b_.r).magnitude()
                if dist <= 2*ball_radius:
                    collide(b,b_)

        settle = True
        for b in active_balls:
            if b.v.magnitude() != 0:
                settle = False
        if settle and get_tracer_set() == False:
            set_random_velocity()
            set_tracer()
    pass




def init():
    a_d_s = 2*ball_radius/radius
    a_d_d = math.sqrt(3)*a_d_s
    theta = math.pi/6

    active_balls.append(Ball(BLUE,to_position(PLANE_RADIUS,0,0),Vector(0,0,0)))
    for I in range(6):
        i = 2*I
        for j in [1,2]:
            active_balls.append(Ball(RED,to_position(PLANE_RADIUS,theta*i,a_d_s*j),Vector(0,0,0)))
    for I in range(6):
        i = 2*I+1
        active_balls.append(Ball(BLUE,to_position(PLANE_RADIUS,theta*i,a_d_d),Vector(0,0,0)))



