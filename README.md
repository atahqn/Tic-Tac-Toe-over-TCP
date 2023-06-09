# Tic Tac Toe Game: Server-Client Model

This project is a simple implementation of the classic Tic Tac Toe game using a client-server architecture. The game is played between two clients (players) that are connected to a server. The players take turns to make a move, the status of which is communicated through the server. The server also keeps track of the game's state and determines the winner.

## Prerequisites

- Python 3.x

## Server Side Code

The server-side of the game is handled by the `TicTacToeServer` class. Here's a breakdown of its methods:

- `__init__(self, port)`: Initializes the server on a specific port, sets up the game state, and starts listening for incoming connections.

- `check_legal_move(self, move, player)`: Checks if a move made by a player is legal (i.e., within the game's boundaries and not on an already occupied cell).

- `check_winner(self, symbol)`: Checks if there's a winner, given a specific player's symbol.

- `main_server(self, conn, player)`: The main loop that handles game logic and communicates with the clients.

- `handle_game_result(self, winner=None)`: Handles the result of the game, notifying all clients about the game's result.

- `send_status(self, conn, player)`: Sends the current game state to a client upon request.

- `start(self)`: Starts the server and waits for two clients to connect. Once two clients have connected, it starts a new thread for each client, allowing them to play the game simultaneously.

## Client Side Code

The client-side of the game is handled by the `TicTacToeClient` class. Here's what its methods do:

- `__init__(self, port)`: Initializes the client and connects it to the server.

- `main_client(self)`: The main loop that receives data from the server and sends user input to the server.

## How to Run

1. First, start the server by running the server script. Replace `<port>` with the desired port number.

    ```sh
    python server.py <port>
    ```

2. On two different terminals, start each client by running the client script. Replace `<port>` with the same port number you used for the server.

    ```sh
    python client.py <port>
    ```

3. The game will then start, and each client will be prompted to input their moves, in turns.
