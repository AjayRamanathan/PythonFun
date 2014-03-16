import pygame, sys
from pygame.locals import*
from sys import exit
import math


def main():
	N = 3*(365*10+2)
	print N
	clock = pygame.time.Clock()
	R = 200
	constant = 2000000000/(800*R)
	pygame.init()
	screen=pygame.display.set_mode((800,800))
	pygame.display.set_caption('Basic Pygame program')

	sun_x,sun_y = 400,400
	sun_color = (250, 250, 0)
	sun_radius = 696342/constant

	jb_x,jb_y = 200,200
	jb_color = (250, 100, 0)
	jb_radius = 69911/constant

	cg_color = (0, 0, 0)
	cg_radius = 4*10000/constant

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
			font = pygame.font.Font(None, 36)
			text = font.render("End of event", 1, (10, 10, 10))
			textpos = text.get_rect()
			textpos.centerx = background.get_rect().centerx
			textpos.centery = background.get_rect().centery
			background.blit(text, textpos)
		else:
			screen.blit(background, (0, 0))
			x,y=pygame.mouse.get_pos()
			pygame.draw.circle(screen, sun_color, (sun_x, sun_y), int(sun_radius+1))
			pygame.draw.circle(screen, cg_color, (x, y), cg_radius)
			pygame.draw.circle(screen, jb_color, (jb_x, jb_y), jb_radius)		
			pygame.display.flip()
		
		n += 1
	clock.tick(30)

if __name__ == '__main__': main()	



