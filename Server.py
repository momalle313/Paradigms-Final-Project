### Programming Paradigms Final Project ###

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor


# Global Variables
player_num = 0
PORT = 40087
factory = Factory()
factory.clients = []

# Data Connection handlers
class DataConnection(Protocol):

	def connectionMade(self):

		global player_num
		global factory

		player_num += 1
		factory.clients.append(self)
		print
		print factory.clients
		print
		print "Player " + str(player_num) + " Connected"
		if player_num == 1:
			self.transport.write("You are Player 1")
			self.transport.write("Waiting for Player 2 to join...")
		elif player_num == 2:
			self.transport.write("You are Player 2")

	def dataReceived(self, data):

		print data

	def connectionLost(self, reason):

		print "Connection to " + str(self) + " lost"
		print reason

class DataFactory(Factory):

	def __init__(self):

		self.myconn = DataConnection()

	def buildProtocol(self, addr):

		return self.myconn


### Main Execution ###


if __name__ == "__main__":

	Data = DataFactory()

	reactor.listenTCP(PORT, Data)
	reactor.run()
