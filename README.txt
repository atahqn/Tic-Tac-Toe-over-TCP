Multithreaded Tic-Tac-Toe Game Server

Description:

This is a simple network-based, two-player Tic-Tac-Toe game implemented in Python. The project consists of two main components - a multithreaded server and a client.

Server:

The server is multithreaded, handling each client in a separate thread, allowing for turn-based play between two players. It manages the game state, validates moves, checks for the game-ending condition, and communicates with clients.

Client:

The client connects to the server, receives updates about the game state, sends moves to the server, and displays game information to the user. The client can also send a 'status' command to request the current game status from the server.

Requirements:

Python 3.x

Server:

Run the server with a port number as a command-line argument:

python3 TicTacToeServer.py [port]

Replace [port] with the desired port number.

Client:

Run the client with the same port number as a command-line argument:

python3 TicTacToeClient.py [port]

Replace [port] with the same port number you used for the server. Run this command twice for two clients/players.

During the game, when it's a client's turn, the client should input a move in the format 'row,column' (0-indexed), or type 'status' to check the current game state.

Note:

Please ensure that the server is running before starting the clients. Both clients should be running for the game to begin.
