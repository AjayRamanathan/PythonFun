#! /usr/bin/python 
# A Simple N-Body problem. Direct Method.
#Bug#1 Better Particle system using class particle
#Bug#2 Use pygame to display
#Bug#3 Better collision detection as you have adjust everytime you change radius
#Bug#5 Parallel Computing

from numpy import *
from random import random,seed
import Tkinter
from PIL import Image, ImageDraw
import ImageTk
from time import time

N = 20 #If you change this change line #15 and Line #92
#Number of Particles
G = 0.125
#Gravitional Constant
R = 4
#Radius; changes the radius in UI

MASS = zeros(N,dtype=float)
POSITION = zeros((N,2),dtype=float)
VELOCITY = zeros((N,2),dtype=float)
ACCELERATION = zeros((N,2),dtype=float)
#Initialization of Particles with all values as zero

Skip_Time = 0.1
#Time for which each loop runs
Time = 0
#Time

IMAGE_SIZE = (600,400)
#Screen Size
#Needs work; error auto-resize for other resolution

class Universe:#Class Universe; Boundaries
	def __init__(self,edge,dimension=2):
		assert(dimension*2 == len(edge))    #check dimensions
		self.edge = array(edge,dtype=float) #edge co-ordinate
		self.dimension = dimension
		self.center = array( [(self.edge[2]+self.edge[0])/2, (self.edge[3]+self.edge[1])/2] , dtype=float) #center
		self.length = self.max() - self.min() #array of two lengths

	def max(self):
		return self.edge[self.dimension:] #max
	
	def min(self):
		return self.edge[:self.dimension] #min
	
	def __repr__(self):
		return self.__str__()

	def inside(self,p): #checks whether object is inside or outside
		if any(p < self.min()) or any(p > self.max()):
			return False
		else:
			return True    
	
	def __str__(self): #Input
		return "<<%g,%g,%g,%g>>" % (self.edge[0],self.edge[1],self.edge[2],self.edge[3])

UNIVERSE = Universe([0,0,10,10])        
#Initialization of universe corner co-ordinates

for i in xrange(N):
	MASS[i] = 1
	#MASS can be set as random too
	POSITION[i] = UNIVERSE.min() + array([random(),random()])*UNIVERSE.length
	#Random Initial position


class Physics: #Class Physics: Physics of the system
	global N
	def __init__(self, universe):
		self.universe = universe

	def updateSys(self, Skip_Time):#Iterate over time
		global VELOCITY, POSITION, ACCELERATION, MASS
		self.calculateAcceleration()
		VELOCITY = VELOCITY + ACCELERATION * Skip_Time #New Velocity
		POSITION += VELOCITY * Skip_Time  + ACCELERATION * Skip_Time * Skip_Time #New Position
		self.checkCollision() #Check for Collision
	
	def checkCollision(self):#Check for Collision
		global R
		for i in xrange(N):
			for k in xrange(N):
				if i != k and MASS[k]!= 0:
						Distance = getDistance(POSITION[k], POSITION[i])*R*2
						if Distance < MASS[i]+MASS[k]:
								VELOCITY[i] = ((MASS[i]*VELOCITY[i])+(MASS[k]*VELOCITY[k]))/(MASS[i]+MASS[k])
								POSITION[i] = ((MASS[i]*POSITION[i])+(MASS[k]*POSITION[k]))/(MASS[i]+MASS[k])
								MASS[i] += MASS[k] 
								MASS[k] = 0 #Mass of partitcle 2 is 0; New Mass,New Velocity, and New Position

	def calculateAcceleration(self):#Calculate Accceleration of all the bodies
		for i in xrange(N):
			ACCELERATION[i] = self.calculateBodyAcceleration(i) 

	def calculateBodyAcceleration(self, k):  #calculate the acceleration of one body            
		acc = zeros((1,2),dtype=float)
		for i in xrange(N):
			if k != i and MASS[i] != 0:
				 acc += getAcceleration(POSITION[k], MASS[k], POSITION[i], MASS[i]) #Sum of all accelerations
		return acc

def getAcceleration(p1,m1,p2,m2): #Calculates acceleration between two objects
	vector = p2-p1
	radius = sqrt(vector.dot(vector))
	acceleration = 0
	if m1 != 0 and m2 != 0:
	  acceleration = array(( vector * G*m1*m2 / radius**3 ))/m1  
	return acceleration   

def getDistance(p1,p2): #calculates Distance between two objects
	vector = p2-p1
	distance = sqrt(vector.dot(vector))	
	return distance   
	
sys = Physics(UNIVERSE) #Physics Initiated

def drawBodies(drawPtr): #Draw body
	global R
	for x in xrange(N):
		if UNIVERSE.inside(POSITION[x]):
			p = convertPos(POSITION[x])
			r = MASS[x]*R
			drawPtr.ellipse( join(p-r,p+r) , fill = (0,0,0) )

def convertPos(p): #making the bodies eliptical
	c = trunc( ( p - UNIVERSE.min()) / (UNIVERSE.max()-UNIVERSE.min()) * array(IMAGE_SIZE) ).tolist()
	c[1] = IMAGE_SIZE[1] - c[1]
	return c

def join(p1,p2): #line between Two points
		return ([p1[0],p1[1],p2[0],p2[1]])	

def task_update(): #time
	global Time, icon
	
	Time += Skip_Time #Time change
	
	im = Image.new('RGB', IMAGE_SIZE, (255,255,255)) #Drawing part
	draw = ImageDraw.Draw(im)
	drawBodies(draw)
	
	sys.updateSys(Skip_Time) #Updating Physics

	icon = ImageTk.PhotoImage(im)
	label_image.config(image=icon)
	label_image.pack()

	root.after(10,task_update)

def button_click_exit_mainloop (event): #Define Click
	event.widget.quit() 

root = Tkinter.Tk() #Initialization of screen
root.bind("<Button>", button_click_exit_mainloop)
label_image = Tkinter.Label(root)
Time += Skip_Time #First time change

sys.updateSys(Skip_Time)

im = Image.new('RGB', IMAGE_SIZE, (255,255,255)) #First drawing
draw = ImageDraw.Draw(im)
drawBodies(draw)

task_update() 
root.mainloop() #Start of loop
print "Done."
