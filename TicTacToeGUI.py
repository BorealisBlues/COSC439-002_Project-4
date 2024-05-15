from tkinter import *
import tkinter as tk
from itertools import cycle
from tkinter import font, ttk
from typing import NamedTuple

from TicTacToe import TicTacToe
from TicTacToe import GameEndException  # custom exception for end of game -Andromeda
from connections import TicTacToeServer, TicTacToeClient


class Player(NamedTuple):
    label: str
    color: str


PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)


class TicTacToeBoard(tk.Tk):
    def __init__(self, game: TicTacToe):
        super().__init__()
        self.title("Network Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_initial_screen()
        self.isHost = True
        self.ip_port = {
            "ip": "localhost",
            "port": 9999
        }

    #  Renders the initial screen for selecting player role
    def _create_initial_screen(self):
        self.init_frame = tk.Frame(master=self)
        self.init_frame.pack(expand=True, fill="both")
        welcome = tk.Label(
            master=self.init_frame,
            text="Welcome!",
            font=font.Font(size=28, weight="bold"),
        )
        welcome.pack()
        select_text = tk.Label(master=self.init_frame, text="Will you be hosting or joining another session?")
        select_text.pack()
        host_button = tk.Button(master=self.init_frame, text="Host", command=lambda: self._go_to_create_board_host())
        host_button.pack(padx=5, pady=5)
        join_button = tk.Button(master=self.init_frame, text="Join", command=lambda: self._go_to_join_session())
        join_button.pack(padx=5, pady=5)

    #  Renders top bar menu
    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    #  Renders page for inputting ip/port to join a game
    def _join_session(self):
        self.join_frame = tk.Frame(master=self)
        self.join_frame.pack(expand=True, fill="both")
        join = tk.Label(
            master=self.join_frame,
            text="Join Session",
            font=font.Font(size=28, weight="bold"),
        )
        join.pack()
        ip_text = tk.Label(master=self.join_frame, text="Enter host IP:")
        ip_text.pack()
        self.ip_entry = ttk.Entry(master=self.join_frame)
        self.ip_entry.pack()
        port_text = tk.Label(master=self.join_frame, text="Enter host port:")
        port_text.pack()
        self.port_entry = ttk.Entry(master=self.join_frame)
        self.port_entry.pack()
        submit_button = tk.Button(master=self.join_frame, text="Submit", command=lambda: self._go_to_create_board_join())
        submit_button.pack(padx=5, pady=5)

    #  Function to set up server/destroy initial page/create board
    def _go_to_create_board_host(self):
        self.isHost = True
        connection = TicTacToeServer(game=self._game)
        self._game.setConnection(connection)
        self.init_frame.destroy()
        self._create_board_display()

    #  Destroys initial page and creates join session page
    def _go_to_join_session(self):
        self.isHost = False
        self.init_frame.destroy()
        self._join_session()

    #  Tries to join server, destroys join page, creates board
    def _go_to_create_board_join(self):
        self.ip_port["ip"] = self.ip_entry.get()
        self.ip_port["port"] = int(self.port_entry.get())
        connection = TicTacToeClient(self.ip_port["ip"], self.ip_port["port"], self._game)
        self._game.setConnection(connection)
        self.join_frame.destroy()
        self._create_board_display()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()
        self._create_board_grid()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.getBoardSize()):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.getBoardSize()):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        player = self._game.turn  # i assume this line will be taken changed when we get the netcode in pace
        #if self._game.checkValidMove(row, col):  # The function takeTurn(posX, posY) automatically calls for check
        self._update_button(clicked_btn)  # Valid move now, so this if statment *should* be unnescessary -Andromeda
        try:  # adding try/except block for new exception-based game-end condition
            self._game.takeTurn(player, row, col)
        except ValueError as e:  # ValueError gets raised if A) not the current player's move or B) space is already occupied
            self._update_display("Invalid move!")
        except GameEndException as e:
            if (str(e) == "0"):
                self._update_display(msg="Tied game!", color="red")
            else:
                msg = f'Player "{self._game.turn}" won!'
                color = PLAYERS[self._game.turn - 1].color
                self._update_display(msg, color)
        else:  # this else statement runs in the event of no exception during the try block
            msg = f"{self._game.turn}'s turn"
            self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=PLAYERS[self._game.turn - 1].label)
        clicked_btn.config(fg=PLAYERS[self._game.turn - 1].color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.resetGame()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

    def get_ip_port(self):
        return self.ip_port

    def get_isHost(self):
        return self.isHost


if __name__ == "__main__":  # added for ability to directly run this file for testing
    game = TicTacToe()
    board = TicTacToeBoard(game)
    board.mainloop()
