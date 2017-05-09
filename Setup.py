### Programming Paradigms Final Project ###

import sys, pygame
import math

# Global Screen Variables
screenWidth, screenHeight = 1000, 800
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Setup Class
class Setup():
        def __init__(self):

                # Set return variables
                self.mode = 0
                self.diff = 0
                self.clock = pygame.time.Clock()

                # Set background image
                self.bckgnd_img = pygame.image.load("images/backgrounds/camoplague.jpg")

                ### Set font and labels ###

                # Title
                self.titleFont = pygame.font.SysFont("freeserif", 100)
                self.Title = self.titleFont.render("PONG", 1, (255,255,0))

                # Quit message
                self.quitFont = pygame.font.SysFont("freeserif", 25)
                self.quit = self.quitFont.render("To quit, press \"q\"", 1, (255,255,0))

                # Game Mode options
                self.optionFont = pygame.font.SysFont("freeserif", 50)
                self.option1 = self.optionFont.render("Enter 1 to play a computer", 1, (255,0,0))
                self.option2 = self.optionFont.render("Enter 2 to play another player", 1, (0,0,255))

                # Difficulty Options
                self.diffFont = pygame.font.SysFont("freeserif", 50)
                self.select_diff = self.diffFont.render("SELECT DIFFICULTY", 1, (0,0,0))
                self.diff1 = self.diffFont.render("Enter 1 for Beginner", 1, (255,0,0))
                self.diff2 = self.diffFont.render("Enter 2 for Intermediate", 1, (0,0,255))
                self.diff3 = self.diffFont.render("Enter 3 for Advanced", 1, (0,128,0))

        # Run setup menu
        def run_setup(self):

                # Fit background to screen
                pygame.transform.scale(self.bckgnd_img, (screenWidth, screenHeight))

                # Mode Screen Loop
                exit = False
                while not exit:

                        # Set tick count
                        self.clock.tick(60)

                        # Display all necessary images / text
                        screen.blit(self.bckgnd_img, (0,0))
                        screen.blit(self.Title, (350, 100))
                        screen.blit(self.option1, (200, 300))
                        screen.blit(self.option2, (200, 400))
                        screen.blit(self.quit, (400, 750))

                        # If quit event detected, leave
                        event = pygame.event.poll()
                        if event.type == pygame.QUIT:
                                sys.exit()

                        # Tick function detects key input
                        self.mode = self.tick()

                        # If mode is set properly, exit
                        if self.mode == 1 or self.mode == 2:
                                exit = True
                        elif self.mode == 4:
                                return 0, 0

                        # Display images
                        pygame.display.flip()

                # Difficulty Screen Loop
                exit = False
                while not exit:

                        # Display all necessary images / text
                        screen.blit(self.bckgnd_img, (0,0))
                        screen.blit(self.Title, (350, 100))
                        screen.blit(self.select_diff, (250, 250))
                        screen.blit(self.diff1, (250, 350))
                        screen.blit(self.diff2, (250, 425))
                        screen.blit(self.diff3, (250, 500))
                        screen.blit(self.quit, (400, 750))

                        # If quit detected, exit
                        event = pygame.event.poll()
                        if event.type == pygame.QUIT:
                                sys.exit()

                        # Tick function detects key input
                        self.diff = self.tick()

                        # If mode is set properly, exit
                        if self.diff == 1 or self.diff == 2 or self.diff == 3:
                                exit = True
                        elif self.diff == 4:
                                return 0, 0

                        # Display images
                        pygame.display.flip()

#########################################################
#							#
#	Chisom - here's where the menus for		#
#	player option and ball option will		#
#	go. My code above is pretty straight-		#
#	forward, you can copy the premise of it		#
#							#
#########################################################

                # Player Option Screen Loop
                exit = False
                while not exit:
			self.player_img = "images/players/default.png"
			break # Not really

                # Ball Option Screen Loop
                exit = False
                while not exit:
			self.ball_img = "images/balls/soccerBall.png"
			break # Not really

                # Return appropriate value
                return self.mode, self.diff, self.player_img, self.ball_img


        # Function checks for keystroke, returns it
        def tick(self):

                # If keystroke detected, react accordingly
                key = pygame.key.get_pressed()

                if key[pygame.K_1]:
                        return 1
                if key[pygame.K_2]:
                        return 2
                if key[pygame.K_3]:
                        return 3
                if key[pygame.K_q]:
                        return 4
                else:
                        return 0

