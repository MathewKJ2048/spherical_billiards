import math
import random

class Vector:
    def __init__(self,i,j,k):
        self.i = i
        self.j = j
        self.k = k
    
    def __str__(self):
        return f"({self.i}, {self.j}, {self.k})"

    def __add__(self, other):
        return Vector(self.i + other.i, self.j + other.j, self.k + other.k)

    def __sub__(self, other):
        return Vector(self.i - other.i, self.j - other.j, self.k - other.k)

    def __mul__(self, scalar):
        return Vector(self.i * scalar, self.j * scalar, self.k * scalar)
    
    def scalar_product(self,other):
        return self.i*other.i+self.j*other.j+self.k*other.k

    def vector_product(self, other):
        i = self.j * other.k - self.k * other.j
        j = self.k * other.i - self.i * other.k
        k = self.i * other.j - self.j * other.i
        return Vector(i, j, k)

    def magnitude(self):
        return math.sqrt(self.scalar_product(self))

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0, 0)
        else:
            return self * (1/mag)


def components(v,n):
    n = n.normalize()
    v_perpendicular = n * v.scalar_product(n)
    v_parallel = v - v_perpendicular
    return v_parallel, v_perpendicular

def to_position(R,theta,phi):
    r = Vector(0,0,0)
    r.i = R*math.cos(theta)*math.sin(phi)
    r.j = R*math.sin(theta)*math.sin(phi)
    r.k = R*math.cos(phi)
    return r

def to_spherical_coordinates(r):
    x,y,z = r.i,r.j,r.k
    R = r.magnitude()
    theta = math.atan2(y,x)
    phi = math.atan2((y**2+x**2)**(0.5),z)
    return R, theta, phi

def random_perpendicular(v):
    vt = Vector(0,0,0)
    vt.i = random.random()
    vt.j = random.random()
    vt.k = random.random()
    vt_parallel, vt_perpendicular = components(vt, v)
    if vt_parallel.magnitude()==0:
        return random_perpendicular(v)
    return vt_parallel.normalize()

def random_basis(v):
    vx = random_perpendicular(v)
    vy = vx.vector_product(v).normalize()
    return (vx, vy)

def ring(v, basis, number, radius, offset): # list of vectors radial to v, all perpendicular to v, constant angular difference
     vx, vy = basis
     ring = []
     for i in range(number):
        theta = math.pi*2*i/number + offset
        ring.append((vx*math.cos(theta)+vy*math.sin(theta))*radius)
     return ring