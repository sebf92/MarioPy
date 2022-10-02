import pygame

class Digits(pygame.sprite.Sprite):

	spriteSheet = pygame.image.load("./levels/Sprites/digits.png")

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

		self.image = Digits.spriteSheet.subsurface(pygame.Rect(0,0,52,52))
		self.rect = pygame.Rect(0,0,52,52)
		self.rect.bottom = 52
		self.numeroImage = 0

	def update(self,time):
		# on calcule l'image à afficher
		index = self.numeroImage
		if(index<0):
			index = 0
		if(index>9):
			index = 9
		self.image = Digits.spriteSheet.subsurface(pygame.Rect(index*52,0,52,52))
	
	
	def setPosition(self, x, y):
		self.rect = pygame.Rect(x, y, 16, 16)

	def getPosition(self):
		return self.rect

	def setDigit(self, number):
		self.numeroImage = number
	
	def getDigit(self):
		return self.numeroImage

	def incDigit(self):
		self.numeroImage += 1
		return self.numeroImage

	def decDigit(self):
		self.numeroImage -= 1
		return self.numeroImage
