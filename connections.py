import abc #builtin library allowing for interface creation

import socket
from threading import Thread

## interface class to try and standardize the method calls to both Client and Server objects

class formalConnectionInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'sendNewState') and
                callable(subclass.sendNewState))
    
    @abc.abstractmethod
    def sendNewState(self, newBoardState:list[list]):
        """method to send the new state of a board to other players

        Args:
            newBoardState (list[list]): 2d array indicitating new board state
        """
        raise NotImplementedError #if this function is overwritten, the exception will not occur

class TicTacToeServer(formalConnectionInterface):
    def __init__(self, game):
        # Create a TCP socket for the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to localhost and port 9999
        self.server_socket.bind(('localhost', 9999))
        # Listen for incoming connections, allow only one
        self.server_socket.listen(1)
        # Dictionary to store player sockets
        # server should be passed an instance of the game to have access, AND the game must be passed a reference to the server
        self.game = game
        self.players = []
        game.setConnection(self) #boy i hope this works

    def handle_client(self, clientConnection):
        # Handle messages from a single client
        while True:
            try:
                # Receive data from the client
                data = clientConnection.recv(1024)
                if not data:
                    break
                # Decode the message
                newBoardState = self.__bytesToBoardState(data)
                self.game.updateBoardState(newBoardState) #new board state gets updated, also changes the turn
            except Exception as e:
                print(f"Error: {e}")
                break

        # Handle client disconnection
        print(f"remote player! disconnected")
        clientConnection.close()

    def sendNewState(self, boardState:list[list[int]]):
        """sends updated board state to players
        
        Overwrites formalConnectionInterface.sendNewState()

        Args:
            boardState (list[list]): 2d array indicating board state
        """
        # sends out the new board state and current turn value to all players
        # Send a message to all connected players
        bytestate = self.__boardStateToBytes(boardState)
        for player_socket in self.players:
            player_socket.sendall(bytestate)
            
    def __boardStateToBytes(self, newBoardState:list[list[int]]) -> bytearray:
        """converts the 2d int list of BoardState to a single Bytes object

        Args:
            boardState (list[list]): 2d list of ints to be converted

        Returns:
            bytearray: representation of board object as Bytes object
        """
        byte = bytearray()
        for listY in newBoardState:
            for intX in listY:
                byte.append(intX)
            byte.append(3) # value of 3 used to indicate line break
        return byte
    
    def __bytesToBoardState(self, byte:bytearray) -> list[list[int]]:
        """converts from recieved bytes to 2d intarray

        Args:
            byte (bytearray): recieved bytes

        Returns:
            list[list]: 2d list reconstructed board state
        """
        #god i hope this works the way i want it to
        newBoardState = []
        y = 0 
        x = 0
        for bit in byte:
            if (bit == 3):
                y += 1
            else:
                newBoardState[y][x] = bit 
                x += 1
        return newBoardState

    def start(self):
        # Accept incoming client connections
        while True:
            clientConnection, _ = self.server_socket.accept()
            # Assign a unique player ID to each client
            player_id = len(self.players) + 1
            self.players[player_id] = clientConnection
            # Create a new thread to handle the client
            Thread(target=self.handle_client, args=(clientConnection)).start()

class TicTacToeClient(formalConnectionInterface):
    def __init__(self, hostIP, portNum, game):
        self.receiveData = None  # I made this because it wasn't there but referenced in self.create_thread below
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostIP, portNum))
        self.game = game
        self.game.setConnection(self)
        self.create_thread(self.receiveData) 
        
    def create_thread(self, target):
        thread = Thread(target=target)
        thread.daemon = True
        thread.start()
        
    def __bytesToBoardState(self, byte:bytearray) -> list[list[int]]:
        """converts from recieved bytes to 2d intarray

        Args:
            byte (bytearray): recieved bytes

        Returns:
            list[list]: 2d list reconstructed board state
        """
        #god i hope this works the way i want it to
        newBoardState = []
        y = 0 
        x = 0
        for bit in byte:
            if (bit == 3):
                y += 1
            else:
                newBoardState[y][x] = bit 
                x += 1
        return newBoardState
    
    def __boardStateToBytes(self, newBoardState:list[list[int]]) -> bytearray:
        """converts the 2d int list of BoardState to a single Bytes object

        Args:
            boardState (list[list]): 2d list of ints to be converted

        Returns:
            bytearray: representation of board object as Bytes object
        """
        byte = bytearray()
        for listY in newBoardState:
            for intX in listY:
                byte.append(intX)
            byte.append(3) # value of 3 used to indicate line break
        return byte
    
    def recieveData(self):
        while True:
            try:
                # Receive data from the client
                data = self.sock.recv(1024)
                if not data:
                    break
                # Decode the message
                newBoardState = self.__bytesToBoardState(data)
                self.game.updateBoardState(newBoardState) #new board state gets updated
            except Exception as e:
                print(f"Error: {e}")
                break
            
    def sendNewState(self, boardState:list[list[int]]):
        """sends updated board state to players
            
        Overwrites formalConnectionInterface.sendNewState()

        Args:
            boardState (list[list]): 2d array indicating board state
        """
        # sends out the new board state and current turn value to all players
        # Send a message to all connected players
        bytestate = self.__boardStateToBytes(boardState)
        self.sock.sendall(bytestate)
        
if __name__ == "__main__":
    pass #idk how to make a self-standing unit test for this guy
