import pygame, sys
from pygame.locals import*
from sys import exit
from numpy import *
import math

A = 1
N = 3*(365*10+2)*A
JUPITER = zeros((N,6), dtype=float)
Jupiter_a = (5.096210785220794E+08, -5.625673003639891E+08, -9.109215289602894E+06,  9.531092644846060E+00,  9.401837023552590E+00, -2.522073348918472E-01)
Jupiter_b = (-1.986100514188347E+08, -7.697020902092769E+08,  7.614122074352508E+06,  1.250778592291153E+01, -2.651322314721329E+00, -2.693549489780306E-01)
Jupiter_c = (7.496501615105320E+08, -3.201712734926724E+08,  1.811158327190959E+07,  4.981904715194972E+00, -1.141748300836142E+01, -6.466624164173854E-02)
JUPITER[0] = Jupiter_a

SUN_MASS = 1.9891*(10**19)
JUPITER_MASS = 1.8986*(10**16)
CG_MASS = 33.5
G = 6.67259

def main():
	
	R = 200
	constant = 2000000000/(800*R)

	clock = pygame.time.Clock()
	pygame.init()
	screen=pygame.display.set_mode((800,800))
	pygame.display.set_caption('Basic Pygame program')

	sun_x,sun_y = 400,400
	sun_color = (250, 250, 0)
	sun_radius = 696342/constant

	jb_x,jb_y = 200,200
	jb_color = (255, 100, 0)
	jb_radius = 69911/constant

	cg_color = (0, 0, 0)
	cg_radius = 4*5000/constant

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	screen.blit(background, (0, 0))
	pygame.display.flip()

	n = 0
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
		if n > N:
			screen.blit(background, (0, 0))
			font = pygame.font.Font(None, 36)
			text = font.render("End of event", 1, (10, 10, 10))
			textpos = text.get_rect()
			textpos.centerx = background.get_rect().centerx
			textpos.centery = background.get_rect().centery
			background.blit(text, textpos)
			pygame.display.flip()
		else:
			screen.blit(background, (0, 0))
			calculatejupiter(n+1)
			if JUPITER[n+1][1] and JUPITER[n+1][2]:
				jb_x = 400 + int(JUPITER[n+1][1]/(constant*R))
				jb_y = 400 + int(JUPITER[n+1][2]/(constant*10))
				print(int(JUPITER[n+1][1]/(constant*R)))

				print(int(JUPITER[n+1][2]/(constant*R)))
				print jb_x,jb_y
			else:
				jb_x = 400
				jb_y = 400

			x,y=pygame.mouse.get_pos()
			
			pygame.draw.circle(screen, sun_color, (sun_x, sun_y), int(sun_radius+1))
			pygame.draw.circle(screen, cg_color, (x, y), cg_radius)
			pygame.draw.circle(screen, jb_color, (jb_x, jb_y), jb_radius)		
			pygame.display.flip()
		
		n += 1
	clock.tick(30)

def calculatejupiter(i):
	global A
	
	JUPITER[i][3:] = JUPITER[i-1][3:] + A*getAcceleration((JUPITER[i-1][:3]),(0,0,0),SUN_MASS)
	JUPITER[i][:3] = JUPITER[i-1][:3] + A*JUPITER[i][3:]
	print JUPITER[i][:6]

def getAcceleration(p1,p2,m1): #Calculates acceleration between two objects
	vector = p2-p1
	radius = sqrt(vector.dot(vector))
	if radius != 0:
		acceleration = array(( vector * G*m1 / radius**3 ))
	else :
		acceleration = 0
	return acceleration 

if __name__ == '__main__': main()	



