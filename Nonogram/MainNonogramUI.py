from tkinter import *
from tkinter.ttk import Separator
from Nonogram.NonogramGame import NonogramGame
from Nonogram.FenetreNonogram import FenetreNonogram, FenetreNonogramIndices
import numpy as np


class MainNonogramUI:
    def __init__(self, fenetre_parent=None):
        if fenetre_parent:
            self.master = Toplevel()
        else:
            self.master = Tk()
        self.master.title("Menu Nonogram")
        self.hauteur = 1
        self.largeur = 1
        self.nonogram = NonogramGame(self.hauteur, self.largeur)
        self.board = self.nonogram.export_board()

        self.entree = list()
        self.entree.append(list())
        self.entree[0].append(Button(self.master, text="0", highlightbackground='white', width=1))
        self.entree[0][0]["state"] = "disabled"
        self.entree[0][0].grid(row=1, column=1)

        self.separator_horizontal = list()
        self.separator_vertical = list()

        self.indications_lignes = list()
        self.indications_lignes.append(list())
        self.label_indications_lignes = list()
        self.label_indications_lignes.append(Label(self.master, text="None"))
        self.label_indications_lignes[0].grid(row=1, column=0)
        self.indications_colonnes = list()
        self.indications_colonnes.append(list())
        self.label_indications_colonnes = list()
        self.label_indications_colonnes.append(Label(self.master, text="None"))
        self.label_indications_colonnes[0].grid(row=0, column=1)

        self.column_for_button = self.largeur+(self.largeur-1)//5 + 2
        self.largeur_moins = Button(self.master, text="-", command=lambda val=-1: self.update_largeur(val))
        self.largeur_plus = Button(self.master, text="+", command=lambda val=1: self.update_largeur(val))
        self.largeur_label = Label(self.master, text=str(self.largeur))

        self.hauteur_moins = Button(self.master, text="-", command=lambda val=-1: self.update_hauteur(val))
        self.hauteur_plus = Button(self.master, text="+", command=lambda val=1: self.update_hauteur(val))
        self.hauteur_label = Label(self.master, text=str(self.hauteur))

        self.buttons = list()
        self.buttons.append(Button(self.master, text="Éditer la figure", command=self.dessiner))
        self.buttons.append(Button(self.master, text="Charger une figure", command=self.import_board))
        self.buttons.append(Button(self.master, text="Éditer les indications", command=self.renseigner_indices))
        self.buttons.append(Button(self.master, text="Charger des indications", command=self.import_indications))
        self.buttons.append(Button(self.master, text="Générer les indications", command=self.generer_indices_correspondants))
        self.buttons.append(Button(self.master, text="Résoudre", command=self.solve))
        self.buttons.append(Button(self.master, text="Quitter", command=self.quit))

        self.update_button_grid()

        self.update_taille(10, 10)

    def run(self):
        self.master.mainloop()

    def update_taille(self, largeur, hauteur):
        val = -1
        if largeur > self.largeur:
            val = 1
        for i in range(abs(self.largeur-largeur)):
            self.update_largeur(val)
        val = -1
        if hauteur > self.hauteur:
            val = 1
        for i in range(abs(self.hauteur-hauteur)):
            self.update_hauteur(val)

    def update_largeur(self, val):
        if self.largeur + val > 0:
            self.largeur += val
            self.largeur_label["text"] = str(self.largeur)
            for i in range(len(self.separator_horizontal)):
                self.separator_horizontal[i].grid(column=1, row=6*(i+1), columnspan=self.largeur+(self.largeur-1)//5, sticky='ew')
            if val == 1:
                self.indications_colonnes.append(list())
                self.label_indications_colonnes.append(Label(self.master, text="None"))
                grid_j = (self.largeur - 1) + (self.largeur - 1) // 5 + 1
                self.label_indications_colonnes[self.largeur - 1].grid(row=0, column=grid_j)
                self.board = np.concatenate((self.board, np.zeros((self.hauteur, 1), dtype=int)), axis=1)
                for i in range(self.hauteur):
                    self.entree[i].append(Button(self.master, text="0", highlightbackground='white', width=1))
                    self.entree[i][self.largeur-1]["state"] = "disabled"
                    grid_i = i + i // 5 + 1
                    grid_j = (self.largeur-1) + (self.largeur-1) // 5 + 1
                    self.entree[i][self.largeur-1].grid(row=grid_i, column=grid_j)
                if (self.largeur - 1) % 5 == 0:
                    j = (self.largeur - 1)//5 - 1
                    self.separator_vertical.append(Separator(self.master, orient='vertical'))
                    self.separator_vertical[j].grid(row=1, column=6*(j+1), rowspan=self.hauteur+(self.hauteur-1)//5, sticky='ns')
            else:  # val == -1
                self.indications_colonnes.pop()
                self.label_indications_colonnes.pop().destroy()
                self.board = self.board[:, :self.largeur]
                for i in range(self.hauteur):
                    self.entree[i].pop().destroy()
                if self.largeur % 5 == 0:
                    self.separator_vertical.pop().destroy()
            self.nonogram.import_board(self.board)
            self.nonogram.import_indications(self.indications_lignes, self.indications_colonnes)
            self.column_for_button = self.largeur + (self.largeur - 1) // 5 + 2
            self.update_button_grid()

    def update_hauteur(self, val):
        if self.hauteur + val > 0:
            self.hauteur += val
            self.hauteur_label["text"] = str(self.hauteur)
            for j in range(len(self.separator_vertical)):
                self.separator_vertical[j].grid(row=1, column=6*(j+1), rowspan=self.hauteur+(self.hauteur-1)//5, sticky='ns')
            if val == 1:
                self.indications_lignes.append(list())
                self.label_indications_lignes.append(Label(self.master, text="None"))
                grid_i = (self.hauteur - 1) + (self.hauteur - 1) // 5 + 1
                self.label_indications_lignes[self.hauteur - 1].grid(row=grid_i, column=0)
                self.board = np.concatenate((self.board, np.zeros((1, self.largeur), dtype=int)))
                self.entree.append(list())
                for j in range(self.largeur):
                    self.entree[self.hauteur-1].append(Button(self.master, text="0", highlightbackground='white', width=1))
                    self.entree[self.hauteur-1][j]["state"] = "disabled"
                    grid_i = (self.hauteur-1) + (self.hauteur-1) // 5 + 1
                    grid_j = j + j // 5 + 1
                    self.entree[self.hauteur-1][j].grid(row=grid_i, column=grid_j)
                if (self.hauteur - 1) % 5 == 0:
                    self.separator_horizontal.append(Separator(self.master, orient="horizontal"))
                    i = (self.hauteur - 1) // 5 - 1
                    self.separator_horizontal[i].grid(column=1, row=6*(i+1), columnspan=self.largeur+(self.largeur-1)//5, sticky='ew')
            else:  # val == -1
                self.indications_lignes.pop()
                self.label_indications_lignes.pop().destroy()
                self.board = self.board[:self.hauteur, :]
                for j in range(self.largeur):
                    self.entree[self.hauteur].pop().destroy()
                self.entree.pop()
                if self.hauteur % 5 == 0:
                    self.separator_horizontal.pop().destroy()
            self.nonogram.import_board(self.board)
            self.nonogram.import_indications(self.indications_lignes, self.indications_colonnes)

    def update_button_grid(self):
        self.largeur_moins.grid(row=1, column=self.column_for_button)
        self.largeur_label.grid(row=1, column=self.column_for_button + 1)
        self.largeur_plus.grid(row=1, column=self.column_for_button + 2)
        self.hauteur_moins.grid(row=2, column=self.column_for_button)
        self.hauteur_label.grid(row=2, column=self.column_for_button + 1)
        self.hauteur_plus.grid(row=2, column=self.column_for_button + 2)
        for i in range(len(self.buttons)):
            grid_i = i + (i + 3) // 6
            self.buttons[i].grid(row=grid_i + 3, column=self.column_for_button, columnspan=3)

    def import_board(self, board=None, erase_board=False):
        if board is None:
            board = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                             [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                             [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
                             [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
                             [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
                             [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
                             [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                             [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0],
                             [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                             [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                             [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                             [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
                             [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0],
                             [1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                             [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
                             [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0],
                             [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        if erase_board:
            board = np.zeros(self.board.shape)
        hauteur, largeur = board.shape
        self.update_taille(largeur, hauteur)
        self.board = np.array(board)
        self.nonogram.import_board(self.board)
        self.update_entree_text()

        self.column_for_button = self.largeur + (self.largeur - 1) // 5 + 2
        self.update_button_grid()

    def update_entree_text(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                self.entree[i][j]["text"] = str(self.board[i, j])
                if self.board[i, j] == 0:
                    self.entree[i][j]["highlightbackground"] = 'white'
                    self.entree[i][j]["fg"] = 'black'
                else:
                    self.entree[i][j]["highlightbackground"] = 'black'
                    self.entree[i][j]["fg"] = 'grey'

    def import_indications(self, indications=None):
        if indications is None:
            indications = (
                [[3], [5], [4, 3], [7], [5],
                 [3], [5], [1, 8], [3, 3, 3], [7, 3, 2],
                 [5, 4, 2], [8, 2], [10], [2, 3], [6]],
                [[3], [4], [5], [4], [5],
                 [6], [3, 2, 1], [2, 2, 5], [4, 2, 6], [8, 2, 3],
                 [8, 2, 1, 1], [2, 6, 2, 1], [4, 6], [2, 4], [1]]
            )

        self.update_taille(len(indications[1]), len(indications[0]))
        self.indications_lignes = indications[0]
        self.indications_colonnes = indications[1]
        self.nonogram.import_indications(self.indications_lignes, self.indications_colonnes)

        self.update_label_indication()

    def update_label_indication(self):
        for i in range(len(self.indications_lignes)):
            txt = ""
            if len(self.indications_lignes[i]) == 0:
                txt = "None"
            for j in range(len(self.indications_lignes[i])):
                txt += str(self.indications_lignes[i][j])
                if j < len(self.indications_lignes[i]) - 1:
                    txt += " "
            self.label_indications_lignes[i]["text"] = txt
        for j in range(len(self.indications_colonnes)):
            txt = ""
            if len(self.indications_colonnes[j]) == 0:
                txt = "None"
            for i in range(len(self.indications_colonnes[j])):
                txt += str(self.indications_colonnes[j][i])
                if i < len(self.indications_colonnes[j]) - 1:
                    txt += "\n"
            self.label_indications_colonnes[j]["text"] = txt

    def quit(self):
        self.master.quit()
        self.master.destroy()

    def dessiner(self):
        self.master.withdraw()
        fenetre_dessin = FenetreNonogram(nonogram=self.nonogram, fenetre_parent=self.master)
        fenetre_dessin.run()
        self.master.deiconify()
        self.import_board(fenetre_dessin.data)

    def renseigner_indices(self):
        self.master.withdraw()
        fenetre_indices = FenetreNonogramIndices(nonogram=self.nonogram, fenetre_parent=self.master)
        fenetre_indices.run()
        self.indications_lignes = fenetre_indices.indices_lignes
        self.indications_colonnes = fenetre_indices.indices_colonnes
        self.update_label_indication()
        self.master.deiconify()

    def generer_indices_correspondants(self):
        self.nonogram.create_indication_from_table()
        self.import_indications((self.nonogram.export_indications()))

    def solve(self):
        if self.nonogram.resolution():
            self.board = self.nonogram.export_board()
            self.update_entree_text()
            self.nonogram.afficher()