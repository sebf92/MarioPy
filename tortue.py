import pygame

# Sequences:
# 0 : position d'attente
# 1 : Avance
# 2 : meurt
# 3 : avance face
# 4 : avance de dos
# 5 : monte
class Tortue(pygame.sprite.Sprite):

	# Variable qui contient la direction courante du sprite
	#    8  1  2
	#    7  0  3
	#    6  5  4
	directioncourante = 3

	positionprecedente = pygame.Rect((0,0),(0,0))

	obstacles = list()
	playfield = pygame.Rect((0,0),(0,0))

	spriteSheet = pygame.image.load("./levels/Sprites/Turtle.png")
	sequences = [(0,1,False, False),(1,2,True, False),(3,4,False, True),(7,2,True, False),(9,2,True, False),(10,1,False, False)]

	mort = False

	# couleur des tortues
	# 0 : rouge
	# 1 : vert
	# 2 : jaune
	# 3 : bleu
	couleur = 0

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	# playfield : Rect, La taille du playfield (pour le clipping)
	# Obstacles : List(Rect), Les obstacles sous la forme d'une liste de Rect pour la détection de collision avec le décor
	def __init__(self, FPS, playfield, obstacles):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

		self.image = Tortue.spriteSheet.subsurface(pygame.Rect(0,0,16,32))
		self.rect = pygame.Rect(0,0,16,32)
		self.rect.bottom = 32

		self.numeroSequence = 1
		self.numeroImage = 0
		self.flip = True

		self.deltaTime = 0
		self.vitesse = int(round(120/FPS))
			
		self.playfield = playfield
		self.obstacles = obstacles

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		
		if self.deltaTime>=100:
			self.deltaTime = 0

			# on sauvegarde la position courante pour revenir en arriere en cas de collision
			self.positionprecedente = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

			# on met a jour la position en fonction de la direction
			if self.directioncourante == 2: # en haut a droite
				self.rect = self.rect.move(self.vitesse,-self.vitesse).clamp(self.playfield)
				self.flip = False
			elif self.directioncourante == 3: # a droite
				self.rect = self.rect.move(self.vitesse,0).clamp(self.playfield)
				self.flip = False
			elif self.directioncourante == 4: # en bas a droite
				self.rect = self.rect.move(self.vitesse,self.vitesse).clamp(self.playfield)
				self.flip = False
			elif self.directioncourante == 5: # en bas
				self.rect = self.rect.move(0,self.vitesse).clamp(self.playfield)
				self.flip = False
			elif self.directioncourante == 6: # en bas a gauche
				self.rect = self.rect.move(-self.vitesse,self.vitesse).clamp(self.playfield)
				self.flip = True
			elif self.directioncourante == 7: # a gauche
				self.rect = self.rect.move(-self.vitesse,0).clamp(self.playfield)
				self.flip = True
			elif self.directioncourante == 8: # en haut a gauche
				self.rect = self.rect.move(-self.vitesse,-self.vitesse).clamp(self.playfield)
				self.flip = True
			elif self.directioncourante == 1: # en haut
				self.rect = self.rect.move(0,-self.vitesse).clamp(self.playfield)
				self.flip = True

			# on teste les collisions avec le décor
			if self.rect.collidelist(self.obstacles) != -1:
				self.collision()

			# on gère la gravité: si la tortue est dans le vide on le fait tomber doucement
			if self.rect.move(0,2).collidelist(self.obstacles) == -1:
				self.rect = self.rect.move(0, 2).clamp(self.playfield) # on le descend de deux pixels si il n'a pas d'obstacle sous lui
			elif self.rect.move(0,1).collidelist(self.obstacles) == -1:
				self.rect = self.rect.move(0, 1).clamp(self.playfield) # on le descend d'un pixel si il n'a pas d'obstacle sous lui

			# on calcule l'image à afficher
			n = Tortue.sequences[self.numeroSequence][0]+self.numeroImage
			self.image = Tortue.spriteSheet.subsurface(pygame.Rect(n%20*16,self.couleur*32+n//20*32,16,32))
			if self.flip:
				self.image = pygame.transform.flip(self.image,True,False)
			
			self.numeroImage = self.numeroImage+1
			
			if self.numeroImage == Tortue.sequences[self.numeroSequence][1]:
				if Tortue.sequences[self.numeroSequence][3]:
					self.mort = True
				if Tortue.sequences[self.numeroSequence][2]:
					self.numeroImage = 0
				else:
					self.numeroImage = self.numeroImage-1
	
# 0 : position d'attente
# 1 : Avance
# 2 : meurt
# 3 : avance face
# 4 : avance de dos
# 5 : monte
	def setSequence(self,n):
		if self.numeroSequence != n:
			self.numeroImage = 0
			self.numeroSequence = n
	
	def goRight(self):
		self.directioncourante = 3
		self.setSequence(1)

	def stopRight(self):
		self.directioncourante = 0
		self.setSequence(0)

	def goLeft(self):
		self.directioncourante = 7
		self.setSequence(1)

	def stopLeft(self):
		self.directioncourante = 0
		self.setSequence(0)

	def meurt(self):
		self.directioncourante = 0
		self.setSequence(2)

	def estMort(self):
		return self.mort

	def estTouche(self):
		self.changeDirection()
		
	def collision(self):
		# on reinitialise la position courante du sprite a la position precedente
		self.rect = pygame.Rect(self.positionprecedente.x, self.positionprecedente.y, self.positionprecedente.width, self.positionprecedente.height)
		self.changeDirection()

	def changeDirection(self):
		# on change de direction
		if self.directioncourante == 3:
			self.directioncourante = 7
		elif self.directioncourante == 7:
			self.directioncourante = 3

	def setPosition(self, x, y):
		self.rect = pygame.Rect(x, y, 16, 32)

	# Position courante du sprite pour les tests de collision
	def getPosition(self):
		return self.rect

	# Rectangle qui represente une ligne sous le sprite pour les tests de collision
	def getBottomRect(self):
		return pygame.Rect((self.rect.x, self.rect.y+32), (self.rect.width, 1))

	#    8  1  2
	#    7  0  3
	#    6  5  4
	def getDirection(self):
		return self.directioncourante


	# couleur des tortues
	# 0 : rouge
	# 1 : vert
	# 2 : jaune
	# 3 : bleu
	def setColor(self, color):
		self.couleur = color