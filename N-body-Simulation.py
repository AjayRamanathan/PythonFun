#! /usr/bin/python 
# A N-Body problem solver 

from numpy import *
from random import random,seed
import Tkinter
from PIL import Image, ImageDraw
import ImageTk
from time import time

N = 50
#Number of Particles
G = 0.125
#Gravitional Constant
R = 4
#Radius; changes the radius in UI
CONSTANT = 0.5
#Barnes-Hut Constant
MAXDEPTH = 0
#GRID_SIZE = 10
CROSS_SIZE = 20

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
	
	def __str__(self): #Output
		return "<<%g,%g,%g,%g>>" % (self.edge[0],self.edge[1],self.edge[2],self.edge[3])

UNIVERSE = Universe([0,0,10,10])        
#Initialization of universe corner co-ordinates

for i in xrange(N):
	MASS[i] = 1
	#MASS can be set as random too
	POSITION[i] = UNIVERSE.min() + array([random(),random()])*UNIVERSE.length
	#Random Initial position

class Tree:
		#A smaller rectangles, contains some point bodies considered as one
		def __init__(self,universe,bodies = None,depth=0):
				self.universe = universe
				self.center = universe.center
				self.leaf = True # Whether is a parent or not
				self.depth = depth
				if bodies != None: # want to capture 0 int also
						self.setToBody(bodies)
						self.number = 1
				else:
						self.bodies = []
						self.mass = 0.
						self.center = array([0,0], dtype=float)
						self.number = 0
						
				self.children = [None]*4

		def addBody(self, k,depth):
				if len(self.bodies) > 0 or not self.leaf:
						if (depth >= MAXDEPTH):
								self.bods.append(k)
						else:
								subBodies = [k]
								if len(self.bodies) > 0:
										subBodies.append(self.bodies[0])
										self.bodies = []

								for bodiees in subBodies:
										ID = self.getTreenumber(bodies)
										if self.children[ID]:
												self.children[ID].addBody(bodies,depth+1)
										else:
												subuniverse = self.universe.getSubQuad(ID)
												self.children[ID] = Quad(subuniverse, bodies, depth+1)

								self.leaf = False

						weight = MASS[k]
						self.center = (self.center * self.mass + POSITION[k] * weight) / (self.mass + weight)
						self.mass += weight
				else:
						self.setToBody(k)

		def updatecenter(self):
				if self.leaf:
						self.mass = array(map(lambda x: MASS[x], self.bodies)).sum() #Total Mass
						self.center = array(map(lambda x: POS[x]*MASS[x], self.bodies)).sum(0) / self.mass #New Center of mass
				else:
						self.mass = array(map(lambda child: child.mass if child else 0, self.children)).sum()  #Mass and Center of child-nodes
						self.com = array(map(lambda child: child.mass*child.com if child else zeros(2), self.children)).sum(0) / self.mass
				
		def setToBody(self,k):
				self.bods = [k]
				self.mass = float( MASS[k].copy() )
				self.center = POS[k].copy()

		def getTreenumber(self,k):
				return self.universe.getTreenumber(POS[k])

class Physics: #Class Physics: Physics of the system
	global N, CONSTANT
	tree = None
	
	def __init__(self, universe):
		self.universe = universe
		self.initialize()
	def initialize(self):
		self.tree = Tree(self.universe)
	def generate(self): #generate a new tree
				self.initialize()
				for x in xrange(self.tree.number): # For each body, add to tree
						self.tree.addBody(x,0)  
	def updateSys(self, Skip_Time):#Iterate over time
		global VELOCITY, POSITION, ACCELERATION, MASS
		self.calculateBHAcceleration()
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

	def calculateBHAcceleration(self):#Calculate Accceleration of all the bodies
		for i in xrange(N):
			ACCELERATION[i] = self.calculateBHBodyAcceleration(i, self.tree) 

	def calculateBHBodyAcceleration(self, i, tree):  #calculate the acceleration of one body            
		acc = zeros((1,2),dtype=float)
		if (tree.leaf):
				for k in tree.bodies:
						if k != i:
								acc += getAcceleration( POSITION[i] ,MASS[i],POSITION[k],MASS[k])
		else:
				maxlength = max( node.box.sideLength )
				vector = tree.center - POSITION[i]
				radius = sqrt(vector.dot(vector))
				if (radius > 0 and maxlength/radius < CONSTANT):
						acc += getAcceleration( POSITION[i] ,MASS[i], tree.position, tree.mass)
				else:
						for k in xrange(4):
								if tree.children[k] != None:
										acc += self.calculateBodyAccelR(k, node.children[k])
				return acc
		for k in xrange(N):
			if i != k and MASS[i] != 0:
				 acc -= getAcceleration(POSITION[k], MASS[k], POSITION[i], MASS[i]) #Sum of all accelerations
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

def drawVels(drawPtr):
		for x in xrange(N):
				if UNIVERSE.inside(POSITION[x]):
						drawLine(drawPtr, POSITION[x], POSITION[x]+VELOCITY[x], (0,0,255) )

def drawAccs(drawPtr):
		for x in xrange(N):
				if UNIVERSE.inside(POSITION[x]):
						drawLine(drawPtr, POSITION[x], POSITION[x]+ACCELERATION[x], (255,0,0) )

def join(p1,p2):
		return ([p1[0],p1[1],p2[0],p2[1]])

def drawBOX(drawPtr, foo):
		if foo.depth == 0:
				drawCross(drawPtr,foo.center)

		p = join(convertPos(foo.universe.min()),
						 convertPos(foo.universe.max()))
		print p
		drawPtr.rectangle( p , outline=(0,0,255) )

def drawLine(drawPtr, p1, p2, color):
		drawPtr.line( join( convertPos(p1) , convertPos(p2) ), fill=color )

def drawCross(drawPtr, p):
		global CROSS_SIZE
		p = convertPos(p)
		drawPtr.line( (p[0]-CROSS_SIZE,p[1],p[0]+CROSS_SIZE,p[1]), fill=(0,255,0) )
		drawPtr.line( (p[0],p[1]-CROSS_SIZE,p[0],p[1]+CROSS_SIZE), fill=(0,255,0) )

def drawTree(drawPtr ,bar):
	drawTreeDetail(drawPtr, bar.tree)
def drawTreeDetail(drawPtr, tree):
	drawBOX(drawPtr,tree)
	for child in tree.children:
		if child != None:
			drawTreeDetail(drawPtr,child)
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
	global Time, ICON
	
	Time += Skip_Time #Time change
	sys.generate()

	im = Image.new('RGB', IMAGE_SIZE, (255,255,255)) #Drawing part
	draw = ImageDraw.Draw(im)
	
	drawTree(draw,sys)
	drawBodies(draw)
	drawVels(draw)
	drawAccs(draw)
	sys.updateSys(Skip_Time) #Updating Physics

	ICON = ImageTk.PhotoImage(im)
	label_image.config(image=ICON)
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

ICON = None
task_update() 
root.mainloop() #Start of loop
print "Done."