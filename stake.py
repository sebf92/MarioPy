import pygame

class Stake(pygame.sprite.Sprite):
	spriteSheet = pygame.image.load("./levels/Sprites/stake.png")
	NBIMAGES = 19
	TEMPSPAUSE = 5000 # temps entre 2 montées du pic en ms

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	def __init__(self, FPS, playfield, obstacles):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

		self.image = Stake.spriteSheet.subsurface(pygame.Rect(0,0,16,80))
		self.rect = pygame.Rect(0,0,16,80)
		self.rect.bottom = 80

		self.numeroImage = 0
		self.inc = 0

		self.deltaTime = 0
		self.deltaTimeArmement = 0
		self.FPS = FPS

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		self.deltaTimeArmement = self.deltaTimeArmement + time
		
		# Déclenchement de l'animation du pic
		if(self.deltaTimeArmement>self.TEMPSPAUSE):
			self.deltaTimeArmement = 0
			self.inc = 1 # on déclenche le pic

		if self.deltaTime>=50:
			self.deltaTime = 0

			# on calcule l'image à afficher
			self.image = Stake.spriteSheet.subsurface(pygame.Rect(self.numeroImage*16,0,16,80))

			self.numeroImage = self.numeroImage+self.inc # on fait une animation qui consiste a faire monter et descendre le pic
			if(self.numeroImage<0):
				self.numeroImage = 0
				self.inc = 0
			elif(self.numeroImage>=self.NBIMAGES):
				self.numeroImage = self.NBIMAGES-1
				self.inc = -self.inc

	def setPosition(self, x, y):
		self.rect = pygame.Rect(x, y, 16, 16)

	def getPosition(self):
		return self.rect

	def estTouche(self):
		return

	def estMort(self):
		return False
