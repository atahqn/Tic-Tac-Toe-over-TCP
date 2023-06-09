# README.md

## Tic Tac Toe Game: Server-Client Model

This project is a simple implementation of the classic Tic Tac Toe game using a client-server architecture. The game is played between two clients (players) that are connected to a server. The players take turns to make a move, the status of which is communicated through the server. The server also keeps track of the game's state and determines the winner.

## Prerequisites

You need to have Python 3.x installed to run this program.

## Server Side Code

The server-side of the game is handled by the `TicTacToeServer` class, which takes care of the game logic and handles client connections. Here's a breakdown of its methods:

- `__init__(self, port)`: Initializes the server on a specific port, sets up the game state and starts listening for incoming connections.

- `check_legal_move(self, move, player)`: Checks if a move made by a player is legal (i.e., within the game's boundaries and not on an already occupied cell).

- `check_winner(self, symbol)`: Checks if there's a winner, given a specific player's symbol.

- `main_server(self, conn, player)`: The main loop that handles game logic and communicates with the clients. It sends and receives messages to/from the clients, updates the game's state, and checks for the end of the game.

- `handle_game_result(self, winner=None)`: Handles the result of the game, notifies all clients about the game's result.

- `send_status(self, conn, player)`: Sends the current game state to a client upon request.

- `start(self)`: Starts the server and waits for two clients to connect. Once two clients have connected, it starts a new thread for each client, allowing them to play the game simultaneously.

## Client Side Code

The `TicTacToeClient` class handles the client-side logic of the game. Here's what its methods do:

- `__init__(self, port)`: Initializes the client and connects it to the server.

- `main_client(self)`: The main loop that receives data from the server and sends user input to the server. It continues to prompt the user for input whenever it's their turn, until the game ends.

## How to run

First, start the server:

```bash
python server.py <port>
```

Then, on two different terminals, start each client:

```bash
python client.py <port>
```

The game will then start, and each client will be prompted to input their moves, in turns.
