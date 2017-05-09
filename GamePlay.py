### Programming Paradigms Final Project ###

from random import randint
import sys, pygame
import math, time
from Setup import Setup


# Screen Config Global Variables
screenWidth, screenHeight = 1000, 800
screen = pygame.display.set_mode((screenWidth, screenHeight))


# GameSpace Class
class gameSpace(object):

	# Initializes all necessary variable
	def __init__(self):

		# Initialize window variables and several labels
		pygame.init()
		self.size = self.width, self.height = screenWidth, screenHeight
		self.white = 255,255,255
		self.screen = pygame.display.set_mode(self.size)
		self.waitFont = pygame.font.SysFont("freeserif", 100)
		self.wait = self.waitFont.render("Player 2 has not connected, please wait...", 1, (0,0,0))
		self.bye = self.waitFont.render("Goodbye!", 1, (0,0,0))
		self.player_num = 1

		# Setup game mode and difficulty
		self.connected = 0
		self.setup = Setup()
		self.mode, self.diff = self.setup.run_setup()
		if self.mode == 0  and self.diff == 0:
			# Goodbye Screen
			sys.exit()
		# If mode 2 selected, set a variable for other score
		elif self.mode == 2:
			self.other_score = 0

		# Set Game Variables
		self.player = Player(self.player_num, "images/players/default.png")
		if self.mode == 1:
			self.computer = Computer(self.diff, "images/players/default.png")
			self.ball = Ball(self.player, self.diff, "images/balls/soccerBall.png", self.computer)
		else:
			self.ball = Ball(self.player, self.diff, "images/balls/soccerBall.png")

	# Runs one game loop
	def play(self):

		# If playing online but P2 hasn't connected, wait
		if self.mode == 2 and self.player_num == 1 and self.connected == 0:
			screen.blit(self.wait, (150, 400))

		# check for system exit
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			sys.exit()

		# Set white background
		self.screen.fill(self.white)

		# Movement Functions
		self.player.keyHandler()
		self.ball.move()
		if self.mode == 1:
			self.computer.move()

		# Draw all necessary sprites
		self.ball.draw()
		self.player.draw()
		self.player.goal()
		self.computer.draw()
		self.computer.goal()

		# Display all blits
		pygame.display.flip()

	# Function sets player number
	def set_player(self, num):
		self.player_num = num

	# Indicates player 2 is connected if necessary
	def connected(self):
		self.connected = 1

	# Function receives other player position
	def other_player_pos(self, data):
		return

	# Function returns current player position
	def player_pos(self):
		return

	# function displays lost connection screen
	def connection_lost(self):
		return

	# Returns game mode
	def get_mode(self):
		return self.mode

	# Indicates if game is over
	def game_over(self):

		if self.mode == 1:
			if self.player.get_score() == 10 or self.computer.get_score() == 10:
				return 1
			else:
				return 0

		elif self.mode == 2:
			if self.player.get_score() == 10 or self.other_score == 10:
				return 1
			else:
				return 0

	# Screen say good bye as you exit
	def goodbye(self):
		screen.blit(self.bye, (425, 400))
		pygame.display.flip()
		time.sleep(3)


# Player Class
class Player(pygame.sprite.Sprite):

	# Build player according to image and player num
	def __init__(self, player_num, img):

		# Set image variables
		self.barWidth = 30
		self.barHeight = 80
		self.image = pygame.image.load(img)
		self.image = pygame.transform.scale(self.image, (self.barWidth, self.barHeight))
		self.rect = self.image.get_rect()
		self.rect.y = 360

		# Determine side to start on by player number
		if player_num == 1:
			self.rect.x = 100
		else:
			self.rect.x = 900

		# Score variables
		self.score = 0
		self.scoreKeeper = pygame.font.SysFont("freeserif", 25)

	# Key press handler
	def keyHandler(self):

		# Record any pressed key, move accordingly
		key = pygame.key.get_pressed()

		# Move up without leaving window
		if key[pygame.K_DOWN]:
			if self.rect.y + self.barHeight < screenHeight:
				self.rect.y += 20
			else:
				self.rect.y = screenHeight - self.barHeight

		# Move down without leaving window
		elif key[pygame.K_UP]:
			if self.rect.y  > 0:
				self.rect.y -= 20
			else:
				self.rect.y = 0

		# Leave game
		if key[pygame.K_q]:
			sys.exit()

	# Update corner score
	def goal(self):
		scoreBlit = self.scoreKeeper.render(str(self.score), 1, (0,0,0))
		screen.blit(scoreBlit, (32, 16))
		if self.score == 10:
			print ("player 1 wins")

	# Draw Player to screen
	def draw(self):
		screen.blit(self.image, self.rect)

	# Return current player score
	def get_score(self):
		return self.score

	# Adds one to score
	def up_score(self):
		self.score += 1


# Computer Class
class Computer(pygame.sprite.Sprite):

	# Set computer player up
	def __init__(self, diff, img):

		# Set image variables
		self.barWidth = 30
		self.barHeight = 80
		self.image = pygame.image.load(img)
		self.image = pygame.transform.scale(self.image, (self.barWidth, self.barHeight))
		self.rect = self.image.get_rect()
		self.rect.y = 360
		self.rect.x = 900

		# Other variables
		self.difficulty = diff
		self.score = 0
		self.scoreKeeper = pygame.font.SysFont("freeserif", 25)

	# Update corner score
	def goal(self):
		scoreBlit = self.scoreKeeper.render(str(self.score), 1, (0,0,0))
		screen.blit(scoreBlit, (968, 16))
		if self.score == 10:
			print ("player 2 wins")

	# Blit image to screen
	def draw(self):
		screen.blit(self.image, self.rect)

#########################################################
#							#
#       Chisom I need you to do this function,		#
#       It needs to follow the follow the ball based	#
#	on the variable self.difficulty			#
#							#
#########################################################

	def move(self):
		return

	# Return score
	def get_score(self):
		return self.score

	# Adds one to score
	def up_score(self):
		self.score += 1


# Ball Class
class Ball(pygame.sprite.Sprite):

	# Initialize ball in middle
	def __init__(self, player, diff, img, computer=None):

		# Set image variables
		self.image = pygame.image.load(img)
		self.image = pygame.transform.scale(self.image, (10, 10))
		self.rect = self.image.get_rect()
		self.rect.x = 500
		self.rect.y = 400
		self.size = 10

		# Ball speed according to difficulty, use random angle
		deg = randint(15, 75)
		rad = (deg*math.pi)/180

		if diff == 1:
			self.diff = 10
		elif diff == 2:
			self.diff = 20
		elif diff == 3:
			self.diff = 30

		self.Speedx = self.diff*math.cos(rad)
		self.Speedy = self.diff*math.sin(rad)

		# Player and computer instances
		self.play = player
		self.comp = computer

	# Blit ball to screen
	def draw(self):
		screen.blit(self.image, self.rect)

	# Move ball according to speed and direction
	def move(self):
		self.rect.x += self.Speedx
		self.rect.y += self.Speedy

		# If ball hits top or bottom, switch direction
		if self.rect.y <= self.size:
			self.Speedy *= -1
		elif self.rect.y >= screenHeight-self.size:
			self.Speedy*= -1

		# If ball gets by one of the players, restart with random angle and add points
		if self.rect.x <= 0:
			self.Speedx *= -1
			self.rect.x = 500
			self.rect.y = 400

			# New random angle
			deg = randint(15, 75)
			rad = (deg*math.pi)/180
			self.Speedx = self.diff*math.cos(rad)
			self.Speedy = self.diff*math.sin(rad)

			self.comp.up_score()
		elif self.rect.x >= screenWidth-self.size:
			self.Speedx *= -1
			self.rect.x = 500
			self.rect.y = 400
			self.play.up_score()

		# If ball collides with one of players, switch direction
