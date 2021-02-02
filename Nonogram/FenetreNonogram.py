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


class FenetreNonogramIndices:
    ACCEPTED_CHARACHTER = [" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def __init__(self, fenetre_parent=None, nonogram=None):
        self.master = Toplevel()
        self.master.title("Indications")
        Label(self.master, text="Renseignez les champs correspondants pour les indices").grid(row=0, column=0, columnspan=5)
        self.hauteur = nonogram.hauteur
        self.largeur = nonogram.largeur
        self.indices_lignes, self.indices_colonnes = nonogram.export_indications()

        okCommandLigne = self.master.register(lambda new_val, ligne=True: self.isOk(new_val, ligne))
        self.label_entry_lignes = list()
        self.textvariables_lignes = list()
        self.entry_lignes = list()
        Label(self.master, text=f"---LIGNES : /!\ largeur = {self.largeur}---").grid(row=1, column=0, columnspan=3)
        grid_i = 2
        grid_j = 0
        for i in range(self.hauteur):
            self.label_entry_lignes.append(Label(self.master, text=f"Ligne {i+1}"))
            self.label_entry_lignes[i].grid(row=grid_i, column=grid_j)
            self.textvariables_lignes.append(StringVar())
            self.entry_lignes.append(Entry(self.master, validate='key', validatecommand=(okCommandLigne, '%P'), textvariable=self.textvariables_lignes[i]))
            self.entry_lignes[i].grid(row=grid_i+1, column=grid_j)
            self.entry_lignes[i].insert(0, self.indice_to_string(self.indices_lignes[i]))
            grid_j += 1
            if grid_j == 5:
                grid_i += 2
                grid_j = 0

        okCommandColonne = self.master.register(self.isOk)
        if grid_j != 0:
            grid_i += 2
            grid_j = 0
        Label(self.master, text=f"---COLONNES : /!\ hauteur = {self.hauteur}---").grid(row=grid_i, column=0, columnspan=3)
        grid_i += 1
        self.label_entry_colonnes = list()
        self.textvariables_colonnes = list()
        self.entry_colonnes = list()
        for i in range(self.largeur):
            self.label_entry_colonnes.append(Label(self.master, text=f"Colonne {i+1}"))
            self.label_entry_colonnes[i].grid(row=grid_i, column=grid_j)
            self.textvariables_colonnes.append(StringVar())
            self.entry_colonnes.append(Entry(self.master, validate='key', validatecommand=(okCommandColonne, '%P'), textvariable=self.textvariables_colonnes[i]))
            self.entry_colonnes[i].grid(row=grid_i+1, column=grid_j)
            self.entry_colonnes[i].insert(0, self.indice_to_string(self.indices_colonnes[i]))
            grid_j += 1
            if grid_j == 5:
                grid_i += 2
                grid_j = 0
        grid_i += 2
        Button(self.master, text="Tout effacer", command=self.clear).grid(row= grid_i, column=0, columnspan=2)
        Button(self.master, text="Enregistrer", command=self.enregister).grid(row= grid_i, column=2, columnspan=2)
        Button(self.master, text="Quitter", command=self.quit).grid(row= grid_i, column=4)

    def run(self):
        self.master.mainloop()

    def isOk(self, nouvelle_valeur, pour_ligne=False):
        buffer = " "
        for i in range(len(nouvelle_valeur)):
            if i > 0:
                buffer = nouvelle_valeur[i-1]
            character = nouvelle_valeur[i]
            if buffer == " " and (character == " " or character == "0"):
                return False
            if character not in self.ACCEPTED_CHARACHTER:
                return False
        indices = self.string_to_indice(nouvelle_valeur)
        if pour_ligne:
            if np.array(indices).sum() + len(indices) - 1 > self.largeur:
                return False
        else:
            if np.array(indices).sum() + len(indices) - 1 > self.hauteur:
                return False
        return True

    def string_to_indice(self, text):
        text += " "
        indices = list()
        buffer = ""
        for c in text:
            if c == " " and buffer != "":
                indices.append(int(buffer))
                buffer = ""
            else:
                buffer += c
        return indices

    def indice_to_string(self, indices):
        text = ""
        for i in range(len(indices)):
            text += str(indices[i])
            if i < len(indices) - 1:
                text += " "
        return text

    def quit(self):
        self.master.quit()
        self.master.destroy()

    def enregister(self):
        self.indices_lignes = list()
        for i in range(len(self.textvariables_lignes)):
            self.indices_lignes.append(self.string_to_indice(self.textvariables_lignes[i].get()))
        self.indices_colonnes = list()
        for stringvar in self.textvariables_colonnes:
            self.indices_colonnes.append(self.string_to_indice(stringvar.get()))

    def clear(self):
        for entry in self.entry_lignes:
            entry.delete(0, "end")
        for entry in self.entry_colonnes:
            entry.delete(0, "end")
