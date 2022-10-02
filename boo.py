import pygame,math,random

# Sequences:
# 0 : tire la langue
# 1 : fait boo
# 2 : bouche fermée
# 3 : meurt
class Boo(pygame.sprite.Sprite):

	obstacles = list()
	playfield = pygame.Rect((0,0),(0,0))

	spriteSheet = pygame.image.load("./levels/Sprites/boo.png")
	sequences = [(0,2,True, False),(2,2,True, False),(4,2,True, False),(6,4,False, True)]

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	# playfield : Rect, La taille du playfield (pour le clipping)
	# Obstacles : List(Rect), Les obstacles sous la forme d'une liste de Rect pour la détection de collision avec le décor
	def __init__(self, FPS, playfield, obstacles):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

		self.image = Boo.spriteSheet.subsurface(pygame.Rect(0,0,16,16))
		self.rect = pygame.Rect(0,0,16,16)
		self.rect.bottom = 16

		self.initialrect = pygame.Rect(0,0,16,16)
		self.initialrect.bottom = 16

		# Variable qui contient la direction courante du sprite
		#    8  1  2
		#    7  0  3
		#    6  5  4
		self.directioncourante = 3
		self.mort = False

		self.numeroSequence = 1
		self.numeroImage = 0
		self.flip = True

		self.deltaTime = 0
		self.vitesse = int(round(120/FPS))
			
		self.playfield = playfield
		self.obstacles = obstacles

		self.incangle = 2 # increment d'angle
		self.angle = random.randint(0,359) # compteur utilisé pour les mouvements
		self.rayonx = 100 # le rayon du cercle pour le fantome en pixels
		self.rayony = 50 # le rayon du cercle pour le fantome en pixels

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		
		if self.deltaTime>=100:
			self.deltaTime = 0

			# on incremente le compteur d'animation
			self.angle += self.incangle
			self.angle = self.angle % 360

			# on calcule les offsets sur le cercle
			incx = math.cos(self.angle*2*3.14/360)*self.rayonx
			incy = math.sin(self.angle*2*3.14/360)*self.rayony

			# on met a jour la position en fonction de la direction
			self.rect = pygame.Rect(self.initialrect.x+incx, self.initialrect.y+incy, 16, 16)
			if self.angle >0 and self.angle <180 : # on gere la direction du sprite en fonction de l'increment
				self.flip = True
			else:
				self.flip = False

			# on calcule l'image à afficher
			n = Boo.sequences[self.numeroSequence][0]+self.numeroImage
			self.image = Boo.spriteSheet.subsurface(pygame.Rect(n%20*16,n//20*32,16,16))
			if self.flip:
				self.image = pygame.transform.flip(self.image,True,False)
			
			self.numeroImage = self.numeroImage+1
			
			if self.numeroImage == Boo.sequences[self.numeroSequence][1]:
				if Boo.sequences[self.numeroSequence][3]:
					self.mort = True
				if Boo.sequences[self.numeroSequence][2]:
					self.numeroImage = 0
				else:
					self.numeroImage = self.numeroImage-1
	
# 0 : tire la langue
# 1 : fait boo
# 2 : bouche fermée
# 3 : meurt
	def setSequence(self,n):
		if self.numeroSequence != n:
			self.numeroImage = 0
			self.numeroSequence = n
	
	def meurt(self):
		self.directioncourante = 0
		self.setSequence(3)

	def estMort(self):
		return self.mort

	def estTouche(self):
		self.meurt()

	def setPosition(self, x, y):
		self.rect = pygame.Rect(x, y, 16, 16)
		self.initialrect = pygame.Rect(x, y, 16, 16)

	# Position courante du sprite pour les tests de collision
	def getPosition(self):
		return self.rect

	#    8  1  2
	#    7  0  3
	#    6  5  4
	def getDirection(self):
		return self.directioncourante

