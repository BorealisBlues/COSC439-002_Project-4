import socket
from threading import Thread
from TicTacToe import TicTacToe

class TicTacToeServer:
    def __init__(self):
        # Create a TCP socket for the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to localhost and port 9999
        self.server_socket.bind(('localhost', 9999))
        # Listen for incoming connections, allow up to 2 clients to connect
        self.server_socket.listen(2)
        # Dictionary to store player sockets
        self.players = {}
        # Initialize a TicTacToe game instance
        self.game = TicTacToe()

    def handle_client(self, client_socket, player_id):
        # Handle messages from a single client
        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024)
                if not data:
                    break
                # Decode the message
                message = data.decode()
                # Process player move message
                if message.startswith('move'):
                    _, player, posX, posY = message.split(',')
                    player, posX, posY = int(player), int(posX), int(posY)
                    # Update the game state with the player's move
                    self.game.takeTurn(player, posX, posY)
                    # Get the updated board state
                    board_state = self.game.getBoardState()
                    # Send the updated board state to all players
                    self.send_to_players(board_state)
            except Exception as e:
                print(f"Error: {e}")
                break

        # Handle client disconnection
        print(f"Player {player_id} disconnected")
        del self.players[player_id]
        client_socket.close()

    def send_to_players(self, message):
        # Send a message to all connected players
        for player_socket in self.players.values():
            player_socket.sendall(message.encode())

    def start(self):
        # Accept incoming client connections
        while True:
            client_socket, _ = self.server_socket.accept()
            # Assign a unique player ID to each client
            player_id = len(self.players) + 1
            self.players[player_id] = client_socket
            # Create a new thread to handle the client
            Thread(target=self.handle_client, args=(client_socket, player_id)).start()


if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()
