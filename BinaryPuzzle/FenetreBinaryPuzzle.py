from tkinter import *
from functools import partial


class FenetreBinaryPuzzle:

    def __init__(self, board=None, play=False, fenetre_parent=None):
        self.tailleFenetre = len(board)
        self.f = Tk()
        self.f.title("Binary Puzzle")
        self.boutons = [[Button(self.f, text="", command=partial(self.changeTexte, i, j)) for j in range(self.tailleFenetre)] for i in range(self.tailleFenetre)]
        self.boutons = list()
        for i in range(self.tailleFenetre):
            self.boutons.append(list())
            for j in range(self.tailleFenetre):
                if board[i][j] is None:
                    self.boutons[i].append(Button(self.f, text="", command=partial(self.changeTexte, i, j), width=1))
                else:
                    self.boutons[i].append(Button(self.f, text=str(board[i][j]), command=partial(self.changeTexte, i, j), width=1))
                    if play:
                        self.boutons[i][j]["state"] = "disabled"
                self.boutons[i][j].grid(row=i, column=j)
        self.register_button = Button(self.f, text="Tout supprimer", command=self.clean_board)
        self.register_button.grid(row=0, column=self.tailleFenetre)
        self.register_button = Button(self.f, text="Enregistrer", command=self.register_data)
        self.register_button.grid(row=1, column=self.tailleFenetre)
        self.quit_button = Button(self.f, text="Valider", command=self.quit)
        self.quit_button.grid(row=3, column=self.tailleFenetre)
        self.data = self.get_board()

    def run(self):
        self.f.mainloop()

    def quit(self):
        self.f.quit()
        self.f.destroy()

    def changeTexte(self, i, j):
        if self.boutons[i][j]["text"] == "":
            self.boutons[i][j]["text"] = "0"
        elif self.boutons[i][j]["text"] == "0":
            self.boutons[i][j]["text"] = "1"
        else:
            self.boutons[i][j]["text"] = ""

    def get_board(self):
        board = [[None for j in range(self.tailleFenetre)] for i in range(self.tailleFenetre)]
        for i in range(self.tailleFenetre):
            for j in range(self.tailleFenetre):
                if self.boutons[i][j]["text"] == "0": board[i][j]= 0
                if self.boutons[i][j]["text"] == "1": board[i][j]= 1
        return board

    def register_data(self):
        self.data = self.get_board()

    def clean_board(self):
        for i in range(self.tailleFenetre):
            for j in range(self.tailleFenetre):
                if self.boutons[i][j]["state"] != "disabled":
                    self.boutons[i][j]["text"] = ""
