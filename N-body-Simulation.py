#! /usr/bin/python 
# A N-Body problem solver 

from numpy import *

N = 100

MASS = zeros(N,dtype=float)
POS = zeros((N,2),dtype=float)
VEL = zeros((N,2),dtype=float)

print MASS 
print POS 
print VEL