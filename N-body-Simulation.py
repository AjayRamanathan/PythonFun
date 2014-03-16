#! /usr/bin/python 
# A N-Body problem solver 
#

from numpy import *
from random import random,seed

G= 0.125
N = 100

class Iteratate(type):
    def __iter__(self):
        return self.classiter()

class Objects:
    __metaclass__ = Iteratate
    by_id = {}
    def __init__(self, mass, position, velocity, acceleration, id):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.radius = math.sqrt(self.mass)
        self.id = id
        self.by_id[id] = self
    
    def __repr__(self):
       return self.__str__()

    def __str__(self):
       return "<<%g,%g,%g,%g>>" % (self.mass,self.position,self.velocity,self.acceleration)
       return iter(cls.by_id.values())
    
class Universe:
    def __init__(self,edge,dimension=2):
        assert(dimension*2 == len(edge))
        self.edge = array(edge,dtype=float)
        self.dimension = dimension
        self.center = array( [(self.edge[2]+self.edge[0])/2, (self.edge[3]+self.edge[1])/2] , dtype=float)
        self.length = self.max() - self.min()

    def max(self):
        return self.edge[self.dimension:]
    
    def min(self):
        return self.edge[:self.dimension]
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "<<%g,%g,%g,%g>>" % (self.edge[0],self.edge[1],self.edge[2],self.edge[3])

UNIVERSE = Universe([-10,-10,10,10])  
OBJECTS = Iteratate

for i in xrange(N):
    MASS = 1
    POSITION = UNIVERSE.min() + array([random(),random()])*UNIVERSE.length
    VELOCITY = UNIVERSE.min() + array([random(),random()])*UNIVERSE.length
    ACCELERATION = UNIVERSE.min() + array([random(),random()])*UNIVERSE.length
    OBJECTS = Objects(MASS, POSITION, VELOCITY, ACCELERATION)

def getForce(i1, i2):

    vector = i2.position-i1.position
    radius = sqrt(vector.dot(vector))
    force = array( vector * G*p.mass*p2.mass / radius**3 )
    return force 

for i1 in OBJECTS:
    for i2 in OBJECTS:
        if i1 != i2:
            acceleration = getForce(i1, i2) / i1.mass
            i1.acceleration += acceleration

for i in OBJECTS:
	i.velocity += i.acceleration
        i.position += i.velocity

for i1 in OBJECTS:
    for i2 in OBJECTS:
        if i1 != i2:
            vector = i2.position-i1.position
            radius = sqrt(vector.dot(vector))
            if Distance < (i1.radius+i2.radius):
                p.velocity = ((i.mass*i.velocity)+(i2.mass*i2.velocity))/(i.mass+i2.mass)
                i.position = ((i.mass*i.position)+(i2.mass*i2.position))/(i.mass+i2.mass)
                i.mass += i2.mass
                i.radius = math.sqrt(i.mass)
                Objects.remove(i2)