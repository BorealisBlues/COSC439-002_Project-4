# Main Driver File - Initial Commit - Andromeda
from TicTacToe import TicTacToe
from TicTacToeGUI import TicTacToeBoard


def main():
    ##  TODO:
    ##      - Add a screen for Create Game (host server) / Join Game (run client)
    ##      - impliment netcode into GUI
    ##      - TEST the netcode and make sure we dont have weird bugs in it
    ##      - Fix Bug in TicTacToe.py : Diagonal win checking only procs on \ direction not / direction
    
    
    game = TicTacToe()
    board = TicTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()