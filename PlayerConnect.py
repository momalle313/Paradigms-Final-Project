### Programming Paradigms Final Project ###

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor
from GamePlay import gameSpace


# Global Variables
player_num = 0		# Keeps track of number
PORT = 40087

# Data Connection
class DataConnection(Protocol):

	def __init__(self):
		gs = gameSpace()
		gs.main()

	def connectionMade(self):

		print "Connected to Game Server"

	def dataReceived(self, data):

		global player_num
		print data
		if data == "You are Player 1":
			self.player = 1
		elif data == "You are Player 2":
			self.player = 2
		else:
			gs.screen_update(data, self.player)
			data = gs.get_data()
			self.transport.write(data)

	def connectionLost(self, reason):

		print "Connection to game server was lost:"
		print str(reason)

class DataFactory(ClientFactory):

	def __init__(self):

		self.myconn = DataConnection()

	def buildProtocol(self, addr):

		return self.myconn


### Main Execution ###


if __name__ == "__main__":

        Data = DataFactory()

        reactor.connectTCP("localhost", PORT, Data)
        reactor.run()

