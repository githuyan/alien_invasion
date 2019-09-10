import pygame
import sys
def run():
	pygame.init()
	screen=pygame.display.set_mode((1200,800))
	pygame.display.set_caption='Alien'
	
	image=pygame.image.load('images/alien.bmp')
	alien_rect=image.get_rect()
	screen_rect=screen.get_rect()
	
	alien_rect.x=alien_rect.centerx
	alien_rect.y=alien_rect.centery
	
	direction=1
	
	while True:
		if alien_rect.right >= screen_rect.right:
			alien_rect.y +=20
			direction=-1
			alien_rect.x -=1
		elif alien_rect.left <=screen_rect.left:
			alien_rect.y +=20
			direction=1
			alien_rect.x+=1
		else:
			alien_rect.x +=direction
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			
		screen.fill((230,230,230))
		screen.blit(image,alien_rect)
		pygame.display.flip()
		
run()

	
	
