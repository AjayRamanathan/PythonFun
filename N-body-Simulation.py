#! /usr/bin/python 
# A N-Body problem solver 

from numpy import *

N = 100

MASS = zeros(N,dtype=float)
POSTION = zeros((N,2),dtype=float)
VELOCITY = zeros((N,2),dtype=float)

class Universe:
    def __init__(self,edge,dimension=2):
        assert(dimension*2 == len(edge))
        self.edge = array(edge,dtype=float)
        self.dimension = dimension
        self.center = array( [(self.edge[2]+self.edge[0])/2, (self.edge[3]+self.edge[1])/2] , dtype=float)
        self.sideLength = self.max() - self.min()

    def max(self):
        return self.edge[self.dimension:]
    
    def min(self):
        return self.edge[:self.dimension]
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "<<%g,%g,%g,%g>>" % (self.edge[0],self.edge[1],self.edge[2],self.edge[3])

UNIVERSE = Universe([0,0,10,10])        

print UNIVERSE.sideLength
print UNIVERSE.center
print UNIVERSE.edge
print UNIVERSE.dimension