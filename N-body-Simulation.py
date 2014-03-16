#! /usr/bin/python 
# A N-Body problem solver 

from numpy import *
from random import random,seed
import Tkinter
from PIL import Image, ImageDraw
import ImageTk
from time import time

N = 5
G = 0.125
R = 5

MASS = zeros(N,dtype=float)
POSITION = zeros((N,2),dtype=float)
VELOCITY = zeros((N,2),dtype=float)
ACCELERATION = zeros((N,2),dtype=float)

Skip_Time = 0.1
Time = 0

IMAGE_SIZE = (600,400)
GRID_SIZE = 10
CIRCLE_RADIUS = 10

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

	def inside(self,p):
		if any(p < self.min()) or any(p > self.max()):
			return False
		else:
			return True    
	
	def __str__(self):
		return "<<%g,%g,%g,%g>>" % (self.edge[0],self.edge[1],self.edge[2],self.edge[3])

UNIVERSE = Universe([0,0,10,10])        

for i in xrange(N):
	MASS[i] = 1
	POSITION[i] = UNIVERSE.min() + array([random(),random()])*UNIVERSE.length

class Physics:
	global N
	def __init__(self, universe):
		self.universe = universe

	def updateSys(self, Skip_Time):
		global VELOCITY, POSITION, ACCELERATION, MASS
		self.calculateAcceleration()
		VELOCITY = VELOCITY + ACCELERATION * Skip_Time
		POSITION += VELOCITY * Skip_Time  + ACCELERATION * Skip_Time * Skip_Time
		self.checkCollision()
	
	def checkCollision(self):
		global R
		for i in xrange(N):
			for k in xrange(N):
				if i != k and MASS[k]!= 0:
						Distance = getDistance(POSITION[k], POSITION[i])
						if Distance < (MASS[i]*0.5+MASS[k]*0.5):
						#Work Needed	
								VELOCITY[i] = ((MASS[i]*VELOCITY[i])+(MASS[k]*VELOCITY[k]))/(MASS[i]+MASS[k])
								POSITION[i] = ((MASS[i]*POSITION[i])+(MASS[k]*POSITION[k]))/(MASS[i]+MASS[k])
								MASS[i] += MASS[k]
								MASS[k] = 0

	def calculateAcceleration(self):
		for i in xrange(N):
			ACCELERATION[i] = self.calculateBodyAcceleration(i)

	def calculateBodyAcceleration(self, k):              
		acc = zeros((1,2),dtype=float)
		for i in xrange(N):
			if k != i:
				 acc += getAcceleration(POSITION[k], MASS[k], POSITION[i], MASS[i])
		return acc

def getAcceleration(p1,m1,p2,m2):
	vector = p2-p1
	radius = sqrt(vector.dot(vector))
	acceleration = 0
	if m1 != 0 and m2 != 0:
	  acceleration = array(( vector * G*m1*m2 / radius**3 ))/m1  
	return acceleration   

def getDistance(p1,p2):
	vector = p2-p1
	distance = sqrt(vector.dot(vector))	
	return distance   
	
sys = Physics(UNIVERSE)

def drawBodies(drawPtr):
	global R
	for x in xrange(N):
		if UNIVERSE.inside(POSITION[x]):
			p = convertPos(POSITION[x])
			r = MASS[x]*R
			drawPtr.ellipse( join(p-r,p+r) , fill = (0,0,0) )

def convertPos(p):
	c = trunc( ( p - UNIVERSE.min()) / (UNIVERSE.max()-UNIVERSE.min()) * array(IMAGE_SIZE) ).tolist()
	c[1] = IMAGE_SIZE[1] - c[1]
	return c

def join(p1,p2):
		return ([p1[0],p1[1],p2[0],p2[1]])	

def task_update():
	global Time,boo
	
	Time += Skip_Time
	im = Image.new('RGB', IMAGE_SIZE, (255,255,255))
	
	draw = ImageDraw.Draw(im)
	drawBodies(draw)
	sys.updateSys(Skip_Time)

	boo = ImageTk.PhotoImage(im)
	label_image.config(image=boo)
	label_image.pack()

	root.after(10,task_update)

def button_click_exit_mainloop (event):
	event.widget.quit() 

root = Tkinter.Tk()
root.bind("<Button>", button_click_exit_mainloop)
label_image = Tkinter.Label(root)
Time += Skip_Time
sys.updateSys(Skip_Time)
im = Image.new('RGB', IMAGE_SIZE, (255,255,255))
draw = ImageDraw.Draw(im)

drawBodies(draw)

task_update()
root.mainloop()
print "Done."