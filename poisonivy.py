import pygame

class PoisonIvy(pygame.sprite.Sprite):
	PIECEJAUNE = 0
	PIECEARGENT = 1
	QUESTIONBOX = 2
	BOX = 3
	POMMEROUGE = 4
	POMMEROSE = 5
	POMMEVERT = 6
	FLEURNOIR = 7
	NOTEMUSIQUE = 8

	spriteSheet = pygame.image.load("./levels/Sprites/AnimatedTiles.png")
	# piece jaune
	# piece argentée
	# questionbox
	# box
	# pomme rouge
	# pomme rose
	# pomme vert
	# fleur noir
	# note musique
	sequences = [(0,4,True),(4,4,True),(8,4,True),(12,4,True),(16,3,True),(19,3,True),(22,3,True),(29,2,True),(31,3,True)]

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	def __init__(self, FPS, playfield, obstacles):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

		self.image = PoisonIvy.spriteSheet.subsurface(pygame.Rect(0,0,16,16))
		self.rect = pygame.Rect(0,0,16,16)
		self.rect.bottom = 16

		self.numeroSequence = 7
		self.numeroImage = 0

		self.deltaTime = 0

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		
		if self.deltaTime>=500:
			self.deltaTime = 0

			# on calcule l'image à afficher
			n = PoisonIvy.sequences[self.numeroSequence][0]+self.numeroImage
			self.image = PoisonIvy.spriteSheet.subsurface(pygame.Rect(n%40*16,n//40*16,16,16))
			
			self.numeroImage = self.numeroImage+1
			
			if self.numeroImage == PoisonIvy.sequences[self.numeroSequence][1]:
				if PoisonIvy.sequences[self.numeroSequence][2]:
					self.numeroImage = 0
				else:
					self.numeroImage = self.numeroImage-1
	
	def setPosition(self, x, y):
		self.rect = pygame.Rect(x, y, 16, 16)

	def getPosition(self):
		return self.rect

	def estTouche(self):
		return

	def estMort(self):
		return False
