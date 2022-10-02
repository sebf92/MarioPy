# #####################################################################################
#
# Un exemple de jeu de plateau en Python
#
#
# #####################################################################################

# Ne pas oublier d'installer les librairies manquantes:
# pip install pygame
# pip install pytmx

import sys,math,random,pygame,pytmx 
from pytmx.util_pygame import load_pygame

from mario import Mario
from objet import Objet
from water import Water
from tortue import Tortue
from boo import Boo
from poisonivy import PoisonIvy
from stake import Stake
from digits import Digits
from score import Score

def ajoutObjets(nomLayer, typeObjet):
	layer = tm.get_layer_by_name(nomLayer)
	for x,y,image in layer.tiles():
		objet = Objet(FPS)
		objet.setSequence(typeObjet)
		objet.setPosition(x*8, y*8-8)
		objets.append(objet)

# Paramètres principaux du jeu
WIDTH = 640
HEIGHT = 432
FPS = 60 
MUSIC = True
NBLIFE = 9
TITLE = "Mario Py"


# On initialise les variables du jeu
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF, vsync=1)
pygame.display.set_caption(TITLE)

# On charge le niveau
tm = pytmx.load_pygame('levels/level1.tmx')
tileWidth = tm.tilewidth
tileHeight = tm.tileheight
playfield = pygame.Rect((0, 0), (tm.width*tileWidth, tm.height*tileHeight))

while True: # on boucle entre ecran accueil -> jeu -> panneau de fin de partie
	# on initialise les variables de scrolling de l'ecran principal
	POSITION = 0 # La positionrelative d'affichage du playfield sur l'ecran
	PASX = 2 # Le pas de scrolling du playfield à l'ecran
	COMPTEUR = 0 # Un simple compteur pour les sprites animés

	# on charge la musique
	if MUSIC:
		pygame.mixer.music.load('soundtracks/01 - Super Mario Bros.mp3')

	# on crée la liste des obstacles en s'appuyant sur un layer specifique de la map
	obstacles = list()
	obstacleLayer = tm.get_layer_by_name("obstacles")
	for object in obstacleLayer:
		obstacles.append(pygame.Rect(object.x, object.y, object.width, object.height))

	# on crée la liste des zones mortelles
	zonesmortelles = list()
	mortLayer = tm.get_layer_by_name("mort")
	for mort in mortLayer:
		zonesmortelles.append(pygame.Rect(mort.x, mort.y, mort.width, mort.height))

	# on crée la liste des zones de fin
	zonesfin = list()
	finLayer = tm.get_layer_by_name("fin")
	for fin in finLayer:
		zonesfin.append(pygame.Rect(fin.x, fin.y, fin.width, fin.height))

	# on charge l'ensemble des objets à ramasser
	objets = list()
	ajoutObjets("piecesjaunes", Objet.PIECEJAUNE)
	ajoutObjets("piecesargentees", Objet.PIECEARGENT)
	ajoutObjets("questionbox", Objet.QUESTIONBOX)
	ajoutObjets("box", Objet.BOX)
	ajoutObjets("pommerouge", Objet.POMMEROUGE)
	ajoutObjets("pommeverte", Objet.POMMEVERT)
	ajoutObjets("pommerose", Objet.POMMEROSE)
	ajoutObjets("notemusique", Objet.NOTEMUSIQUE)

	# on charge et on positionne les sprites qui representent l'eau
	watersprites = list()
	layer = tm.get_layer_by_name("water")
	for x,y,image in layer.tiles():
		w = Water(FPS)
		w.setPosition(x*8, y*8-40)
		watersprites.append(w)

	# on charge et on positionne l'ensemble des ennemis
	ennemis = list()

	stakeLayer = tm.get_layer_by_name("stake")
	for x,y,image in stakeLayer.tiles():
		stake = Stake(FPS, playfield, obstacles)
		stake.setPosition(x*8, y*8-72)
		ennemis.append(stake)

	tortuesLayer = tm.get_layer_by_name("tortues")
	for x,y,image in tortuesLayer.tiles():
		tortue = Tortue(FPS, playfield, obstacles)
		tortue.setPosition(x*8, y*8-24)
		ennemis.append(tortue)

	booLayer = tm.get_layer_by_name("boo")
	for x,y,image in booLayer.tiles():
		boo = Boo(FPS, playfield, obstacles)
		boo.setPosition(x*8, y*8-8)
		ennemis.append(boo)

	poisonivyLayer = tm.get_layer_by_name("poisonivy")
	for x,y,image in poisonivyLayer.tiles():
		poisonivy = PoisonIvy(FPS, playfield, obstacles)
		poisonivy.setPosition(x*8, y*8-8)
		ennemis.append(poisonivy)

	# On charge mario et on le positionne par rapport à la map
	mario = Mario(FPS, playfield, obstacles)
	marioposition = tm.get_object_by_name("mario")
	mario.setPosition(marioposition.x, marioposition.y)

	lifeCounter = Digits()
	lifeCounter.setPosition(WIDTH-52-20, 14)
	lifeCounter.setDigit(NBLIFE)

	score = Score()
	score.setPosition(0, 14)
	score.setScore(0)

	# on cache le curseur de la souris
	pygame.mouse.set_visible(False)

	# On démarre la musique en boucle
	if MUSIC:
		pygame.mixer.music.play(loops=-1)

	# ##################################################
	# ##################################################
	# Ecran d'acceuil
	# ##################################################
	# ##################################################
	imageAccueil = pygame.image.load("splashscreens/principal.png").convert()
	(w,h) = pygame.display.get_surface().get_size()
	pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,w,h))
	(iw,ih) = imageAccueil.get_size()
	screen.blit(imageAccueil, ((w-iw)/2,(h-ih)/2))

	clock = pygame.time.Clock()
	ecranprincipal = True
	while ecranprincipal:
		# on limite l'affichage à FPS images par secondes
		time = clock.tick(FPS)	
		
		# on gère les evenements clavier
		###################
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				# on quitte si on appui sur la touche ESC
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit(0)
			# on gère l'appui sur la barre espace
				elif event.key == pygame.K_SPACE:
					ecranprincipal = False

		pygame.display.flip()


	# ##################################################
	# ##################################################
	# Boucle principale du jeu
	# ##################################################
	# ##################################################
	header = pygame.image.load("splashscreens/mariopy.png").convert_alpha()

	levelfinished = False
	clock = pygame.time.Clock()
	while not levelfinished and lifeCounter.getDigit()>0:
		# on limite l'affichage à FPS images par secondes
		time = clock.tick(FPS)	
		
		# on gère les evenements clavier
		###################
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				# on quitte si on appui sur la touche ESC
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit(0)
			# on gère les touches de direction et la barre espace pour diriger le personnage
				elif event.key == pygame.K_LEFT:
					mario.goLeft()
				elif event.key == pygame.K_RIGHT:
					mario.goRight()
				elif event.key == pygame.K_SPACE:
					mario.jump()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					mario.stopLeft()
				elif event.key == pygame.K_RIGHT:
					mario.stopRight()

		# on met a jour les sprites
		###################
		mario.update(time)

		# l'eau
		for w in watersprites:
			w.update(time)

		# les ennemis
		for ennemi in ennemis:
			ennemi.update(time)

		# les tiles
		for objet in objets:
			objet.update(time)

		# on gère les collisions entre mario et les zones mortelles
		if mario.rect.collidelist(zonesmortelles) != -1:
			lifeCounter.setDigit(0) # on perd toutes les vies d'un coup...

		# on gère les collisions entre mario et les zones de fin
		if mario.rect.collidelist(zonesfin) != -1:
			levelfinished = True # on a fini le niveau

		# on gère les collisions entre mario et les objets
		# pour les ramasser
		objet_a_ramasser = pygame.sprite.spritecollideany(mario,objets)
		if objet_a_ramasser:
			objet_a_ramasser.collision()
			score.addScore(objet_a_ramasser.getReward())
			objets.remove(objet_a_ramasser)

		# on gère les collisions entre mario et les enemis
		collision_ennemi = pygame.sprite.spritecollideany(mario,ennemis, pygame.sprite.collide_mask)
		if collision_ennemi:
			if mario.injured(): # seulement si mario n'a pas deja un dommage en cours de traitement (pour eviter de perdre trop de vies d'un coup)
				collision_ennemi.estTouche()
				lifeCounter.decDigit()
				if lifeCounter.getDigit() == 1:
					if MUSIC: # on change de musique si il ne reste plus qu'une vie
						pygame.mixer.music.load('soundtracks/03 - Hurry - Super Mario Bros.mp3')
						pygame.mixer.music.play(loops=-1)



		# on nettoie la liste et on supprime tous les ennemis qui sont morts
		# (a cause de l'animation cela peut prendre un peu de temps)
		for ennemi in ennemis:
			if ennemi.estMort(): # on supprime de la liste tous les ennemis qui sont morts
				ennemis.remove(ennemi)

		# on met a jour l'affichage du score et des vies
		lifeCounter.update(time)
		score.update(time)

		# on gere le décalage du playfield pour faire un scrolling si besoin ainsi que les animations
		###################

		# on incrémente le compteur utilisé pour les animations et les sprites
		COMPTEUR += 1

		# on active le scrolling de l'ecran si le sprite est en bordure
		mariopositionx = mario.getPosition().x
		if(mariopositionx-POSITION<200):
			MOUVEMENTX = -PASX
		elif(mariopositionx-POSITION>WIDTH-200):
			MOUVEMENTX = PASX
		else:
			MOUVEMENTX = 0

		# on déplace la position relative de l'ecran si un mouvement de scrolling est en cours
		POSITION = POSITION + MOUVEMENTX
		
		# on limite la position de manière à le pas dépasser la map
		if POSITION < 0:
			POSITION = 0
		if POSITION > playfield.width-WIDTH:
			POSITION = playfield.width-WIDTH

		# on corrige la position de mario si il sort de la fenetre visible
		positionMario = mario.getPosition()
		if positionMario.x<POSITION:
			mario.setPosition(POSITION, positionMario.y)
		if positionMario.x+positionMario.width>=POSITION+WIDTH:
			mario.setPosition(POSITION+WIDTH-positionMario.width, positionMario.y)

		# on affiche la map
		###################

		# on crée une grosse image qui contient tout le playfield
		buffer = pygame.Surface((playfield.width, playfield.height))

		# on dessine le playfield
		# 1. Le fond
		layer = tm.get_layer_by_name("fond")
		for x, y, image in layer.tiles():
			buffer.blit(image,(x*8+POSITION/2,y*8))

		# 2. Les arbres
		layer = tm.get_layer_by_name("arbres")
		for x, y, image in layer.tiles():
			buffer.blit(image,(x*8+POSITION/4,y*8))

		# 3. Les nuages
		layer = tm.get_layer_by_name("nuages")
		for x, y, image in layer.tiles():
			buffer.blit(image,(x*8+POSITION/2-COMPTEUR/16,y*8))

		# 4. Le plateau de jeu
		layer = tm.get_layer_by_name("plateau")
		for x, y, image in layer.tiles():
			buffer.blit(image,(x*8,y*8))

		# on dessine tous les sprites
		# ##########################

		# les objets
		for objet in objets:
			buffer.blit(objet.image, objet.rect)

		# les ennemis
		for ennemi in ennemis:
			buffer.blit(ennemi.image, ennemi.rect)

		# Mario
		buffer.blit(mario.image,mario.rect)

		# l'eau en dernier car c'est un overlay
		for w in watersprites:
			buffer.blit(w.image, w.rect)

		# on dessine la toute derniere map en avant plan
		# 5. Le plateau en avant plan
		layer = tm.get_layer_by_name("plateaufront")
		for x, y, image in layer.tiles():
			buffer.blit(image,(x*8,y*8))

		###################
		# on met à jour les dessins sur l'ecran
		# Note: on a une carte en mémoire qui fait l'ensemble du Tileset, on affiche qu'une sous partie de la carte
		# en s'appuyant sur la position de scrolling (il faut donc décaler la grande image à gauche pour faire avancer
		# virtuellement la fenetre de scrolling sur le Tileset)
		pygame.draw.rect(screen, (255,255,255),(0,0,WIDTH,81))
		screen.blit(header, (180,14))
		screen.blit(lifeCounter.image, lifeCounter.rect)
		screen.blit(score.image, score.rect)

		screen.blit(buffer, (-POSITION, 80))
	

		# on met à jour l'affichage ecran
		pygame.display.flip()

	# ##################################################
	# ##################################################
	# Ecran de fin
	# ##################################################
	# ##################################################

	# on affiche le logo winner ou game over centré sur l'ecran de jeu
	if levelfinished:
		winner = pygame.image.load("splashscreens/winner.png").convert_alpha()
		(winnerWidth, winnerHeight) = winner.get_size()
		screen.blit(winner, pygame.Rect( (WIDTH-winnerWidth)/2, 80+(HEIGHT-winnerHeight)/2, winnerWidth, winnerHeight ) )
		if MUSIC: # musique de winner
			pygame.mixer.music.load('soundtracks/04 - Area Clear.mp3')
			pygame.mixer.music.play()
	else:
		gameover = pygame.image.load("splashscreens/game over.png").convert_alpha()
		(gameoverWidth, gameoverHeight) = gameover.get_size()
		screen.blit(gameover, pygame.Rect( (WIDTH-gameoverWidth)/2, 80+(HEIGHT-gameoverHeight)/2, gameoverWidth, gameoverHeight ) )
		if MUSIC: # musique de game over
			pygame.mixer.music.load('soundtracks/16 - Game Over.mp3')
			pygame.mixer.music.play()

	pygame.display.flip()

	clock = pygame.time.Clock()
	ecranprincipal = True
	while ecranprincipal:
		# on limite l'affichage à FPS images par secondes
		time = clock.tick(FPS)	
		
		# on gère les evenements clavier
		###################
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				# on quitte si on appui sur la touche ESC
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit(0)
			# on gère l'appui sur la barre espace
				elif event.key == pygame.K_SPACE:
					ecranprincipal = False
