from tkinter import *
from tkinter.ttk import Separator
from Sudoku.SudokuGame import SudokuGame
from Sudoku.FenetreSudoku import FenetreSudoku


class MainSudokuUI:
    def __init__(self, fenetre_parent=None):
        self.sudoku = SudokuGame()
        board = self.sudoku.get_board()
        if fenetre_parent:
            self.master = Toplevel()
        else:
            self.master = Tk()
        self.master.title("Menu SUDOKU")
        self.entree = list()
        self.textvariables = list()
        for i in range(9):
            self.entree.append(list())
            self.textvariables.append(list())
            for j in range(9):
                self.textvariables[i].append(StringVar())
                self.entree[i].append(Entry(self.master, width=1, textvariable=self.textvariables[i][j]))
                self.entree[i][j]["state"] = "disabled"
                if board[i, j] != 0:
                    self.entree[i][j].insert(0, str(board[i, j]))
                grid_i = i
                grid_j = j
                if i > 2:
                    grid_i += 1
                if i > 5:
                    grid_i += 1
                if j > 2:
                    grid_j += 1
                if j > 5:
                    grid_j += 1
                self.entree[i][j].grid(row=grid_i, column=grid_j)
        Separator(self.master, orient='vertical').grid(column=3, row=0, rowspan=11, sticky='ns')
        Separator(self.master, orient='vertical').grid(column=7, row=0, rowspan=11, sticky='ns')
        Separator(self.master, orient='horizontal').grid(column=0, row=3, columnspan=11, sticky='ew')
        Separator(self.master, orient='horizontal').grid(column=0, row=7, columnspan=11, sticky='we')

        self.buttons = list()
        self.buttons.append(Button(self.master, text="Éditer le sudoku", command=self.edit_sudoku))
        self.buttons[0].grid(column=12, row=0)
        self.buttons.append(Button(self.master, text="Charger un sudoku aléatoire", command=self.load_sudoku))
        self.buttons[1].grid(column=12, row=2)
        self.buttons.append(Button(self.master, text="Jouer", command=self.play_sudoku))
        self.buttons[2].grid(column=12, row=5)
        self.buttons.append(Button(self.master, text="Résoudre automatiquement", command=self.solve_sudoku))
        self.buttons[3].grid(column=12, row=8)
        self.buttons.append(Button(self.master, text="Quitter", command=self.quit))
        self.buttons[4].grid(column=12, row=10)

        self.sub_window = None

    def run(self):
        self.master.mainloop()

    def quit(self):
        self.master.quit()
        self.master.destroy()

    def edit_sudoku(self):
        self.sub_window = FenetreSudoku(self.sudoku.get_board(), fenetre_parent=self.master)
        self.master.withdraw()
        self.sub_window.run()
        # after closing the sub_window:
        self.master.deiconify()
        board = self.sub_window.data
        self.sudoku.import_board(board)
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self.textvariables[i][j].set(str(board[i][j]))
                else:
                    self.textvariables[i][j].set("")

    def load_sudoku(self):
        board = [
            [1, 0, 0, 0, 0, 0, 0, 0, 6],
            [0, 0, 6, 0, 2, 0, 7, 0, 0],
            [7, 8, 9, 4, 5, 0, 1, 0, 3],
            [0, 0, 0, 8, 0, 7, 0, 0, 4],
            [0, 0, 0, 0, 3, 0, 0, 0, 0],
            [0, 9, 0, 0, 0, 4, 2, 0, 1],
            [3, 1, 2, 9, 7, 0, 0, 4, 0],
            [0, 4, 0, 0, 1, 2, 0, 7, 8],
            [9, 0, 8, 0, 0, 0, 0, 0, 0]
        ]
        self.sudoku.import_board(board)
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self.textvariables[i][j].set(str(board[i][j]))
                else:
                    self.textvariables[i][j].set("")

    def play_sudoku(self):
        self.sub_window = FenetreSudoku(self.sudoku.get_board(), fenetre_parent=self, play=True)
        self.master.withdraw()
        self.sub_window.run()
        # after closing the sub_window:
        self.master.deiconify()
        board = self.sub_window.data
        self.sudoku.import_board(board)
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self.textvariables[i][j].set(str(board[i][j]))
                else:
                    self.textvariables[i][j].set("")

    def solve_sudoku(self):
        if self.sudoku.resolution():
            board = self.sudoku.get_board()
            for i in range(9):
                for j in range(9):
                    if board[i, j] != 0:
                        self.textvariables[i][j].set(str(board[i, j]))
        else:
            print("Aucune solution, vérifiez les données d'entrée")
