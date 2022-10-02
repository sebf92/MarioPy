import pygame

class Score(pygame.sprite.Sprite):

	spriteSheet = pygame.image.load("./levels/Sprites/digits.png")

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

		self.image = pygame.Surface((52*3, 52))
		#self.image = pygame.Surface((52*3, 52), pygame.SRCALPHA, 32) # on crée une image transparente (pas necessaire ici car on réécrit le score a chaque fois)
		#self.image.convert_alpha()

		self.rect = pygame.Rect(0,0,52,52)
		self.rect.bottom = 52

		self.score = 0
		self.counter = 0

		self.deltaTime = 0

	def update(self,time):
		unite = self.counter%10
		dizaine = (self.counter//10)%10
		centaine = (self.counter//100)%10

		pygame.draw.rect(self.image, (255,255,255), (0,0,52*3,52))
		digit = Score.spriteSheet.subsurface(pygame.Rect(centaine*52,0,52,52))
		self.image.blit(digit, (0,0))
		digit = Score.spriteSheet.subsurface(pygame.Rect(dizaine*52,0,52,52))
		self.image.blit(digit, (52,0))
		digit = Score.spriteSheet.subsurface(pygame.Rect(unite*52,0,52,52))
		self.image.blit(digit, (104,0))

		# on gere une petite animation sur le score
		# avec un compteur
		self.deltaTime = self.deltaTime + time
		if self.deltaTime>=100:
			self.deltaTime = 0

			if(self.counter<self.score):
				self.counter = self.counter + 1
		
	def setPosition(self, x, y):
		self.rect = pygame.Rect(x, y, 52*3, 52)

	def getPosition(self):
		return self.rect

	def setScore(self, number):
		self.score = number
	
	def getScore(self):
		return self.score

	def addScore(self, val):
		self.score += val
		return self.score

	def subScore(self, val):
		self.score -= val
		return self.score
