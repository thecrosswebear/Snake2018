#anciennement Test 15 avril 2018


import pygame
import random
from Constants import *
import time

pygame.init()

FONT_40 = pygame.font.Font("Data/space_invaders.ttf", 40)
FONT_20 = pygame.font.Font("Data/space_invaders.ttf", 20)
FONT_10 = pygame.font.Font("Data/space_invaders.ttf", 10)

SCORE_STATIC = FONT_20.render("SCORE: ", True, WHITE)
LIVES_STATIC = FONT_20.render("LIVES: ", True, WHITE)
init_coordx_lives = 100

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("test 15 avril 2018")
clock = pygame.time.Clock()

all_sprite_list = pygame.sprite.Group()
all_snake_list = pygame.sprite.Group()
all_food_list = pygame.sprite.Group()
all_wall_list = pygame.sprite.Group()


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
	#self,x,y, cote = COTE_SNAKE, direction = 1
	def __init__(self,x, y, couleur, cote = COTE_SNAKE, direction ="RIGHT"):
	#def __init__(self,x,y, cote = COTE_SNAKE, direction = 1):
		super(Head, self).__init__(x,y,couleur,cote)
		self.direction = direction
		self.score = 0
		self.lives = 3
		self.snake = []
		self.snake.append(self)

	def update(self):

		previousPosHeadX = self.rect.x
		previousPosHeadY = self.rect.y
		#previousHead = self.rect
		#print ("previousHead: "), self.rect

		if self.direction == "UP":
			self.rect.y -= DEPLACEMENT_SNAKE + SPACE_BETWEEN_TAIL + COTE_SNAKE
		elif self.direction == "DOWN":
			self.rect.y += DEPLACEMENT_SNAKE  + SPACE_BETWEEN_TAIL + COTE_SNAKE
		elif self.direction == "LEFT":
			self.rect.x -= DEPLACEMENT_SNAKE + SPACE_BETWEEN_TAIL + COTE_SNAKE
		elif self.direction == "RIGHT":
			self.rect.x += DEPLACEMENT_SNAKE + SPACE_BETWEEN_TAIL + COTE_SNAKE

		#print ("afterDeplacementHead: "),self.rect
		
		for i in range(1,len(self.snake)):
			#print ("iteration: "), i
			tempX = self.snake[i].rect.x
			tempY = self.snake[i].rect.y
			#print ("tempX debut For: "), tempX
			#print ("tempY debut For: "), tempY
			#print ("PreviousPos[%d,%d]"%(previousPosHeadX, previousPosHeadY))
			self.snake[i].rect.x = previousPosHeadX
			self.snake[i].rect.y = previousPosHeadY
			#print ("snake[i]:", self.snake[i])
			previousPosHeadX = tempX
			previousPosHeadY = tempY
			#print("nouvellePreviousPosHeadX: ", previousPosHeadX)
			#print ("nouvellePreviousPosHeadY: ", previousPosHeadY)
			
			#print self.snake[i]	
			#print ("dans for: len(self.snake): "), len(self.snake)

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

def makeWall():
	topWall = Wall(0,TOP_SCORE_SPACE,SIZE[0], EPAISSEUR_WALL)
	leftWall = Wall(0,TOP_SCORE_SPACE,EPAISSEUR_WALL, SIZE[1])
	rightWall = Wall(SIZE[0] - EPAISSEUR_WALL, TOP_SCORE_SPACE, 10, SIZE[1] )
	bottomWall = Wall(0, SIZE[1] - EPAISSEUR_WALL, SIZE[0], EPAISSEUR_WALL)
	all_wall_list.add(topWall)
	all_wall_list.add(leftWall)
	all_wall_list.add(rightWall)
	all_wall_list.add(bottomWall)
	all_sprite_list.add(all_wall_list)

class App(object):

	def __init__(self):
		self.credits = 0
		self.gameStart = False
		self.snakeText = FONT_20.render(str("SNAKE!!!"), True, WHITE)
		self.insertCoinText = FONT_20.render(str("INSERT COIN! (PRESS 5)"), True, WHITE)
		self.creditsText = FONT_20.render(str("credits  ") + str(self.credits), True, WHITE)
		self.pressStartText = FONT_20.render(str("Press 1 to start! "), True, WHITE)
		self.done = False

	def reInitEverything(self):
		self.__init__()

	def initEverything(self):
		pass

	def showStartScreen(self):
		theScoreP1 = FONT_20.render(str(head.score), True, WHITE)
		theLivesP1 = FONT_20.render(str(head.lives), True, WHITE)

		screen.blit(LIVES_STATIC, (10, 10))
		screen.blit(SCORE_STATIC,  (SIZE[0] - SIZE[0]/4 , 10))
		screen.blit(theScoreP1, (SIZE[0] - 40 , 10))


makeWall()
head = Head(300,100, BLUE)
#snake = []
#snake.append(head)


cell1 = Cell(265,100, BLUE)
cell2 = Cell(230,100, BLUE)
cell3 = Cell(195,100, BLUE)
cell4 = Cell(160,100, BLUE)
cell5 = Cell(125,100, BLUE)
head.snake.append(cell1)
head.snake.append(cell2)
head.snake.append(cell3)
head.snake.append(cell4)
head.snake.append(cell5)
all_snake_list.add(cell1)
all_snake_list.add(cell2)
all_snake_list.add(cell3)
all_snake_list.add(cell4)
all_snake_list.add(cell5)

all_sprite_list.add(cell1)
all_sprite_list.add(cell2)
all_sprite_list.add(cell3)
all_sprite_list.add(cell4)
all_sprite_list.add(cell5)

food = Cell(300,300, RED, COTE_FOOD)
all_sprite_list.add(all_wall_list)
all_sprite_list.add(head)
all_sprite_list.add(food)


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

def showLives():
	x = init_coordx_lives
	for i in range(0,head.lives):
		pygame.draw.rect(screen, BLUE, (x,10,20,20))
		x +=25


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

if __name__ == '__main__':
    app = App()

    while not app.done:

    	keys = pygame.key.get_pressed()
    	if keys[K.ESCAPE]:
    		app.done = True

    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			app.done = True
    		elif event.type ==pygame.KEYDOWN:
    			if event.key == pygame.K_5:
    				app.credits +=1
    			elif event.key == pygame.K_ESCAPE:
    				app.done = True


    pygame.quit()

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