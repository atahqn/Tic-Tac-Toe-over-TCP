import socket
import sys


# Client side of TicTacToe
class TicTacToeClient:
    def __init__(self, port):
        # Initializing the client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', port))
        print("Connected to the server.")

    # Main function
    def main_client(self):
        while True:
            data = self.client_socket.recv(1024).decode()
            if not data:
                break

            print(data)
            if "Your turn!" in data:
                move = input("Enter your move (row,column) or type 'status' to check the board state: ")
                self.client_socket.sendall(move.encode())

        self.client_socket.close()


if __name__ == "__main__":
    port_ = int(sys.argv[1])
    client = TicTacToeClient(port_)
    client.main_client()
