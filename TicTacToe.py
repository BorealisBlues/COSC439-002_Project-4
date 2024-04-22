#Class definition for internal game logic

class TicTacToe:
    """class representing the actual game
    """
    
    
    def __init__(self, length:int=3, width:int=3):
        """Constructor function

        Args:
            length (int): the length of the board, default 3
            width (int): the width of the board, default 3
        """
        self.__board=[]
        self.turn = 1 # tracks which player's turn it is, starting with player 1
        self.__initializeBoard(length, width)
    

    def getBoardState(self) -> list:
        """function to get the state of the board for display or transmission

        Returns:
            list: 2 dimensional array representing board state, 0's indicate empty, 
                                                                1's for player 1 has played here,
                                                                2's for player 2 has played here
        """
        return self.__board
    
    
    def __initializeBoard(self, length:int, width:int):
        '''Initializes a multidimensional array for tracking moves by each player, allows for variable board size'''
        self.__board = [[0 for j in range(width)] for i in range(length)]
    
    def takeTurn(self, player:int, posX:int, posY:int):
        
        """function for a player to take thier turn and make their mark
        Throws ValueError on wrong turn

        Args:
            player (int): the player (1 or 2) who is taking their turn
            posX (int): horizontal position in the board where the player is playing
            posY (int): vertical position in the board where the player is playing
        """
        if(self.turn == player): # check if it is the players turn
            self.__board[posX][posY] = player
        else:
            raise ValueError(f"It is player {self.turn}'s turn! not player {player}'s!")
        
        self.checkWin(posX, posY)
        self.changeTurn()
        
    def changeTurn(self):
        """changes which player's turn it is
        """
        if(self.turn == 1):
            self.turn = 2
        else: self._turn = 1
        
    def checkWin(self, posX:int, posY:int) -> bool:
        """Checks if the board is in a winning state, raises ??? something, not sure what yet
        
        Args:
            posX (int): horizontal position just played at
            posY (int): vertical position just played at
        Returns:
            bool: whether or not there is a victory for the player whose turn it is
        """
        if(self.__checkWinRow(posY) or self.__checkWinColumn(posX) or self.__checkWinDiagonal()):
            #if any of the 3 possible win conditions are true then return True
            return True
        else: return False
    
    def __checkWinRow(self, posY:int) -> bool:
        """checks if there is a row-based victory for the player whose turn it is

        Args:
            posY (int): current vertical position

        Returns:
            bool: whether or not there is a victory for the player whose turn it is
        """
        victory = True
        
        for spot in self.__board:
            if not (spot[posY] == self.turn):
                victory = False
            
        return victory
    
    def __checkWinColumn(self, posX:int) -> bool:
        """checks for a Column win at current horizontal position

        Args:
            posX (int): current horizontal position

        Returns:
            bool:  whether or not there is a victory for the player whose turn it is
        """
        victory = True
        
        for spot in self.__board[posX]:
            if not (spot == self.turn):
                victory = False
        return victory
    
    def __checkWinDiagonal(self) -> bool:
        """this thing is the most convoluted thing in the damn world, theres gotta be a better way

        Returns:
            bool: whether or not there is a victory for the player whose turn it is
        """
        
        if(len(self.__board) == len(self.__board[0])): #returns false always if game is not square
            vicTLeftToBRight = True
            vicTRightToBLeft = True
            
            #first we check from top left to bottom right
            for i in range(len(self.__board)):
                if not (self.__board[i][i] == self.turn): # if the spot does not belong to the player
                    vicTLeftToBRight = False # the player does not have this victory
            
            #then we check if from top right to bottom left
            for x in reversed(range((len(self.__board)))): #iterating backwards (from right to left)
                for y in range(len(self.__board)): #iterating normal style, top to bottom
                    if (x == y): #if we are along a diagonal
                        if not (self.__board[x][y] == self.turn): #if the spot does not belong to the player
                            vicTRightToBLeft = False #player does not have this victory
            
            if(vicTRightToBLeft or vicTLeftToBRight): #if player has either subtype of victory
                return True 
            else: return False

        else: return False
        
    def __str__(self) -> str:
        """Returns a string representation of the current board state

        Returns:
            str: the board state as a string, i hope
        """
        boardasString = ""
        for x in self.__board:
            boardasString += "|"
            for y in x:
                boardasString += f" {y} |"
            boardasString += "\n"
        return boardasString
            
            
        
def testGame():
    game = TicTacToe()
    
    while(True):
        print(f"welcome to ticTacToe! Current turn is player {game.turn}'s")
        print(game)
        player = int(input("Please enter which player you are, 1 or 2!"))
        posX = int(input(f"Please enter the X Position that player {player} wishes to play at :"))
        posY = int(input("Thank you! now please enter the Y Position! :"))
        game.takeTurn(player, posX, posY)
    
    
    
    
        
if __name__ == "__main__":
    testGame()