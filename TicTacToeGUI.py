from tkinter import *
from tkinter import ttk
import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

from TicTacToe import TicTacToe


class Player(NamedTuple):
    label: str
    color: str


PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

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
        player = self._game.turn
        if self._game.checkValidMove(row, col):
            self._update_button(clicked_btn)
            self._game.takeTurn(player, row, col)
            if self._game.checkTie(row, col):
                self._update_display(msg="Tied game!", color="red")
            elif self._game.checkWin(row, col):
                # self._highlight_cells()
                msg = f'Player "{self._game.turn}" won!'
                color = PLAYERS[self._game.turn - 1].color
                self._update_display(msg, color)
            else:
                self._game.changeTurn()
                msg = f"{self._game.turn}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=PLAYERS[self._game.turn - 1].label)
        clicked_btn.config(fg=PLAYERS[self._game.turn - 1].color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    # def _highlight_cells(self):
    #     for button, coordinates in self._cells.items():
    #         if coordinates in self._game.winner_combo:
    #             button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")