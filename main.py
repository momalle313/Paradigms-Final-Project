### Programming Paradigms Final Project ###

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
#from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from GamePlay import gameSpace, Player, Computer, Ball, Setup
from PlayerConnect import DataFactory, DataConnection
import sys, pygame, math


# Global Variable
PORT = 40087		# Utilizes open port
HOST = "localhost"	# Can only play if on ash

### Main Execution ###


if __name__ == "__main__":

	gs = gameSpace()


	# Connect to server, run reactor if 2 player game initiated
	if gs.get_mode() == 2:
		reactor.connectTCP(HOST, PORT, DataFactory())
        	lc = LoopingCall(gs.play())
		lc.start(.01666)
		reactor.run()
	else:
		clock = pygame.time.Clock()
		while gs.game_over() == 0:
			clock.tick(60)
			gs.play()

