#Class definition for internal game logic

#TODO:
# -A    Please add requests for specific functions or clarification of functions here while we are in development
# -A    Need to add some sort of reset_board function to be called by ther GUI i think
class GameEndException(Exception):
    """To be raised upon game win with int value 0 for Tie, 1 for player 1 victory, 2 for player 2 victory """ 

class TicTacToe:
    """class representing the actual game"""   
     
    def __init__(self, length:int=3, width:int=3):
        """Constructor function

        Args:
            length (int): the length of the board, default 3
            width (int): the width of the board, default 3
        """
        self.__board=[]
        self.turn = 1 # tracks which player's turn it is, starting with player 1
        self.__initializeBoard(length, width)
    
    def getBoardState(self) -> list[list]:
        """function to get the state of the board for display or transmission

        Returns:
            list: 2 dimensional array representing board state, 0's indicate empty, 
                                                                1's for player 1 has played here,
                                                                2's for player 2 has played here
        """
        return self.__board

    def updateBoardState(self, newboardState:list[list]):
        """function to be called upon reception of new board state to synchronize between players

        Args:
            NewboardState (list[list]): 2 dimensional list representing new board state
        """
        #first check to make sure that the arrays are of equal size, which, shouldn't be an issue, but yk
        #input validation and all
        if (len(newboardState) == len(self.__board) and len(newboardState[0]) == len(self.__board[0])):
            print("Current Board State: " + str(self))
            for y in range(self.getBoardSize):
                for x in range(self.getBoardSize):
                    self.__board[y][x] = newboardState[y][x]
            print("New Board State: " + str(self))
        else:
            raise ValueError("new array does not match dimension of existing board!")

    def getBoardSize(self) -> int:
        """returns the size of the board - Ben"""
        return len(self.__board)

    def __initializeBoard(self, length:int, width:int):
        '''Initializes a multidimensional array for tracking moves by each player, allows for variable board size'''
        self.__board = [[0 for j in range(width)] for i in range(length)]
    
    def __checkValidMove(self, posX:int, posY:int) -> bool: #mangling this name too
        """check if the space is taken for attempted move -Ben"""
        if self.__board[posY][posX] != 0: #Swapped for intuitive display and storage, even if it leads to unintuitive access
            return False
        else:
            return True

    def takeTurn(self, player:int, posX:int, posY:int):
        
        """function for a player to take thier turn and make their mark
        Throws ValueError on wrong turn
        
        Raises:
            ValueError: for invalid move (wrong player or occupied space)
            GameEndException: game is now over, either victory for player 1/2, or tie (0)

        Args:
            player (int): the player (1 or 2) who is taking their turn
            posX (int): horizontal position in the board where the player is playing
            posY (int): vertical position in the board where the player is playing
        """
        if(self.turn == player): # check if it is the players turn
            if self.__checkValidMove(posX, posY):
                self.__board[posY][posX] = player #Y and X are swapped for consistent and intuitive display,
                                                  #even if it reads a little unintuitively
            else:
                raise ValueError(f"Position at X: {posX} Y: {posY} is alredy taken!")
        else:
            raise ValueError(f"It is player {self.turn}'s turn! not player {player}'s!")
        
        if self.checkWin(posX, posY):
            raise GameEndException(self.turn)
        elif self.__checkTie(posX, posY):
            raise GameEndException(0)
        else:   
            self.__changeTurn()
        
    def __changeTurn(self): #changed to a mangled name to indicate use only internally
        """changes which player's turn it is
        """
        if(self.turn == 1):
            self.turn = 2
        else: self.turn = 1
        
    def checkWin(self, posX:int, posY:int) -> bool:
        """Checks if the board is in a winning state,
           intended for internal use only but left unmangled for edge cases
        
        Args:
            posX (int): horizontal position just played at
            posY (int): vertical position just played at
        Returns:
            bool: whether or not there is a victory for the player whose turn it is
        """
        if(self.__checkWinRow(posX) or self.__checkWinColumn(posY) or self.__checkWinDiagonal()):
            #if any of the 3 possible win conditions are true then return True
            return True
        else: return False

    def __checkTie(self, posX:int, posY:int) -> bool: #changed to a mangled name to indicate use only internally
        """checks for a tie condition - Ben
        Args:
            PosX:int : X position of current move
            posY:int : Y position of current move
        """
        if 0 not in (item for sublist in self.__board for item in sublist) and not self.checkWin(posX, posY):
            return True
        else:
            return False

    def __checkWinRow(self, posX:int) -> bool:
        """checks if there is a row-based victory for the player whose turn it is

        Args:
            posY (int): current vertical position

        Returns:
            bool: whether or not there is a victory for the player whose turn it is
        """
        victory = True
        
        for spot in self.__board:
            if not (spot[posX] == self.turn):
                victory = False
            
        return victory
    
    def __checkWinColumn(self, posY:int) -> bool:
        """checks for a Column win at current horizontal position

        Args:
            posX (int): current horizontal position

        Returns:
            bool:  whether or not there is a victory for the player whose turn it is
        """
        victory = True
        
        for spot in self.__board[posY]:
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
            
    def resetGame(self): #renamed function for internal consistency
        """Resets all entries in the board to 0 (representing empty) values
        
        Calls internal function __initializeBoard to do so
        """
        self.__initializeBoard(len(self.__board), len(self.__board[0])) #makes a call to the board initialization
        # this should result in a reset of the board state
        
def testGame() -> int:
    """Pure CLI testing for internal game logic

    Returns:
        _type_: 1, 2, or 0 depending on player 1 victory, player 2 victory, or tie respectively
    """
    game = TicTacToe()
    while(True):
        try:
            print(f"welcome to ticTacToe! Current turn is player {game.turn}'s")
            print(game)
            player = int(input("Please enter which player you are, 1 or 2!"))
            posX = int(input(f"Please enter the X Position that player {player} wishes to play at :"))
            posY = int(input("Thank you! now please enter the Y Position! :"))
            game.takeTurn(player, posX, posY)
        except ValueError as e:
            print("invalid move! Please try again.")
        except GameEndException as e:
            print("Game over!")
            if str(e) == "0":
                print("Game ended in a tie!")
                return 0
            else:
                print(f"Player {e} wins!")
                return e
    
if __name__ == "__main__":
    testGame()