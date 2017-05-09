### Programming Paradigms Final Project ###

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor
import sys, pygame, math
import PlayerConnect
import GamePlay


# Global Variable
PORT = 40087		# Utilizes open port
HOST = "localhost"	# Can only play if on ash

### Main Execution ###


if __name__ == "__main__":

	# Connect to server, run reactor
	reactor.connectTCP(HOST, PORT, DataFactory())
        reactor.run()

