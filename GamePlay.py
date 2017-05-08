### Programming Paradigms Final Project ###

import sys, pygame
import math

screenWidth, screenHeight = 1000, 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
### Gameplay Classes ###


# GameSpace Class
class gameSpace(object):
	def main(self):
		pygame.init()
		self.size = self.width, self.height = screenWidth, screenHeight
		self.white = 255,255,255
		self.screen = pygame.display.set_mode(self.size)
		#step 2
		self.clock = pygame.time.Clock()
		self.player = Player(self)
		self.computer = Computer(self)
		self.ball = Ball(self)

		crashed = False
		while not crashed:
			event = pygame.event.poll()
			if event.type == pygame.QUIT:
				crashed = True
			self.clock.tick(60)
			self.player.keyHandler()
			self.screen.fill(self.white)
			#self.player.tick()
			#self.deathStar.tick()
			self.ball.draw()
			self.screen.blit(self.player.image, self.player.rect)
			self.screen.blit(self.computer.image, self.computer.rect)
			#self.screen.blit(self.ball.image, self.ball.rect)
			pygame.display.flip()

# Player Class
class Player(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.score = 0 #score
		self.image = pygame.image.load('images/players/default.png')
		self.originalImage = self.image
		self.rect = self.image.get_rect()
		self.rect.centerx = 300
		self.rect.centery = 500
		self.angle = 0
		self.resize(4)

	def keyHandler(self):
		key = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()
		mv = 5
		if key[pygame.K_UP]:
			self.rect = self.rect.move(0, -mv)
		elif key[pygame.K_DOWN]:
			self.rect = self.rect.move(0, mv)

		if key[pygame.K_ESCAPE]:
			gs.running = 0

	def resize(self, amnt):
		self.size = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (int(self.size[0]/amnt), int(self.size[1]/amnt)))

	def goal(self):
		scoreBlit = self.scoreFont.render(str(self.score), 1, (255, 255, 255))
		screen.blit(scoreBlit, (32, 16))
		if self.score == 10:
			print ("player 1 wins")
			exit()




# Computer Class
class Computer:
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.score = 0 #score
		self.image = pygame.image.load('images/players/default.png')
		self.originalImage = self.image
		self.rect = self.image.get_rect()
		self.rect.centerx = 1100
		self.rect.centery = 500
		self.angle = 0
		self.resize(4)

	def keyHandler(self):
		key = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()
		mv = 5
		if key[pygame.K_w]:
			self.rect = self.rect.move(0, -mv)
		elif key[pygame.K_s]:
			self.rect = self.rect.move(0, mv)

		if key[pygame.K_ESCAPE]:
			gs.running = 0

	def resize(self, amnt):
		self.size = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (int(self.size[0]/amnt), int(self.size[1]/amnt)))

	def goal(self):
		scoreBlit = self.scoreFont.render(str(self.score), 1, (255, 255, 255))
		screen.blit(scoreBlit, (32, 16))
		if self.score == 10:
			print ("player 2 wins")
			exit()


# Setup Class
#class Setup:


# Ball Class
class Ball:
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.image.load('images/balls/yellowPingPongBall.png')
		#self.originalImage = self.image
		#self.rect = self.image.get_rect()
		self.size = 20
		self.x = 500
		self.y = 300
		#self.resize(30)
		self.Speedx = 4
		self.Speedy = 4

	#def resize(self, amnt):
	#	self.size = self.image.get_size()
	#	self.image = pygame.transform.scale(self.image, (int(self.size[0]/amnt), int(self.size[1]/amnt)))

	def draw(self):
		pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.size, 0)

	def move(self):
		self.x += self.Speedx
		self.y += self.Speedy

		if self.y <= 0:
			self.Speedy *= -2
		elif self.y >= screenHeight-self.size:
			self.Speedy*= -2
 
                if self.x <= 0:
                        self.__init__()
                        enemy.score += 1
                elif self.x >= SCR_WID-self.size:
                        self.__init__()
                        self.speed_x = 3
                        player.score += 1



if __name__ == '__main__':
	gs = gameSpace()
	gs.main()