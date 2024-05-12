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
    ## IF HOST
    server = TicTacToeServer(game1) # initialize server
    ## IF NOT HOST
    game2 = TicTacToe()
    board2 = TicTacToeBoard(game2)
    client = TicTacToeClient(game2)
    ## prompt for server IP & port
    ## create client object
    board1.mainloop()
    board2.mainloop()


if __name__ == "__main__":
    main()