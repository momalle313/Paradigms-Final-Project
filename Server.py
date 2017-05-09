### Programming Paradigms Final Project ###

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor


# Global Variables
player_num = 0		# Keeps track of connections, only allows 2
PORT = 40087		# Open port to run server on

connection_list = []	# Keeps both connections distinct in list
			# This way, the server can wait for two connections
			# from anybody, place them in this list, and be able
			# to have them communicate rather than only allowing
			# specific clients to communicate. Anyone can connect

# Data Connection handlers
class DataConnection(Protocol):

	# Init makes queue
	def __init__(self):
		self.queue = DeferredQueue()

	# Responses for each player when connection is made
	def connectionMade(self):

		# Declare globals
		global connection_list
		global player_num

		# Increment player number
		player_num += 1

		# Check if too many players
		if player_num > 2:
			self.transport.write("Already two players: Disconnecting")
			player_num -= 1
			self.transport.loseConnection()
			return

		# Add self to connection list
		connection_list.append(self)
		print "Player " + str(player_num) + " Connected"
		self.player = player_num
		self.transport.write(str(player_num))

		# If player 2, tell player 1 you're connected
		if player_num == 2:
			connection_list[0].transport.write("3")

	# Handle data received, send to opposite player
	def dataReceived(self, data):

		# Put data in queue
		self.queue.put(data)
		self.queue.get().addCallback(self.forwardData)

	# Begin forwarding process
	def forwardData(self, data):

		# If data is received from player 1, send to player 2
		if self.player == 1:
			connection_list[1].transport.write(data)
			self.queue.get().addCallback(self.forwardData)

		# If data is received from player 2, send to player 1
		elif self.player == 2:
			connection_list[0].transport.write(data)
			self.queue.get().addCallback(self.forwardData)

	# On loss of connection, name player and explain reason
	def connectionLost(self, reason):

		# Decrease player number
		global player_num
		player_num -= 1

		# State loss and reason
		print "Connection to Player " + str(self.player) + " was lost:"
		print str(reason)

		# Check who left, send appropriate messages
		if self.player == 1:
			connection_list.pop(0)
		elif self.player == 2:
			self.player = 1
			connection_list.pop(1)

# Factory for connection
class DataFactory(Factory):

	# Build Connect class
	def __init__(self):

		self.myconn = DataConnection()

	# Returns own connection
	def buildProtocol(self, addr):

		return self.myconn


### Main Execution ###


if __name__ == "__main__":

	# Init facrory and listen for Players to connect
	reactor.listenTCP(PORT, DataFactory())
	reactor.run()
