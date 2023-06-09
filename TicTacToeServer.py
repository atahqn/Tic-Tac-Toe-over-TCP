import socket
import threading
import sys


# Server side of TicTacToe
class TicTacToeServer:
    def __init__(self, port):
        # Initialize the game state
        self.board = [['_' for _ in range(3)] for _ in range(3)]
        self.turn = 0
        self.symbols = ['X', 'O']
        self.condition = threading.Condition()
        self.game_over = False
        self.clients = []

        # Creating and binding the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen(2)
        print("TicTacToe server is ready.")

    def check_legal_move(self, move, player):
        # Checking if the given move is legal
        x, y = move
        # If x and y is between 0 and 3 then it is legal
        # If desired place is occupied it is illegal
        # If trying to input while others turn it is illegal
        return 0 <= x < 3 and 0 <= y < 3 and self.board[x][y] == '_' and self.turn % 2 == player

    def check_winner(self, symbol):
        # This function checks if the player with the given symbol has won the game.
        # Check each row of the board to see if all cells in the row have the same symbol
        for row in self.board:
            if all(cell == symbol for cell in row):
                return True  # If a row is filled with the player's symbol, they have won the game
        # Check each column of the board to see if all cells in the column have the same symbol
        for col in range(3):
            if all(self.board[row][col] == symbol for row in range(3)):
                return True  # If a column is filled with the player's symbol, they have won the game
        # Check the two diagonals to see if all cells in the diagonals have the same symbol
        if all(self.board[i][i] == symbol for i in range(3)) or all(self.board[i][2 - i] == symbol for i in range(3)):
            return True  # If a diagonal is filled with the player's symbol, they have won the game
        # If none of the conditions above are met, the player has not yet won the game
        return False

    def main_server(self, conn, player):
        # Send initial connection message to client with player's symbol and ID
        conn.sendall(f"Retrieved symbol {self.symbols[player]} and ID={player}\n".encode())
        # Main game loop, continues while the game is not over
        while not self.game_over:
            with self.condition:
                # If it's not the current player's turn, wait until condition is notified
                while self.turn % 2 != player and not self.game_over:
                    self.condition.wait()
                # If the game has ended, break out of the game loop
                if self.game_over:
                    break
                # Send the current board state to the client
                conn.sendall("\nState of the board:\n".encode())  # Added a newline character before the first board
                for row in self.board:
                    conn.sendall(" ".join(row).encode() + b'\n')
                # Check if the game has reached a draw
                if self.turn >= 9:
                    self.game_over = True
                    self.condition.notify_all()
                    self.handle_game_result()  # Handle the result (in this case, a draw)
                    break
                # Notify the client it's their turn
                conn.sendall(f"Turn information: Your turn!\n".encode())
                # Receive the client's move
                move = conn.recv(1024).decode().strip()
                # If the client sends the 'status' command, send them the current game status
                if move.lower() == "status":
                    self.send_status(conn, player)
                    continue
                # Split the move into coordinates
                move = move.split(',')
                # Check if the client has sent a valid move
                if len(move) != 2:
                    print(f"Invalid input given by Player {player}")
                else:
                    x, y = int(move[0]), int(move[1])
                print(f"Waiting for Player {player}'s move")
                # If the move is legal, update the board and check for a winner
                if self.check_legal_move((x, y), player):
                    print(f"Received {self.symbols[player]} on ({x},{y}). It is a legal move.")
                    self.board[x][y] = self.symbols[player]
                    # If the move wins the game, update game status, notify all players, and handle the game result
                    if self.check_winner(self.symbols[player]):
                        self.game_over = True
                        self.condition.notify_all()
                        # Send the final board state to the client
                        conn.sendall("Final board state:\n".encode())
                        for row in self.board:
                            conn.sendall(" ".join(row).encode() + b'\n')
                        self.handle_game_result(winner=player)
                        break
                    # If the game hasn't been won, increment the turn counter and notify all players
                    self.turn += 1
                    self.condition.notify_all()
                    # Send the updated board state to the client after their successful move
                    conn.sendall("State of the board after your move:\n".encode())
                    for row in self.board:
                        conn.sendall(" ".join(row).encode() + b'\n')

                else:  # If the move is illegal
                    # Provide an appropriate error message
                    if 0 <= x < 3 and 0 <= y < 3 and self.board[x][y] != '_':
                        print(
                            f"Received {self.symbols[player]} on ({x},{y}). It is an illegal move. (The cell is "
                            f"already occupied.)")
                    else:
                        print(
                            f"Received {self.symbols[player]} on ({x},{y}). It is an illegal move. (The move is out of "
                            f"the board.)")
                    conn.sendall("This is an illegal move. Please change your move!\n".encode())
        # Close the connection to the client after the game ends
        conn.close()

    def handle_game_result(self, winner=None):
        # Sending the final board state to all clients
        for c, _ in self.clients:
            c.sendall("Final board state:\n".encode())
            for row in self.board:
                c.sendall(" ".join(row).encode() + b'\n')

        # Displaying the final board state before showing the game result
        print("Final board state:")
        for row in self.board:
            print(" ".join(row))

        # Sending the game result to all clients
        if winner is not None:
            print(f"\nPlayer {winner} wins!")
            for c, _ in self.clients:
                c.sendall(f"Player {winner} wins!\n".encode())
        else:
            print("\nThe game is tied.")
            for c, _ in self.clients:
                c.sendall("The game is tied.\n".encode())

    def send_status(self, conn, player):
        # Client can request the board state and turn information at any moment throughout the game.
        # Sending the current game status to the client
        status = f"Player {player} requested game status.\n"
        status += "Current board state:\n"
        for row in self.board:
            status += " ".join(row) + "\n"
        status += f"Turn: {self.turn}\n"
        status += f"Next player: {self.symbols[self.turn % 2]}\n"
        status += "-----------------------------------------\n"
        conn.sendall(status.encode())

    def start(self):
        # Accept connections and start client handler threads
        for i in range(2):
            conn, addr = self.server_socket.accept()
            print(f"A client is connected, and it is assigned with the symbol {self.symbols[i]} and ID={i}")
            self.clients.append((conn, i))
        print("The game is started.")
        # Making system multithreading as desired in the assignment
        for conn, i in self.clients:
            threading.Thread(target=self.main_server, args=(conn, i)).start()


if __name__ == "__main__":
    port_ = int(sys.argv[1])
    server = TicTacToeServer(port_)
    server.start()
