#! /usr/bin/python 
# A N-Body problem solver 
#

from numpy import *
from random import random,seed

N = 100

class Objects:
    def __init__(self, mass, position, velocity, acceleration, radius):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.radius = radius

    def __repr__(self):
       return self.__str__()

    def __str__(self):
       return "<<%g,%g,%g,%g>>" % (self.mass,self.position,self.velocity,self.acceleration)

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
OBJECTS = []
for i in xrange(N):
    MASS = 1
    POSITION = UNIVERSE.min() + array([random(),random()])*UNIVERSE.length
    VELOCITY = UNIVERSE.min() + array([random(),random()])*UNIVERSE.length
    ACCELERATION = UNIVERSE.min() + array([random(),random()])*UNIVERSE.length
    RADIUS = 1
    OBJECTS = Objects(MASS, POSITION, VELOCITY, ACCELERATION, RADIUS)
    




