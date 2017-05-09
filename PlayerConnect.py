### Programming Paradigms Final Project ###

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor
from GamePlay import gameSpace


# Global Variables
player_num = 0		# Keeps track of number
PORT = 40087		# Available port to connect to on localhost

# Data Connection
class DataConnection(Protocol):

	# Initialize gamespace and start main loop
	def __init__(self):
		self.gs = gameSpace()
		self.gs.main()

		# Variables to pass to game space
		self.connected = 0
		self.player = 0

	# Set connection variable to true, print to terminal
	def connectionMade(self):

		self.connected = 1
		print "Connected to Game Server"

	# Determine what to do with received data
	def dataReceived(self, data):

		global player_num

		# If data is P1 message, set to P1
		if data == "You are Player 1":
			self.player = 1
			self.gs.set_player(self.player)

		# If data is P2 message, set to P2
		elif data == "You are Player 2":
			self.player = 2
			self.gs.set_player(self.player)

		# If data is position update, send to gs, update other player
		else:
			self.gs.other_player_pos(data)
			data = self.gs.player_pos()
			self.transport.write(data)

	# If connection is lost, display connection lost screen
	def connectionLost(self, reason):

		self.gs.connection_lost()
		print "Connection to game server was lost:"
		print str(reason)

# Factory for DataConnection
class DataFactory(ClientFactory):

	# Establish Connection
	def __init__(self):

		self.myconn = DataConnection()

	# Build protocol returns own connection
	def buildProtocol(self, addr):

		return self.myconn
