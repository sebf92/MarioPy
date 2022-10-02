import pygame

class Objet(pygame.sprite.Sprite):
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
	def __init__(self, FPS):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

		self.image = Objet.spriteSheet.subsurface(pygame.Rect(0,0,16,16))
		self.rect = pygame.Rect(0,0,16,16)
		self.rect.bottom = 16

		self.numeroSequence = 0
		self.numeroImage = 0

		self.deltaTime = 0
		self.vitesse = int(round(200/FPS))

		self.sonRamassage = pygame.mixer.Sound("sounds/piece.wav")

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		
		if self.deltaTime>=200:
			self.deltaTime = 0

			# on calcule l'image à afficher
			n = Objet.sequences[self.numeroSequence][0]+self.numeroImage
			self.image = Objet.spriteSheet.subsurface(pygame.Rect(n%40*16,n//40*16,16,16))
			
			self.numeroImage = self.numeroImage+1
			
			if self.numeroImage == Objet.sequences[self.numeroSequence][1]:
				if Objet.sequences[self.numeroSequence][2]:
					self.numeroImage = 0
				else:
					self.numeroImage = self.numeroImage-1
	
	# PIECEJAUNE = 0
	# PIECEARGENT = 1
	# QUESTIONBOX = 2
	# BOX = 3
	# POMMEROUGE = 4
	# POMMEROSE = 5
	# POMMEVERT = 6
	# FLEURNOIR = 7
	# MUSIQUE = 8
	def setSequence(self,n):
		if self.numeroSequence != n:
			self.numeroImage = 0
			self.numeroSequence = n
	
	def setPosition(self, x, y):
		self.rect = pygame.Rect(x, y, 16, 16)

	def getPosition(self):
		return self.rect

	def collision(self):
		self.sonRamassage.play()

	def getReward(self):
		if self.numeroSequence == self.PIECEJAUNE:
			return 2
		elif self.numeroSequence == self.PIECEARGENT:
			return 4
		elif self.numeroSequence == self.QUESTIONBOX:
			return 10
		elif self.numeroSequence == self.BOX:
			return 5
		elif self.numeroSequence == self.POMMEROUGE:
			return 1
		elif self.numeroSequence == self.POMMEROSE:
			return 2
		elif self.numeroSequence == self.POMMEVERT:
			return 3
		elif self.numeroSequence == self.FLEURNOIR:
			return 0
		elif self.numeroSequence == self.NOTEMUSIQUE:
			return 7
		else:
			return 0
		
