# Main Driver File - Initial Commit - Andromeda
from TicTacToe import TicTacToe
from TicTacToeGUI import TicTacToeBoard


def main():
    game = TicTacToe()
    board = TicTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()