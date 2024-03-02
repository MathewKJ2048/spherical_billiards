import math

height = 800
width = 800

radius = 300
ball_radius =10
hole_radius = 4*ball_radius
hole_rotator_radius = 0.5*ball_radius

friction = 0.0001

max_frame_rate = 60

ANGLE_SENSITIVITY = 0.05
FINE_ANGLE_SENSITIVITY = 0.005
POWER_SENSITIVITY = 0.01

LAUNCH_VELOCITY = 1

CAMERA_SENSITIVITY = 0.1

orbit_factor = 1.2

right = math.pi/2
hole_orientations = []
for i in range(4):
    # theta, phi
    hole_orientations.append((right*i,right))

SPIN = 0.001

NUM_RING = 20

TRACER_RADII = [8,7,6,5,4,4,4,4,4,4,4,4]
TRACER_POSITIONS = [4,8,12,16,20,24,28,32,36,40,44,48] # at max power
for i in range(len(TRACER_POSITIONS)):
    TRACER_POSITIONS[i]*=ball_radius

