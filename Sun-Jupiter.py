import pygame, sys
from pygame.locals import*
from sys import exit


def main():
	clock = pygame.time.Clock()

	pygame.init()
	screen=pygame.display.set_mode((800,800))
	pygame.display.set_caption('Basic Pygame program')
	Constant = 1000000000/800
	print Constant
	
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

	x,y=pygame.mouse.get_pos()

	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(background, (0, 0))
		pygame.display.flip()
		
	clock.tick(30)

if __name__ == '__main__': main()	



