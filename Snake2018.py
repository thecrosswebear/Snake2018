#anciennement Test 15 avril 2018

# test git

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
GAME_OVER = FONT_20.render(str("Game Over !"), True, WHITE)
BOOM_SNAKE = FONT_20.render(str("Boom Snake !"), True, WHITE)
BOOM_WALL = FONT_20.render(str("Boom wall !"), True, WHITE)
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

'''
class Head (Cell):
	
	def __init__(self,x, y, couleur, cote = COTE_SNAKE, direction ="RIGHT"):
		super(Head, self).__init__(x,y,couleur,cote)
		self.direction = direction
		self.score = 0
		self.lives = 3
		self.snake = []
		self.snake.append(self)

'''

class Head (pygame.sprite.Sprite):

	def __init__(self, x,y, couleur = BLUE, cote = 30):
		super(Head, self).__init__()
		self.image = pygame.Surface([cote,cote])
		self.image.fill(couleur)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.direction = ""
		self.score = 0
		self.lives = 2
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
			
			#previousPosHeadX = self.rect.x
			#previousPosHeadY = self.rect.y

			tempX = self.snake[i].rect.x
			tempY = self.snake[i].rect.y
			
			self.snake[i].rect.x = previousPosHeadX
			self.snake[i].rect.y = previousPosHeadY
			
			previousPosHeadX = tempX
			previousPosHeadY = tempY
			
	def resetPos(self):
		self.rect.x = 255
		self.rect.y = 255
		self.snake = []
		self.snake.append(self)

		'''for i in range(1,len(self.snake)):
			
			tempX = self.snake[i].rect.x
			tempY = self.snake[i].rect.y
			
			self.snake[i].rect.x = previousPosHeadX
			self.snake[i].rect.y = previousPosHeadY
			
			previousPosHeadX = tempX
			previousPosHeadY = tempY
		'''

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
		self.snakeTextFont = FONT_20.render(str("SNAKE!!!"), True, WHITE)
		self.snakeText = "SNAKE!!!"
		self.insertCoinText = FONT_20.render(str("INSERT COIN! (PRESS 5)"), True, WHITE)
		self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
		self.pressStartText = FONT_20.render(str("Press 1 to start! "), True, WHITE)
		self.done = False
		self.all_sprite_list = pygame.sprite.Group()
		self.all_snake_list = pygame.sprite.Group()
		self.all_food_list = pygame.sprite.Group()
		self.all_wall_list = pygame.sprite.Group()
		#self.head = Head(300,100, BLUE)
		self.head = Head(300,100, RED_BLUE)
		self.food = None
		self.startScreenDone = False
		self.appDone = False
		self.gameDone = False


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

		#self.startScreen()

		coordYAll = self.centerVerticalText()

		screen.fill(BLACK)	
		#screen.blit(self.snakeText, (300, 15))
		screen.blit(self.snakeTextFont, (self.centerRenderedText(self.snakeTextFont.get_width()), 15))
		if self.credits <1:
			#screen.blit(self.insertCoinText, (coordXInsertCoin, coordYAll))
			screen.blit(self.insertCoinText, (self.centerRenderedText(self.insertCoinText.get_width()), coordYAll))
		else:
			screen.blit(self.pressStartText, (self.centerRenderedText(self.pressStartText.get_width()), coordYAll))
		
		self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
		screen.blit(self.creditsText, (SIZE[0] - 150, SIZE[1] - 30))

		pygame.display.update()
		'''screen.fill(BLACK)	
		screen.blit(self.snakeText, (200, 15))
		if self.credits <1:
			screen.blit(self.insertCoinText, (100, 225))
		else:
			screen.blit(self.pressStartText, (100,225))
		
		self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
		screen.blit(self.creditsText, (SIZE[0] - 150, SIZE[1] - 30))

		pygame.display.update()
		'''
	def showLives(self):
		x = init_coordx_lives
		
		screen.blit(LIVES_STATIC, (10,10))

		for i in range(0, self.head.lives):
			pygame.draw.rect(screen, BLUE, (x,10,20,20))
			x +=25

	def showScore(self):
		theScore = FONT_20.render(str("SCORE: ") + str(self.head.score), True, WHITE)
		screen.blit(theScore,  (SIZE[0] - SIZE[0]/4 , 10))

	def showCredits(self):
		self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
		screen.blit(self.creditsText, (550,670))

	def centerRenderedText(self, textFontSize, screenSize = SIZE[0]):
		return (screenSize - textFontSize)/2

	def centerVerticalText(self, screenSize = SIZE[1], fontSize = 20):
		return ((screenSize - 20)/2)

	def startScreen(self):

		
		coordYAll = self.centerVerticalText()
		self.startScreenDone = False

		while not self.startScreenDone:

			#print "coordX centre: ", self.centerText(self.snakeText)
			screen.fill(BLACK)	
			#screen.blit(self.snakeText, (300, 15))
			screen.blit(self.snakeTextFont, (self.centerRenderedText(self.snakeTextFont.get_width()), 15))
			if self.credits <1:
				#screen.blit(self.insertCoinText, (coordXInsertCoin, coordYAll))
				screen.blit(self.insertCoinText, (self.centerRenderedText(self.insertCoinText.get_width()), coordYAll))
			else:
				screen.blit(self.pressStartText, (self.centerRenderedText(self.pressStartText.get_width()), coordYAll))
			
			self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
			screen.blit(self.creditsText, (SIZE[0] - 150, SIZE[1] - 30))

			pygame.display.update()
			
			self.startScreenDone = self.manageStartScreenInput()
			if self.startScreenDone:
				print "startScreenDone fin loop: ", self.startScreenDone
		

	def createInitSprites(self):
				
		self.food = Cell(300,300, RED, COTE_FOOD)
		self.resetRandomFood()
		self.all_sprite_list.add(self.all_snake_list)
		self.all_sprite_list.add(self.all_wall_list)
		self.all_sprite_list.add(self.head)
		self.all_sprite_list.add(self.food)
		
	def manageStartScreenInput(self):

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.appDone = True
					self.gameDone = True
					return True
				
				elif event.key == pygame.K_1 and self.credits>0:
					print "key 1 in screen input"
					print "self.credit: ", self.credits
					self.credits = self.credits -1
					return True
									
				elif event.key == pygame.K_5:
					self.credits +=1
					self.refreshStartScreen()

	def manageGameInput(self):

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_5:
					self.credits +=1
				if event.key == pygame.K_ESCAPE:
					print "escape in manageGameInput"
					self.appDone = True
					self.gameDone = True
					return True

		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			#done = True
			return True
		elif keys[pygame.K_UP] and self.head.direction != "DOWN":
			self.head.direction = "UP"
			#print "up"
		elif keys[pygame.K_DOWN] and self.head.direction != "UP":
			self.head.direction = "DOWN"
		elif keys[pygame.K_LEFT] and self.head.direction != "RIGHT":
			self.head.direction = "LEFT"
		elif keys[pygame.K_RIGHT] and self.head.direction != "LEFT":
			self.head.direction = "RIGHT"

	def validFood(self,x,y):
		if (abs(x - self.head.rect.x) <= COTE_FOOD and abs(y - self.head.rect.y) <= COTE_FOOD):
			return False
		else:
			return True
	
	def resetRandomFood(self):
		x = random.randrange(EPAISSEUR_WALL, SIZE[0] - EPAISSEUR_WALL - COTE_FOOD)
		y = random.randrange(TOP_SCORE_SPACE + EPAISSEUR_WALL , SIZE[1] - EPAISSEUR_WALL - COTE_FOOD - TOP_SCORE_SPACE)
		while not  self.validFood(x,y):
			x = random.randrange(EPAISSEUR_WALL, SIZE[0] - EPAISSEUR_WALL - COTE_FOOD)
			y = random.randrange(TOP_SCORE_SPACE, SIZE[1] - EPAISSEUR_WALL - COTE_FOOD)
		self.food.rect.x = x
		self.food.rect.y = y

	def resetPlayer(self):
		self.head.score = 0
		self.head.lives = 2
		print "reset player"


	def resetSnakePosition(self):
		self.head.rect.x = 255
		self.head.rect.y = 255
		self.head.snake = []
		self.head.snake.append(self.head)
		for cell in self.all_snake_list:
			cell.kill()
		self.head.direction = "None"
		
	def mainLoop(self):

		screen.fill(BLACK)
		self.makeWall()		
		self.createInitSprites()
		center_y = self.centerVerticalText()
		wait_a_bit = False
		self.gameDone = False
		self.resetPlayer()
		self.resetSnakePosition()

		while not self.gameDone:
			
			screen.fill(BLACK)
			self.showLives()
			self.showScore()
			self.showCredits()

			#collision avec bouffe
			if pygame.sprite.collide_rect(self.head, self.food):
				self.head.score += POINT
				# - 2000 pour ne pas que la cellule apparaisse dans l'ecran
				cell = Cell(self.head.rect.x -2000, self.head.rect.y, BLUE, COTE_TAIL)
				self.head.snake.append(cell)
				self.all_snake_list.add(cell)
				self.all_sprite_list.add(cell)
				self.resetRandomFood()
			
			#Collision avec mur
			if pygame.sprite.spritecollide(self.head,self.all_wall_list, False):
				
				#screen.blit(BOOM_WALL, (self.centerRenderedText(BOOM_WALL.get_width()), center_y))

				if self.head.lives < 1:
					screen.blit(GAME_OVER, (self.centerRenderedText(GAME_OVER.get_width()), center_y))
					wait_a_bit = True
					self.gameDone = True
					
					#break
				else:
					screen.blit(BOOM_WALL, (self.centerRenderedText(BOOM_WALL.get_width()), center_y))
					self.head.lives -= 1
					self.resetSnakePosition()
					self.resetRandomFood()
					wait_a_bit = True
				
			
			#Collision avec queue de serpent			
			if pygame.sprite.spritecollide(self.head, self.all_snake_list, False):
				
				if self.head.lives < 1:
					screen.blit(GAME_OVER, (self.centerRenderedText(GAME_OVER.get_width()), center_y))
					wait_a_bit = True
					self.gameDone = True

					#break
				else:
					screen.blit(BOOM_SNAKE, (self.centerRenderedText(BOOM_SNAKE.get_width()), center_y))
					self.head.lives -= 1
					self.resetSnakePosition()
					self.resetRandomFood()
					wait_a_bit = True
			
			self.all_sprite_list.draw(screen)
			self.all_sprite_list.update()
			pygame.display.update()
			if wait_a_bit:
				time.sleep(2)
				wait_a_bit = False
				#self.appDone = True
				#break
			clock.tick(10)
			blah = self.manageGameInput()
			if self.gameDone:
				self.food.kill()
				#self.resetPlayer()
			#self.gameDone = self.manageGameInput()

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
			




if __name__ == '__main__':
    app = App()
    #app.createInitSprites()
    

    #screen.fill(BLACK)
    while not app.appDone:
    	print("on recommence")
    	app.startScreen()
    	print ("snake head: "), app.head
    	app.mainLoop()
    #for cell in app.all_snake_list:
    #	print cell
    #print app.head
    #for sprite in app.all_sprite_list:
    #	print ("sprite.rect.x: "), sprite.rect.x
    #	print ("sprite.rect.y: "), sprite.rect.y

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