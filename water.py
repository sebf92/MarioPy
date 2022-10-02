import pygame

class Water(pygame.sprite.Sprite):
	PIECEJAUNE = 0
	PIECEARGENT = 1
	QUESTIONBOX = 2
	BOX = 3
	POMMEROUGE = 4
	POMMEROSE = 5
	POMMEVERT = 6
	FLEURNOIR = 7
	NOTEMUSIQUE = 8

	spriteSheet = pygame.image.load("./levels/Sprites/water.png")

	sequences = [(0,4,True)]

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	def __init__(self, FPS):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

		self.image = Water.spriteSheet.subsurface(pygame.Rect(0,0,16,48))
		self.rect = pygame.Rect(0,0,16,48)
		self.rect.bottom = 48

		self.numeroSequence = 0
		self.numeroImage = 0

		self.deltaTime = 0
		self.vitesse = int(round(200/FPS))

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		
		if self.deltaTime>=200:
			self.deltaTime = 0

			# on calcule l'image à afficher
			n = Water.sequences[self.numeroSequence][0]+self.numeroImage
			self.image = Water.spriteSheet.subsurface(pygame.Rect(n%40*16,n//40*48,16,48))
			
			self.numeroImage = self.numeroImage+1
			
			if self.numeroImage == Water.sequences[self.numeroSequence][1]:
				if Water.sequences[self.numeroSequence][2]:
					self.numeroImage = 0
				else:
					self.numeroImage = self.numeroImage-1
	
	def setSequence(self,n):
		if self.numeroSequence != n:
			self.numeroImage = 0
			self.numeroSequence = n
	
	def setPosition(self, x, y):
		self.rect = pygame.Rect(x, y, 16, 48)

	def getPosition(self):
		return self.rect

