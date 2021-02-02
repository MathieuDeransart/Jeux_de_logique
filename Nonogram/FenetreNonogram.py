from tkinter import *
from functools import partial
import numpy as np


class FenetreNonogram:
    def __init__(self, nonogram=None, fenetre_parent=None):
        self.largeurFenetre = nonogram.largeur
        self.hauteurFenetre = nonogram.hauteur
        if fenetre_parent:
            self.f = Toplevel()
        else:
            self.f = Tk()
        self.f.title("Fenetre Dessin")
        self.data = nonogram.export_board()
        self.boutons = [[Button(self.f, text=str(self.data[i, j]), highlightbackground='white', command=partial(self.changeTexte, i, j)) for j in range(self.largeurFenetre)] for i in range(self.hauteurFenetre)]
        for i in range(self.hauteurFenetre):
            for j in range(self.largeurFenetre):
                if self.data[i, j] == 1:
                    self.boutons[i][j]["highlightbackground"] = 'black'
                    self.boutons[i][j]["fg"] = 'grey'
                self.boutons[i][j].grid(row=i, column=j)
        self.buttons = list()
        self.buttons.append(Button(self.f, text="Tout effacer", command=self.erase))
        self.buttons.append(Button(self.f, text="Enregistrer", command=self.register_data))
        self.buttons.append(Button(self.f, text="Quitter", command=self.quit))
        for i in range(len(self.buttons)):
            self.buttons[i].grid(row=i+1, column=self.largeurFenetre+1)

    def changeTexte(self, i, j):
        if self.boutons[i][j]["text"] == "0":
            self.boutons[i][j]["text"] = "1"
            self.boutons[i][j]["highlightbackground"] = 'black'
            self.boutons[i][j]["fg"] = 'grey'
        else:
            self.boutons[i][j]["text"] = "0"
            self.boutons[i][j]["highlightbackground"] = 'white'
            self.boutons[i][j]["fg"] = 'black'

    def run(self):
        self.f.mainloop()

    def register_data(self):
        self.data = np.zeros((self.hauteurFenetre, self.largeurFenetre), dtype=int)
        for i in range(self.hauteurFenetre):
            for j in range(self.largeurFenetre):
                if self.boutons[i][j]["text"] == "1":
                    self.data[i, j] = 1

    def erase(self):
        for i in range(self.hauteurFenetre):
            for j in range(self.largeurFenetre):
                self.boutons[i][j]["text"] = "0"
                self.boutons[i][j]["highlightbackground"] = 'white'
                self.boutons[i][j]["fg"] = 'black'

    def quit(self):
        self.f.quit()
        self.f.destroy()
