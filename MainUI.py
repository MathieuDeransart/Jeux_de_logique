from tkinter import *
from Sudoku.MainSudokuUI import MainSudokuUI
from BinaryPuzzle.MainBinaryPuzzleUI import MainBinaryPuzzleUI
from Nonogram.MainNonogramUI import MainNonogramUI
from tkinter.ttk import Separator

class MainUI:
    def __init__(self):
        self.master = Tk()
        self.master.title("Menu Jeux de Logique")
        title_label = Label(self.master, text="Jeux de Logique\nChoisissez un jeu")
        title_label.grid(row=0, column=0)
        Separator(self.master, orient='vertical').grid(column=0, row=1, columnspan=1, sticky='ew')
        self.buttons = list()
        self.buttons.append(Button(self.master, text="Sudoku", command=self.call_sudoku))
        self.buttons.append(Button(self.master, text="Binary Puzzle", command=self.call_binary_puzzle))
        self.buttons.append(Button(self.master, text="Nonogram", command=self.call_nonogram))
        for i in range(len(self.buttons)):
            self.buttons[i].grid(column=0, row=2+i)

    def run(self):
        self.master.mainloop()

    def call_sudoku(self):
        self.master.withdraw()
        sudoku_window = MainSudokuUI(fenetre_parent=self.master)
        sudoku_window.run()
        self.master.deiconify()

    def call_binary_puzzle(self):
        self.master.withdraw()
        binary_puzzle_window = MainBinaryPuzzleUI(fenetre_parent=self.master)
        binary_puzzle_window.run()
        self.master.deiconify()

    def call_nonogram(self):
        self.master.withdraw()
        nonogram_window = MainNonogramUI(fenetre_parent=self.master)
        nonogram_window.run()
        self.master.deiconify()