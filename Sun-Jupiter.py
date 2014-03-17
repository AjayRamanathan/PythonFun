import pygame, sys
from pygame.locals import*
from sys import exit
from numpy import *
import math

G = 0.66759
constant = 2000000000/(800)

def main():

	SUN_MASS = 1.9891*(10**19)
	#JUPITER_MASS = 1.8986*(10**16)
	#CG_MASS = 33.5
	N = (365*10+2)
	JUPITER = zeros((N,6), dtype=float)

	Jupiter_a = [5.096210785220794E+08, -5.625673003639891E+08, -9.109215289602894E+06,  9.531092644846060E+00,  9.401837023552590E+00, -2.522073348918472E-01]
	Jupiter_b = [-1.986100514188347E+08, -7.697020902092769E+08,  7.614122074352508E+06,  1.250778592291153E+01, -2.651322314721329E+00, -2.693549489780306E-01]
	Jupiter_c = [7.496501615105320E+08, -3.201712734926724E+08,  1.811158327190959E+07,  4.981904715194972E+00, -1.141748300836142E+01, -6.466624164173854E-02]

	for i in xrange (3):
		Jupiter_a[i] = Jupiter_a[i]/constant
	for i in xrange (3):
		Jupiter_a[i+3] = Jupiter_a[i+3]*100*60*60*24*3/constant
	for i in xrange (3):
		Jupiter_b[i] = Jupiter_b[i]/constant
	for i in xrange (3):
		Jupiter_b[i+3] = Jupiter_c[i+3]*100*60*60*24*3/constant		
	for i in xrange (3):
		Jupiter_c[i] = Jupiter_c[i]/constant
	for i in xrange (3):
		Jupiter_b[i+3] = Jupiter_b[i+3]*100*60*60*24*3/constant
	for i in xrange (3):
		JUPITER[0][i] = Jupiter_a[i]
	M = 10**(-32)
	for i in xrange (N-1):
		JUPITER[i+1][3:] = JUPITER[i][3:] + M*getAcceleration((JUPITER[i][:3]),[0,0,0],SUN_MASS)
		JUPITER[i+1][:3] = JUPITER[i][:3] + JUPITER[i+1][3:]

	clock = pygame.time.Clock()
	pygame.init()
	screen=pygame.display.set_mode((800,800))
	pygame.display.set_caption('Basic Pygame program')

	sun_x,sun_y = 400,400
	sun_color = (250, 250, 0)
	sun_radius = 696342*200/(constant)

	jb_color = (255, 100, 0)
	jb_radius = 69911*200/(constant)

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
		if n > N-1:
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
			jb_y = 400 + int((JUPITER[n+1][1]))
			jb_x = 400 + int((JUPITER[n+1][0]))
			x, y = pygame.mouse.get_pos()
			pygame.draw.circle(screen, sun_color, (sun_x, sun_y), int(sun_radius+1))
			pygame.draw.circle(screen, cg_color, (x,y), cg_radius)
			pygame.draw.circle(screen, jb_color, (jb_x, jb_y), jb_radius)		
			pygame.display.flip()
		
		n += 1
	clock.tick(30)	

def getAcceleration(p1,p2,m1):
	global G
	global constant

	vector = p2-p1
	radius = sqrt(vector.dot(vector))
	if radius != 0:
		acceleration = array((( vector * G*m1 / radius**3 ))*constant*constant)
	else :
		acceleration = 0	
	return acceleration		

if __name__ == '__main__': main()			