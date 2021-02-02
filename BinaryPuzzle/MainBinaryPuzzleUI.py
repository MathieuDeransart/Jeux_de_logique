from tkinter import *
from BinaryPuzzle.BinaryPuzzleGame import BinaryPuzzleGame
from BinaryPuzzle.FenetreBinaryPuzzle import FenetreBinaryPuzzle


class MainBinaryPuzzleUI:
    def __init__(self, fenetre_parent=None):
        self.binary_puzzle = BinaryPuzzleGame()
        if fenetre_parent:
            self.master = Toplevel()
        else:
            self.master = Tk()
        self.master.title("Menu Binary Puzzle")

        self.taille = 6
        self.entree = list()
        for i in range(self.taille):
            self.entree.append(list())
            for j in range(self.taille):
                self.entree[i].append(Button(self.master, width=1))
                self.entree[i][j]["state"] = "disabled"
                self.entree[i][j].grid(row=i, column=j)

        self.taille_moins = Button(self.master, text="-", command=lambda val=-1: self.update_taille(val))
        self.taille_plus = Button(self.master, text="+", command=lambda val=1: self.update_taille(val))
        self.label_taille = Label(self.master, text=str(self.taille))
        self.taille_moins.grid(row=0, column=self.taille)
        self.taille_plus.grid(row=0, column=self.taille+2)
        self.label_taille.grid(row=0, column=self.taille+1)

        self.buttons = list()
        self.buttons.append(Button(self.master, text="Charger un puzzle binaire", command=self.load_binary_puzzle))
        self.buttons.append(Button(self.master, text="Editer le puzzle", command=self.edit_binary_puzzle))
        self.buttons.append(Button(self.master, text="Jouer", command=self.play_binary_puzzle))
        self.buttons.append(Button(self.master, text="Résoudre", command=self.solve_binary_puzzle))
        self.buttons.append(Button(self.master, text="Quitter", command=self.quit))
        for i in range(len(self.buttons)):
            self.buttons[i].grid(row=i+1, column=self.taille, columnspan=3)

        self.sub_window = None

    def update_taille(self, val):
        if self.taille + 2*val != 0:  # alors on update
            self.taille += 2*val
            board = self.binary_puzzle.board
            if val == 1:
                for i in range(self.taille-2, self.taille):
                    self.entree.append(list())
                    board.append(list())
                    for j in range(self.taille-2):
                        self.entree[i].append(Button(self.master, width=1))
                        self.entree[i][j]["state"] = "disabled"
                        self.entree[i][j].grid(row=i, column=j)
                        board[i].append(None)
                for i in range(self.taille):
                    for j in range(self.taille - 2, self.taille):
                        self.entree[i].append(Button(self.master, width=1))
                        self.entree[i][j]["state"] = "disabled"
                        self.entree[i][j].grid(row=i, column=j)
                        board[i].append(None)
            else:  # val == -1
                for i in range(self.taille+2):
                    for j in range(self.taille, self.taille+2):
                        self.entree[i].pop().destroy()
                        board[i].pop()
                for i in range(self.taille, self.taille+2):
                    for j in range(self.taille):
                        self.entree[i].pop().destroy()
                        board[i].pop()
                self.entree.pop()
                self.entree.pop()
                board.pop()
                board.pop()
            self.binary_puzzle.import_board(board)
            self.taille_moins.grid(row=0, column=self.taille)
            self.taille_plus.grid(row=0, column=self.taille + 2)
            self.label_taille.grid(row=0, column=self.taille + 1)
            self.label_taille["text"] = str(self.taille)
            for i in range(len(self.buttons)):
                self.buttons[i].grid(row=i+1, column=self.taille, columnspan=3)

    def run(self):
        self.master.mainloop()

    def quit(self):
        self.master.quit()
        self.master.destroy()

    def load_binary_puzzle(self, board=None):
        if board is None:
            board = [
                [None, None, None, 0, None, None],
                [None, None, None, 1, None, None],
                [1, None, None, None, None, 1],
                [None, None, 0, None, None, 1],
                [None, 1, None, None, None, None],
                [None, None, None, 0, None, None],
            ]
        self.binary_puzzle.import_board(board)
        for i in range(self.taille):
            for j in range(self.taille):
                self.entree[i][j].destroy()
        self.taille = len(board)
        self.label_taille["text"] = str(self.taille)
        self.entree = list()
        for i in range(self.taille):
            self.entree.append(list())
            for j in range(self.taille):
                if board[i][j] is not None:
                    self.entree[i].append(Button(self.master, width=1, text=str(board[i][j])))
                else:
                    self.entree[i].append(Button(self.master, width=1))
                self.entree[i][j]["state"] = "disabled"
                self.entree[i][j].grid(row=i, column=j)
        self.taille_moins.grid(row=0, column=self.taille)
        self.taille_plus.grid(row=0, column=self.taille + 2)
        self.label_taille.grid(row=0, column=self.taille + 1)
        self.label_taille["text"] = str(self.taille)
        for i in range(len(self.buttons)):
            self.buttons[i].grid(row=i + 1, column=self.taille, columnspan=3)

    def edit_binary_puzzle(self):
        self.sub_window = FenetreBinaryPuzzle(board=self.binary_puzzle.board, fenetre_parent=self.master)
        self.master.withdraw()
        self.sub_window.run()
        # after closing the sub_window:
        self.master.deiconify()
        board = self.sub_window.data
        self.load_binary_puzzle(board)

    def play_binary_puzzle(self):
        self.sub_window = FenetreBinaryPuzzle(board=self.binary_puzzle.board, fenetre_parent=self.master, play=True)
        self.master.withdraw()
        self.sub_window.run()
        # after closing the sub_window:
        self.master.deiconify()
        board = self.sub_window.data
        self.load_binary_puzzle(board)

    def solve_binary_puzzle(self):
        if self.binary_puzzle.resoudre():
            board = self.binary_puzzle.board
            self.load_binary_puzzle(board)
        else:
            print("Aucune solution trouvée, vérifiez les données d'entrée")
