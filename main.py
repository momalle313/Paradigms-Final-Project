### Programming Paradigms Final Project ###

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from GamePlay import gameSpace, Player, Computer, Ball, Setup
from PlayerConnect import DataFactory, DataConnection
import sys, pygame, math, time


# Global Variable
PORT = 40087		# Utilizes open port
HOST = "localhost"	# Can only play if on ash


### Main Execution ###


if __name__ == "__main__":

	# Create gamespace
	gs = gameSpace()

	# Connect to server, run reactor if 2 player game initiated
	if gs.get_mode() == 2:

		# Connect to server
		reactor.connectTCP(HOST, PORT, DataFactory(gs))
		reactor.run()

		# Wait for player_num to be set
		time.sleep(1)

		# Begin looping gameloop
        	lc = LoopingCall(gs.play())
		lc.start(.01666)

	# If not, run normal gameloop with computer
	else:
		# Build clock, set to tick 60 times a second
		clock = pygame.time.Clock()

		# While game is not over, continue
		while gs.game_over() == 0:
			clock.tick(60)
			gs.play()

		# Once game is over, check winner, display screen, and exit
		gs.winner()
