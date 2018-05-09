#anciennement Test 15 avril 2018


import pygame
import random
import os
from Constants import *
import time

pygame.init()

if os.path.isfile('Data/space_invaders.ttf'):

	FONT_40 = pygame.font.Font("Data/space_invaders.ttf", 40)
	FONT_20 = pygame.font.Font("Data/space_invaders.ttf", 20)
	FONT_10 = pygame.font.Font("Data/space_invaders.ttf", 10)
else:
	FONT_40 = pygame.font.SysFont('arial', 40)
	FONT_20 = pygame.font.SysFont('arial', 20)
	FONT_10 = pygame.font.SysFont('arial', 10)


SCORE_STATIC = FONT_20.render("SCORE  ", True, WHITE)
LIVES_STATIC = FONT_20.render("LIVES  ", True, WHITE)
init_coordx_lives = 100

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("test 15 avril 2018")
clock = pygame.time.Clock()

class Cell (pygame.sprite.Sprite):

	def __init__(self, x, y, couleur, cote = COTE_SNAKE):
		super(Cell, self).__init__()
		self.image = pygame.Surface([cote, cote])
		self.image.fill(couleur)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y 

	def __str__(self):
		return "Cell[%d,%d]"%(self.rect.x, self.rect.y)

class Head (Cell):
	
	def __init__(self,x, y, couleur, cote = COTE_SNAKE, direction ="RIGHT"):
		super(Head, self).__init__(x,y,couleur,cote)
		self.direction = direction
		self.score = 0
		self.lives = 3
		self.snake = []
		self.snake.append(self)

	def update(self):

		previousPosHeadX = self.rect.x
		previousPosHeadY = self.rect.y
		
		if self.direction == "UP":
			self.rect.y -= DEPLACEMENT_SNAKE + SPACE_BETWEEN_TAIL + COTE_SNAKE
		elif self.direction == "DOWN":
			self.rect.y += DEPLACEMENT_SNAKE  + SPACE_BETWEEN_TAIL + COTE_SNAKE
		elif self.direction == "LEFT":
			self.rect.x -= DEPLACEMENT_SNAKE + SPACE_BETWEEN_TAIL + COTE_SNAKE
		elif self.direction == "RIGHT":
			self.rect.x += DEPLACEMENT_SNAKE + SPACE_BETWEEN_TAIL + COTE_SNAKE

		
		
		for i in range(1,len(self.snake)):
			
			tempX = self.snake[i].rect.x
			tempY = self.snake[i].rect.y
			
			self.snake[i].rect.x = previousPosHeadX
			self.snake[i].rect.y = previousPosHeadY
			
			previousPosHeadX = tempX
			previousPosHeadY = tempY
			
	def resetPos(self):
		self.rect.x = 255
		self.rect.y = 255

	def __str__(self):
		return "Head[%d, %d]" % (self.rect.x, self.rect.y)

class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y, largeur, longueur):
		super(Wall,self).__init__()
		self.image = pygame.Surface([largeur, longueur])
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.largeur = largeur
		self.longueur = longueur

class App(object):

	def __init__(self):
		self.credits = 0
		self.gameStart = False
		self.snakeText = FONT_20.render(str("SNAKE!!!"), True, WHITE)
		self.insertCoinText = FONT_20.render(str("INSERT COIN! (PRESS 5)"), True, WHITE)
		self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
		self.pressStartText = FONT_20.render(str("Press 1 to start! "), True, WHITE)
		self.done = False
		self.all_sprite_list = pygame.sprite.Group()
		self.all_snake_list = pygame.sprite.Group()
		self.all_food_list = pygame.sprite.Group()
		self.all_wall_list = pygame.sprite.Group()
		self.head = Head(300,100, BLUE)
		self.startScreenDone = False
		self.appDone = False


	def makeWall(self):
		#def __init__(self, x, y, largeur, longueur):
		topWall = Wall(0,TOP_SCORE_SPACE,SIZE[0], EPAISSEUR_WALL)
		leftWall = Wall(0,TOP_SCORE_SPACE,EPAISSEUR_WALL , SIZE[1] - 85)
		rightWall = Wall(SIZE[0] - EPAISSEUR_WALL, TOP_SCORE_SPACE, 10, SIZE[1] -85)
		bottomWall = Wall(0, SIZE[1] - EPAISSEUR_WALL -TOP_SCORE_SPACE, SIZE[0], EPAISSEUR_WALL)
		self.all_wall_list.add(topWall)
		self.all_wall_list.add(leftWall)
		self.all_wall_list.add(rightWall)
		self.all_wall_list.add(bottomWall)
		#self.all_sprite_list.add(self.all_wall_list)
		print "wall made"

	def reInitEverything(self):
		self.__init__()

	def initEverything(self):
		pass

	def refreshStartScreen(self):
		self.startScreen()
		screen.fill(BLACK)	
		screen.blit(self.snakeText, (200, 15))
		if self.credits <1:
			screen.blit(self.insertCoinText, (100, 225))
		else:
			screen.blit(self.pressStartText, (100,225))
		
		self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
		screen.blit(self.creditsText, (SIZE[0] - 150, SIZE[1] - 30))

		pygame.display.update()

	def showLives(self):
		x = init_coordx_lives
		
		#FONT_20.render(str("SNAKE!!!"), True, WHITE)
		screen.blit(LIVES_STATIC, (10,10))

		for i in range(0, self.head.lives):
			pygame.draw.rect(screen, BLUE, (x,10,20,20))
			x +=25

	def showScore(self):
		screen.blit(SCORE_STATIC,  (SIZE[0] - SIZE[0]/4 , 10))

	def showCredits(self):
		self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
		print "credit texts dans showStartScreen: ", self.credits
		screen.blit(self.creditsText, (550,670))

	def startScreen(self):

		print "startScreenDone debut loop: ", self.startScreenDone

		while not self.startScreenDone:

			screen.fill(BLACK)	
			screen.blit(self.snakeText, (200, 15))
			if self.credits <1:
				screen.blit(self.insertCoinText, (100, 225))
			else:
				screen.blit(self.pressStartText, (100,225))
			
			self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
			screen.blit(self.creditsText, (SIZE[0] - 150, SIZE[1] - 30))

			pygame.display.update()
			
			self.startScreenDone = self.manageStartScreenInput()
			if self.startScreenDone:
				print "startScreenDone fin loop: ", self.startScreenDone

		
		'''
		screen.fill(BLACK)
		screen.blit(self.snakeText, (310,10))
		if self.credits < 1:
			screen.blit(self.insertCoinText, (240,350))
		else:
			screen.blit(self.pressStartText, (240,350))
		self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
		print "credit texts dans showStartScreen: ", self.credits
		screen.blit(self.creditsText, (550,670))
		pygame.display.update()
		'''

	def createInitSprites(self):
		
		cell1 = Cell(265,100, BLUE)
		'''cell2 = Cell(230,100, BLUE)
		cell3 = Cell(195,100, BLUE)
		cell4 = Cell(160,100, BLUE)
		cell5 = Cell(125,100, BLUE)
		'''
		food = Cell(300,300, RED, COTE_FOOD)

		self.head.snake.append(cell1)
		'''
		self.head.snake.append(cell2)
		self.head.snake.append(cell3)
		self.head.snake.append(cell4)
		self.head.snake.append(cell5)
		'''

		self.all_snake_list.add(cell1)
		
		#self.all_snake_list.add(cell2)
		#self.all_snake_list.add(cell3)
		#self.all_snake_list.add(cell4)
		#self.all_snake_list.add(cell5)
		
		self.all_sprite_list.add(cell1)
		
		#self.all_sprite_list.add(cell2)
		#self.all_sprite_list.add(cell3)
		#self.all_sprite_list.add(cell4)
		#self.all_sprite_list.add(cell5)
		
		self.all_sprite_list.add(self.all_snake_list)
		self.all_sprite_list.add(self.all_wall_list)
		self.all_sprite_list.add(self.head)
		self.all_sprite_list.add(food)
		#self.all_sprite_list.update()

	def manageStartScreenInput(self):

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return True
				
				elif event.key == pygame.K_1 and self.credits>0:
				#elif event.key == pygame.K_1:	
					print "key 1 in screen input"
					print "self.credit: ", self.credits
					return True
					#break
				
				elif event.key == pygame.K_5:
					self.credits +=1
					self.refreshStartScreen()

	def manageGameInput(self):

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return True

		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			#done = True
			return True
		elif keys[pygame.K_UP] and self.head.direction != "DOWN":
			self.head.direction = "UP"
			print "up"
		elif keys[pygame.K_DOWN] and self.head.direction != "UP":
			self.head.direction = "DOWN"
		elif keys[pygame.K_LEFT] and self.head.direction != "RIGHT":
			self.head.direction = "LEFT"
		elif keys[pygame.K_RIGHT] and self.head.direction != "LEFT":
			self.head.direction = "RIGHT"


	def mainLoop(self):

		screen.fill(BLACK)
		self.makeWall()		
		self.createInitSprites()
		self.showLives()
		self.showScore()
		self.showCredits()

		while not self.appDone:
			#print "mainLoop"
			

			#pygame.display.update()


			
			self.all_sprite_list.draw(screen)
			self.all_sprite_list.update()
			pygame.display.update()
			clock.tick(60)
			self.appDone = self.manageGameInput()

    	#mainDone = False

    	'''
    	
    	while not mainDone:

			screen.fill(BLACK)

			

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainDone = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						print "esc in mainLoop"
						mainDone = True

			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				print ("escape keys")
				mainDone = True
			elif keys[pygame.K_UP] and self.head.direction != "DOWN":
				self.head.direction = "UP"
			elif keys[pygame.K_DOWN] and self.head.direction != "UP":
				self.head.direction = "DOWN"
			elif keys[pygame.K_LEFT] and self.head.direction != "RIGHT":
				self.head.direction = "LEFT"
			elif keys[pygame.K_RIGHT] and self.head.direction != "LEFT":
				self.head.direction = "RIGHT"

			
			print ("boo")
			self.showLives()
			self.all_sprite_list.draw(screen)
			self.all_sprite_list.update()


			pygame.display.update()
			clock.tick(60)
		'''
			


def validFood(x,y):
	if (abs(x - head.rect.x) <= COTE_FOOD and abs(y - head.rect.y) <= COTE_FOOD):
		return False
	else:
		return True
	
def randomFood():
	x = random.randrange(EPAISSEUR_WALL, SIZE[0] - EPAISSEUR_WALL - COTE_FOOD)
	y = random.randrange(TOP_SCORE_SPACE, SIZE[1] - EPAISSEUR_WALL - COTE_FOOD)
	while not  validFood(x,y):
		x = random.randrange(EPAISSEUR_WALL, SIZE[0] - EPAISSEUR_WALL - COTE_FOOD)
		y = random.randrange(TOP_SCORE_SPACE, SIZE[1] - EPAISSEUR_WALL - COTE_FOOD)
	food.rect.x = x
	food.rect.y = y

if __name__ == '__main__':
    app = App()

    #screen.fill(BLACK)
    #app.startScreen()
    app.mainLoop()

'''
randomFood()

done = False

while not done:

	screen.fill(BLACK)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		done = True
	elif keys[pygame.K_UP] and head.direction != "DOWN":
		head.direction = "UP"
	elif keys[pygame.K_DOWN] and head.direction != "UP":
		head.direction = "DOWN"
	elif keys[pygame.K_LEFT] and head.direction != "RIGHT":
		head.direction = "LEFT"
	elif keys[pygame.K_RIGHT] and head.direction != "LEFT":
		head.direction = "RIGHT"

	if pygame.sprite.collide_rect(head, food):
		head.score += POINT
		#coordXLastCell = head.snake[len(head.snake) -1].rect.x
		#coordYLastCell = head.snake[len(head.snake) -1].rect.y
		# - 2000 pour ne pas que la cellule apparaisse dans l'ecran
		cell = Cell(head.rect.x -2000, head.rect.y, BLUE, COTE_TAIL)
		#cell = Cell(coordXLastCell, coordYLastCell, BLUE, COTE_TAIL)
		head.snake.append(cell)
		all_snake_list.add(cell)
		all_sprite_list.add(cell)
		randomFood()

	if pygame.sprite.spritecollide(head,all_wall_list, False):
		print "boom wall"
		if head.lives < 1:
			gameOver = FONT_20.render(str("Game Over!"), True, WHITE)
			screen.blit(gameOver, (SIZE[0]/2, SIZE[1]/2))
			time.sleep(1)
		head.lives -= 1

	if pygame.sprite.spritecollide(head,all_snake_list, False):
		print "boom snake"
		boomSnake = FONT_20.render(str("Boom snake!"), True, WHITE)
		screen.blit(boomSnake, (SIZE[0]/2, SIZE[1]/2))
		time.sleep(1)
		head.lives -= 1
		
	
	theScoreP1 = FONT_20.render(str(head.score), True, WHITE)
	theLivesP1 = FONT_20.render(str(head.lives), True, WHITE)

	screen.blit(LIVES_STATIC, (10, 10))
	screen.blit(SCORE_STATIC,  (SIZE[0] - SIZE[0]/4 , 10))
	screen.blit(theScoreP1, (SIZE[0] - 40 , 10))
	
	showLives()
	all_sprite_list.draw(screen)
	all_sprite_list.update()
	pygame.display.update()


	clock.tick(10)


pygame.quit()

'''	



'''
    while not app.done:
    	
    	keys = pygame.key.get_pressed()
    	if keys[pygame.K_ESCAPE]:
    		app.done = True

    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			app.done = True
    		elif event.type ==pygame.KEYDOWN:
    			if event.key == pygame.K_5:
    				app.credits +=1
    				#pygame.display.update()
    				app.refreshStartScreen()
    			elif event.key == pygame.K_1 and app.credits>0:
    				app.mainLoop()
    			elif event.key == pygame.K_ESCAPE:
    				app.done = True
    		#pygame.display.update()


    pygame.quit()
    '''

#for cell in head.snake:
#	print cell
#print "len(snake):", len(head.snake)



#VIEUX TRUCS POUR FAIRE APPARAITRE BCP DE FOOD ALEATOIREMENT SUR L'ECRAN ET VALIDER
#QU'IL NE S'EMBARQUE PAS UNE PAR DESSUS L'AUTRE	
"""def makeFoodMultiple():
	
	all_food_list.add(Food(random.randrange(0, SIZE[0] - COTE_FOOD),random.randrange(0,SIZE[1] - COTE_FOOD)))
	for i in range (0,30):
		x = random.randrange(0, SIZE[0] - COTE_FOOD)
		y = random.randrange(0, SIZE[1] - COTE_FOOD)
		if validFood(x,y):
			food = Food(x,y)
			all_food_list.add(food)
			all_sprite_list.add(food)

def validFoodGroup(x,y):
	for food in all_food_list:
		if abs(x - food.rect.x) <=COTE_FOOD and abs(y - food.rect.y <=COTE_FOOD):
			return False
	return True
"""
#makeFoodMultiple()


'''
class Snake(pygame.sprite.Sprite):

	def __init__(self,x,y, cote = COTE_SNAKE, direction = 1):
		super(Snake,self).__init__()
		self.image = pygame.Surface([cote, cote])
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.direction = direction
		self.score = 0
		self.lives = 3


	def update(self):
		if self.direction == "UP":
			self.rect.y -= DEPLACEMENT_SNAKE
		elif self.direction == "DOWN":
			self.rect.y += DEPLACEMENT_SNAKE
		elif self.direction == "LEFT":
			self.rect.x -= DEPLACEMENT_SNAKE
		elif self.direction == "RIGHT":
			self.rect.x += DEPLACEMENT_SNAKE

	def resetPos(self):
		self.rect.x = 255
		self.rect.y = 255

	def __str__(self):
		return "Snake[%d,%d]"%(self.rect.x, self.rect.y)

class Food(pygame.sprite.Sprite):
	def __init__(self, x,y, cote = COTE_FOOD):
		super(Food,self).__init__()
		self.image = pygame.Surface([cote,cote])
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	
	def __str__(self):
		return "Food[%d,%d]"%(self.rect.x, self.rect.y)

'''