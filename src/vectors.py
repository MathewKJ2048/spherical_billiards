import math

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

