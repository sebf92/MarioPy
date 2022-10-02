import pygame

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,x,y,image):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(x*8,y*8,8,8)
		self.image = image