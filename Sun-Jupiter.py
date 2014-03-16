import pygame, sys
from pygame.locals import*
from sys import exit
import math


def main():
	clock = pygame.time.Clock()
	R = 100
	pygame.init()
	screen=pygame.display.set_mode((800,800))
	pygame.display.set_caption('Basic Pygame program')
	constant = 2000000000/(800*R)
	print constant
	sun_radius = 696342/constant
	print sun_radius
	sun_x,sun_y = 400,400
	sun_color = (250, 250, 0)

	color = (0, 0, 0)
	radius = 69911/constant

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	
	font = pygame.font.Font(None, 36)
	text = font.render("Hello There", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)

	screen.blit(background, (0, 0))
	pygame.display.flip()

	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(background, (0, 0))
		x,y=pygame.mouse.get_pos()
		pygame.draw.circle(screen, sun_color, (sun_x, sun_y), int(sun_radius+1))
		pygame.draw.circle(screen, color, (x, y), radius)		
		pygame.display.flip()
		
	clock.tick(30)

if __name__ == '__main__': main()	



