# FightingGame
A 2d Python based fighting game


 # How to run:
First open the code folder and run the Server.py file
This is the server which handles lobby creation

Open the code folder and run execute.py to start the game
Online only works on local host for now so you can test it by opening 2 instances of the game,
Host a game on one client and it should appear for the other client, which you can join on

# Improvements:
The current game only has the 2 players send their data to the game server, instead of the server receiving 
input requests and emitting game states. My implementation could result in diverging game states in some cases
So if the game was remade, I would make the server have authoritative game state, and the user sends input to the server

More characters and moves could be added, and my implementation with the assets was very slow to make. Instead of
using a sprite sheet and sliding a window across the sheet to retrieve the needed sprite, i cut out each sprite
and stored it in a folder, which took a long time.

Attempting to make the game run not only on local host would also be a big improvement to see it properly work.
