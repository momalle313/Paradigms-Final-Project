### Programming Paradigms Final Project ###

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor


# Global Variables
player_num = None	# Keeps track of number
PORT = 40087

# Data Connection
class DataConnection(Protocol):

	def connectionMade(self):

		print "Connected to Game Server"

	def dataReceived(self, data):

		global player_num
		player_num += 1
		print data
		#screen_update(data, player_num)

	def connectionLost(self, reason):
		print "Connection to game server was lost"


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

