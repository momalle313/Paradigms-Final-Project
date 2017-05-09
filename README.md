# Paradigms-Final-Project

# Michael O'Malley
# Chisom Igwe
# 5/10/17

Tutorial
========

1 player: run the command:
	python main.py
The title screen will pop up. Select 1 for 1 player. Then choose a difficulty,
1 to 3. Once this is chosen, the game starts. Deflect oncoming balls back at
your opponent with your sprite. If the ball gets past you, the other player
scores, and vice versa. First player to 10 wins!

2 player: run this command to begin the game server
	python Server.py
Now any two ash users can connect to the server on Michael's open port,
40087. To start, run the command:
	python main.py
The title screen will pop up. Select 2 for 2 player. Then choose a difficulty,
1 to 3. If you are the second player to join, this is chosen for you.
Once this is chosen, the game starts. Deflect oncoming balls back at
your opponent with your sprite. If the ball gets past you, the other player
scores, and vice versa. First player to 10 wins!


Overview
========

We decided to recreate pong for our project. We would allow the user to play
with a computer or a human over a network connection. However, we were too
ambitious, and not all of it is operational.


What Works
==========

- Setup Menus
- Win Screen
- Good bye screen
- Lost connection screen
- 1 player with computer
- Client / Server Connection (Players can connect and it knows the difference
				between them) 
- data transfer
	(We know it transfers data to the correct client because of a
	debugging program that tested if data was being sent correctly,
	however we never got a chance to attempt data transfer during a game)


What doesn't work
=================

- 2 player is not functional. LoopingCall was never fully debugged, so while
there was a connection, the game data was not transferred back and forth
- In general, the game lags badly. Likely a bad connection to ash


What we didn't have time to add
===============================

- Variability of player sprites (had pictures, no time to set up screens)
- same with ball sprites
- same with background images
- Random obstacle mode
