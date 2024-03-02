from vectors import *
from conf import *
from assets import *
import random

PLANE_RADIUS = radius+ball_radius

time=0
def get_time():
    global time
    return time

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
        self.active = True

balls = []
balls.append(Ball(WHITE,to_position(PLANE_RADIUS,0,math.pi/4),Vector(0,0,0))) # striker

hole_positions = []
hole_bases = []
for o in hole_orientations:
    r_h = to_position(PLANE_RADIUS,o[0],o[1])
    hole_bases.append(random_basis(r_h))
    hole_positions.append(r_h)


def get_striker():
    return balls[0]
velocity_tracer = Vector(0,0,0)


def get_tracer():
    return velocity_tracer
def set_random_velocity():
    global velocity_tracer
    velocity_tracer = random_perpendicular(get_striker().r)

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

def reflect(b, r):
    v_parallel, v_perpendicular = components(b.v, b.r - r)
    b.v = v_parallel - v_perpendicular

def evolve(dt):
    global velocity_tracer
    global time
    time+=dt



    active_balls = []
    inactive_balls = []
    for b in balls:
        if b.active:
            active_balls.append(b)
        else:
            inactive_balls.append(b)
    
    for b in inactive_balls:
        new_r = (b.r + b.v*dt)
        new_v = b.v
        if new_r.magnitude() >= orbit_factor*PLANE_RADIUS:
            new_r = new_r.normalize()*orbit_factor*PLANE_RADIUS
            new_v = b.r.vector_product(b.v).vector_product(new_r).normalize() * b.v.magnitude()
        b.r = new_r
        b.v = new_v

    for i in range(len(active_balls)):
        b = active_balls[i]
        for hr in hole_positions:
            if (b.r-hr).magnitude() <= hole_radius+ball_radius:
                if i!=0:
                    b.active = False
                else:
                    reflect(b,hr)
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





def init():
    a_d_s = 2*ball_radius/radius
    a_d_d = math.sqrt(3)*a_d_s
    theta = math.pi/6

    balls.append(Ball(BLUE,to_position(PLANE_RADIUS,0,0),Vector(0,0,0)))
    for I in range(6):
        i = 2*I
        for j in [1,2]:
            balls.append(Ball(RED,to_position(PLANE_RADIUS,theta*i,a_d_s*j),Vector(0,0,0)))
    for I in range(6):
        i = 2*I+1
        balls.append(Ball(BLUE,to_position(PLANE_RADIUS,theta*i,a_d_d),Vector(0,0,0)))



