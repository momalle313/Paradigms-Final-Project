### Programming Paradigms Final Project ###

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from GamePlay import gameSpace


# Global Variables
player_num = 0		# Keeps track of number
PORT = 40087		# Available port to connect to on localhost

# Data Connection
class DataConnection(Protocol):

	# Initialize gamespace and start main loop
	def __init__(self, gs):

		# GameSpace Variables
		self.gs = gs
		self.connected = 0

	# Set connection variable to true, print to terminal
	def connectionMade(self):

		self.connected = 1
		print "Connected to Game Server"
		data = self.gs.player_pos()
		self.transport.write(data)

	# Determine what to do with received data
	def dataReceived(self, data):

		# Update data
		data = data.strip()
		self.gs.update(data)

	# If connection is lost, display connection lost screen
	def connectionLost(self, reason):

		print "Connection to game server was lost:"
		print str(reason)
		self.gs.connection_lost()

# Factory for DataConnection
class DataFactory(ClientFactory):

	# Establish Connection
	def __init__(self, gs):

		self.myconn = DataConnection(gs)

	# Build protocol returns own connection
	def buildProtocol(self, addr):

		return self.myconn
