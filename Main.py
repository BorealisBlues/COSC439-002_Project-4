# Main Driver File - Initial Commit - Andromeda
from TicTacToe import TicTacToe
from TicTacToeGUI import TicTacToeBoard
from connections import TicTacToeServer
from connections import TicTacToeClient


def main():
    ##  TODO:
    ##      - Add a screen for Create Game (host server) / Join Game (run client)
    ##      - impliment netcode into GUI
    ##      - TEST the netcode and make sure we dont have weird bugs in it
    ##      - Fix Bug in TicTacToe.py : Diagonal win checking only procs on \ direction not / direction
    
    ## PROMPT USER FOR IF HOST OR CLIENT

    game1 = TicTacToe()
    board1 = TicTacToeBoard(game1)
    game2 = TicTacToe()
    board2 = TicTacToeBoard(game2)
    board1.mainloop()
    board2.mainloop()

def testNet():
    game = TicTacToe()
    playerchoice = int(input("Welcome to our tictactoe project! Please enter 1 to host a game, and 2 to join one! : "))
    match playerchoice:
        case 1:
            connection = TicTacToeServer(game)
        case 2:
            serverAddress = input("Please enter the ip address of the server! : ")
            portNum = int(input("Please enter the port to connect to! : "))
            connection = TicTacToeClient(serverAddress, portNum, game)
        case _:
            print ("please enter a valid number! goodbye")
            return
    game.setConnection(connection)
    board = TicTacToeBoard(game)
    board.mainloop()
    
    

if __name__ == "__main__":
    main()