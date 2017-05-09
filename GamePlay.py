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

		# Various screen fonts and labels
		self.byeFont = pygame.font.SysFont("freeserif", 100)
		self.winFont = pygame.font.SysFont("freeserif", 50)
		self.scoreKeeper = pygame.font.SysFont("freeserif", 25)
		self.wait = self.winFont.render("Player 2 has not connected, please wait...", 1, (0,0,0))
		self.bye = self.byeFont.render("Goodbye!", 1, (0,0,0))
		self.lost = self.winFont.render("Game Server Connection Lost.", 1, (0,0,0))

		# Setup game mode and difficulty
		self.player_num = 0
		self.connected = 0
		self.setup = Setup()
		self.mode, self.diff, self.player_img, self.ball_img = self.setup.run_setup()

		### Check chosen mode ###

		# If quit occurred, leave game
		if self.mode == 0:
			self.goodbye()

		# If player want to play computer, set that up
		elif self.mode == 1:
			self.player_num = 1
			self.connected = 1
			self.player = Player(self.player_num, self.player_img)
			self.computer = Computer(self.diff, self.player_img)
			self.ball = Ball(self.player, self.diff, self.ball_img, self.computer)

		# If mode 2 selected, set a variable for other score
		elif self.mode == 2:
			self.other_score = 0
			self.player = Player(self.player_num, self.player_img)
			self.ball = Ball(self.player, self.diff, self.ball_img)

			# Initialize other player attributes
			self.barWidth = 30
			self.barHeight = 80
			self.other_img = pygame.image.load(self.player_img)
			self.other_img = pygame.transform.scale(self.other_img, (self.barWidth, self.barHeight))
			self.other_rect = self.other_img.get_rect()
			self.other_rect.x = -50
			self.other_rect.y = 900

	# Function sets player number, cannot start mode 2 without this
	def set_player(self, num):
		self.player_num = num
		if self.player_num == 2:
			self.connected = 1
		self.player.set_pos(self.player_num)

	# Indicates player 2 is connected
	def connected(self):
		self.connected = 1

	# Runs one game loop
	def play(self):

		# If playing online but P2 hasn't connected, wait
		if self.connected == 0:
			screen.blit(self.wait, (150, 400))

		# check for system exit
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			sys.exit()

		# Set white background
		self.screen.fill(self.white)

		# Draw everything for mode 1
		if self.mode == 1:
			self.player.keyHandler()
			self.ball.move()
			self.ball.draw()
			self.player.draw()
			self.player.goal()
			self.computer.move()
			self.computer.draw()
			self.computer.goal()

		# Draw everything for mode 2
		else:
			self.player.keyHandler()
			self.ball.draw()
			self.player.draw()
			self.player.goal()

			# Draw other player, blit other score
			screen.blit(self.other_img, self.other_rect)
			scoreBlit = self.scoreKeeper.render(self.other_score, 1, (0,0,0))

			# Blit score in proper place
			if self.player_num == 2:
				screen.blit(scoreBlit, (32, 16))
			else:
				screen.blit(scoreBlit, (968, 16))

			# Check if other player won
			if self.other_score == 10:
				print ("other player wins")
				self.winner()

		# Display all blits
		pygame.display.flip()

	# Function receives other player position
	def update_other(self, data):
		info = data.split()
		self.other_rect.x = int(info[0])
		self.other_rect.y = int(info[1])
		self.other_score = info[2]
		self.ball.set_pos(int(info[3]), int(info[4]), float(info[5]))

	# Function returns current player position
	def player_pos(self):
		return self.ball.get_full_pos()

	# Returns game mode for main
	def get_mode(self):
		return self.mode

	# Indicates if game is over
	def game_over(self):

		# If playing computer, check those scores
		if self.mode == 1:
			if self.player.get_score() == 10 or self.computer.get_score() == 10:
				return 1
			else:
				return 0

		# If playing other player, check those scores
		elif self.mode == 2:
			if self.player.get_score() == 10 or self.other_score == 10:
				return 1
			else:
				return 0

	# function displays lost connection screen
	def winner(self):

		# Winner variable
		winner = 0

		# If playing computer, check those scores
		if self.mode == 1:
			if self.player.get_score() > self.computer.get_score():
				winner = 1
			else:
				winner = 2

		# If playing other player, check those scores
		elif self.mode == 2:
			if self.player.get_score() > self.other_score:
				winner = 1
			else:
				winner = 2

		self.screen.fill(self.white)
		self.win = self.winFont.render("Player " + str(winner) + " won the game!", 1, (0,0,0))
		screen.blit(self.win, (250, 300))
		pygame.display.flip()
		time.sleep(3)
		self.goodbye()

	# function displays lost connection screen
	def connection_lost(self):
		self.screen.fill(self.white)
		screen.blit(self.lost, (200, 300))
		pygame.display.flip()
		time.sleep(3)
		self.goodbye()

	# Screen say good bye as you exit
	def goodbye(self):
		self.screen.fill(self.white)
		screen.blit(self.bye, (300, 300))
		pygame.display.flip()
		time.sleep(3)
		sys.exit()

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
		elif player_num == 0:
			self.rect.x = 1100
		elif player_num == 2:
			self.rect.x = 900

		# Score variables
		self.score = 0
		self.scoreKeeper = pygame.font.SysFont("freeserif", 25)

	# Set x position after the fact
	def set_pos(self, player_num):
		if player_num == 1:
			self.rect.x = 100
		elif player_num == 2:
			self.rect.x = 900

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

	# Return necessary position info
	def get_pos(self):
		return str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.score)

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
		self.deg = randint(15, 75)
		self.rad = (self.deg*math.pi)/180

		if diff == 1:
			self.diff = 20
		elif diff == 2:
			self.diff = 30
		elif diff == 3:
			self.diff = 50

		self.Speedx = self.diff*math.cos(self.rad)
		self.Speedy = self.diff*math.sin(self.rad)

		# Player and computer instances
		self.play = player
		self.comp = computer

	# Returns player and ball position info
	def get_full_pos(self):
		pos = self.play.get_pos()
		return pos + " " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.rad)

	# Sets ball position from outside input
	def set_pos(self, x, y, rad):
		self.rect.x = x
		self.rect.y = y
		self.rad = rad

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
			self.rect.x = 500
			self.rect.y = 400

			# New random angle
			self.deg = randint(15, 75)
			self.rad = (self.deg*math.pi)/180
			self.Speedx = self.diff*math.cos(self.rad)
			self.Speedy = self.diff*math.sin(self.rad)

			self.comp.up_score()

		elif self.rect.x >= screenWidth-self.size:
			self.rect.x = 500
			self.rect.y = 400

			# New random angle
			self.deg = randint(15, 75)
			self.rad = (self.deg*math.pi)/180
			self.Speedx = self.diff*math.cos(self.rad)
			self.Speedy = self.diff*math.sin(self.rad)
			self.Speedx *= -1

			self.play.up_score()

		# If ball collides with one of players, switch direction

#########################################################
#							#
#       Chisom I need you to do collisions,		#
#       Just multiply x by -1 if there is a collision	#
#	with one of the players. Best way to detect	#
#	collisions is using the get_position funcs	#
#	from gs, and checking that against ball pos	#
#							#
#########################################################
