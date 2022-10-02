import pygame

# Sequences:
# 0 : position d'attente
# 1 : Regarde en haut
# 2 : s'accroupie
# 3 : Marche
# 4 : Saute	
# 5 : Collision	
class Mario(pygame.sprite.Sprite):

	# Variable qui contient la direction courante du sprite
	#    8  1  2
	#    7  0  3
	#    6  5  4
	directioncourante = 0
	isjumpingState = False
	isInjured = False

	velocitex = 0
	velocitey = 0
	accelerationx = 0
	accelerationy = 0
	positionprecedente = pygame.Rect((0,0),(0,0))

	obstacles = list()
	playfield = pygame.Rect((0,0),(0,0))

	spriteSheet = pygame.image.load("./levels/Sprites/Mario.png")
	sequences = [(0,1,False),(1,1,False),(2,1,False),(3,3,True),(6,1,False),(7,1,False)]

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	# playfield : Rect, La taille du playfield (pour le clipping)
	# Obstacles : List(Rect), Les obstacles sous la forme d'une liste de Rect pour la détection de collision avec le décor
	def __init__(self, FPS, playfield, obstacles):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()

		self.sonSaut = pygame.mixer.Sound("sounds/saut.wav")

		self.image = Mario.spriteSheet.subsurface(pygame.Rect(0,0,16,32))
		self.rect = pygame.Rect(0,0,16,32)
		self.rect.bottom = 32

		self.numeroSequence = 0
		self.numeroImage = 0
		self.flip = True

		self.deltaTime = 0
		self.vitesse = int(round(160/FPS))
			
		self.playfield = playfield
		self.obstacles = obstacles

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		

		# on sauvegarde la position courante pour revenir en arriere en cas de collision
		self.positionprecedente = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

		# on met a jour la position en fonction de la direction
		if self.directioncourante == 2: # en haut a droite
			self.rect = self.rect.move(self.vitesse,-self.vitesse).clamp(self.playfield)
			self.flip = True
		elif self.directioncourante == 3: # a droite
			self.rect = self.rect.move(self.vitesse,0).clamp(self.playfield)
			self.flip = True
		elif self.directioncourante == 4: # en bas a droite
			self.rect = self.rect.move(self.vitesse,self.vitesse).clamp(self.playfield)
			self.flip = True
		elif self.directioncourante == 5: # en bas
			self.rect = self.rect.move(0,self.vitesse).clamp(self.playfield)
			self.flip = True
		elif self.directioncourante == 6: # en bas a gauche
			self.rect = self.rect.move(-self.vitesse,self.vitesse).clamp(self.playfield)
			self.flip = False
		elif self.directioncourante == 7: # a gauche
			self.rect = self.rect.move(-self.vitesse,0).clamp(self.playfield)
			self.flip = False
		elif self.directioncourante == 8: # en haut a gauche
			self.rect = self.rect.move(-self.vitesse,-self.vitesse).clamp(self.playfield)
			self.flip = False
		elif self.directioncourante == 1: # en haut
			self.rect = self.rect.move(0,-self.vitesse).clamp(self.playfield)
			self.flip = True

		# on gere la velocité
		self.rect = self.rect.move(self.velocitex,self.velocitey).clamp(self.playfield)
		self.velocitex += self.accelerationx
		self.velocitey += self.accelerationy

		# on teste les collisions avec le décor
		if self.rect.collidelist(self.obstacles) != -1:
			self.collision()

		# on gère la gravité: si mario est dans le vide on le fait tomber doucement
		if not self.isJumping():
			for i in range(0,4):
				if self.rect.move(0,1).collidelist(self.obstacles) == -1:
					self.rect = self.rect.move(0, 1).clamp(self.playfield) # on le descend d'un pixel si il n'a pas d'obstacle sous lui
				else:
					break

			# on calcule l'image à afficher
		if self.deltaTime>=50:
			self.deltaTime = 0
			n = Mario.sequences[self.numeroSequence][0]+self.numeroImage
			self.image = Mario.spriteSheet.subsurface(pygame.Rect(n%64*16,n//64*32,16,32))
			if self.flip:
				self.image = pygame.transform.flip(self.image,True,False)
			
			self.numeroImage = self.numeroImage+1
			
			if self.numeroImage == Mario.sequences[self.numeroSequence][1]:
				if Mario.sequences[self.numeroSequence][2]:
					self.numeroImage = 0
				else:
					self.numeroImage = self.numeroImage-1
	
	# 0 : position d'attente
	# 1 : Regarde en haut
	# 2 : s'accroupie
	# 3 : Marche
	# 4 : Saute	
	def setSequence(self,n):
		if self.numeroSequence != n:
			self.numeroImage = 0
			self.numeroSequence = n
	
	def goRight(self):
		self.directioncourante = 3
		self.setSequence(3)

	def stopRight(self):
		self.directioncourante = 0
		self.setSequence(0)

	def jump(self):
		if not self.isjumpingState: # si il n'est pas deja en train de sauter
			self.isjumpingState = True
			self.velocitey = -12
			self.accelerationy = 1.5
			self.setSequence(4)

	# retourne True si c'est un nouveau dommage, False si un dommage est deja en cours de traitement
	def injured(self):
		if not self.isInjured:
			self.isInjured = True
			self.isjumpingState = True
			self.velocitey = -6
			self.accelerationy = 0.5
			self.setSequence(5)
			self.sonSaut.play()
			return True
		else:
			return False

	def goLeft(self):
		self.directioncourante = 7
		self.setSequence(3)

	def stopLeft(self):
		self.directioncourante = 0
		self.setSequence(0)

	def collision(self):
		# on reinitialise la position courante du sprite a la position precedente
		self.rect = pygame.Rect(self.positionprecedente.x, self.positionprecedente.y, self.positionprecedente.width, self.positionprecedente.height)

		# on arrete la chute
		if self.isjumpingState:
			self.velocitex = 0
			self.accelerationx = 0
			self.velocitey = 0
			self.accelerationy = 0
			self.isjumpingState = False
			if self.directioncourante == 0:
				self.setSequence(0)
			else: 
				self.setSequence(3)

		# si le saut est consécutif a un dommage, on reactive le compteur de dommage
		self.isInjured = False

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

	def isJumping(self):
		return self.isjumpingState
