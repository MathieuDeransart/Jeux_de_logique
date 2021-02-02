import numpy as np
from Nonogram.FenetreNonogram import FenetreNonogram
import matplotlib.pyplot as plt


class NonogramGame:
    def __init__(self, hauteur=10, largeur=10, indication_lignes=None, indication_colonnes=None):
        self.largeur = largeur  # = nombre de colonne
        self.hauteur = hauteur  # = nombre de ligne
        self.table = np.zeros((self.hauteur, self.largeur), dtype=int)
        if indication_lignes is None:
            self.indication_lignes = list()
        else:
            self.indication_lignes = indication_lignes
        if indication_lignes is None:
            self.indication_colonnes = list()
        else:
            self.indication_colonnes = indication_colonnes
        self.ligne_max_atteinte = 0

    def saisie_indications(self):
        for i in range(self.largeur):
            print(i+1, "ème colone :")
            n = input("Nombre d'indices : ")
            temp_list = list()
            for j in range(int(n)):
                temp_list.append(int(input(f"{j+1} ème indice :")))
            self.indication_colonnes.append(temp_list)
        for i in range(self.hauteur):
            print(i+1, "ème ligne :")
            n = input("Nombre d'indices : ")
            temp_list = list()
            for j in range(int(n)):
                temp_list.append(int(input(f"{j+1} ème indice :")))
            self.indication_lignes.append(temp_list)

    def coup_possibles(self, ligne, colonne, case_a_remplir, nbr_indices_utilises, case_vide):
        # Conflits sur la colonne
        car = 0
        cv = False
        niu = 0
        for i in range(ligne):
            if self.table[i, colonne] == 1:
                if car == 0:
                    car = self.indication_colonnes[colonne][niu]-1
                    niu += 1
                else:
                    car -= 1
                if car == 0:
                    cv = True
            else:
                cv = False
        # Si cv = True, il faut qu'on obtienne une case vide en regardant sur la ligne
        # De même si car == 0 et que niu = len(self.indication_colonnes[colonne])
        # Si car > 0, il faut qu'on obtienne une case pleine en regardant sur la colonne
        need_true = car > 0
        need_false = cv or (car == 0 and niu == len(self.indication_colonnes[colonne]))

        if colonne == self.largeur-1:
            if case_a_remplir > 1:
                return []
            elif case_vide and nbr_indices_utilises < len(self.indication_lignes[ligne]):
                return []
            elif nbr_indices_utilises < len(self.indication_lignes[ligne])-1:
                return []
            elif nbr_indices_utilises == len(self.indication_lignes[ligne])-1:
                if case_vide or cv or self.indication_lignes[ligne][-1] > 1:
                    return []

        # Check sur la ligne
        if case_a_remplir > 0 and not need_false:
            return [True]
        if case_vide and not need_true:
            return [False]
        if case_a_remplir == 0 and nbr_indices_utilises >= len(self.indication_lignes[ligne]) and not need_true:
            return [False]
        if case_a_remplir == 0 and nbr_indices_utilises < len(self.indication_lignes[ligne]):
            if need_true:
                return [True]
            elif need_false:
                return [False]
            else:
                return [True, False]
        return []

    def result(self, ligne, colonne, case_a_remplir, nbr_indices_utilises, case_vide, coup):
        if coup:
            self.table[ligne, colonne] = 1
            if case_a_remplir == 0:
                case_a_remplir = self.indication_lignes[ligne][nbr_indices_utilises]-1
                nbr_indices_utilises += 1
            else:
                case_a_remplir -= 1
            if case_a_remplir == 0:
                case_vide = True
        else:
            self.table[ligne, colonne] = 0
            case_vide = False
        colonne += 1
        if colonne >= self.largeur:
            colonne = 0
            ligne += 1
            if ligne > self.ligne_max_atteinte:
                print(f"On a atteint au max la ligne {ligne}")
                self.ligne_max_atteinte = ligne
            nbr_indices_utilises = 0
            case_vide = False
        return ligne, colonne, case_a_remplir, nbr_indices_utilises, case_vide

    def resolution(self, ligne=0, colonne=0, case_a_remplir=0, nbr_indices_utilises=0, case_vide=False):
        if ligne >= self.hauteur:
            print("Réussie ?")
            return True
        liste_coup = self.coup_possibles(ligne, colonne, case_a_remplir, nbr_indices_utilises, case_vide)
        for coup in liste_coup:
            # print(f"Ligne: {ligne}, Colonne: {colonne}, Case_a_remplir: {case_a_remplir}, Nbr_indices_utilise: "
            #       f"{nbr_indices_utilises}, Case_vide: {case_vide}, Coup: {coup}, liste_coup: {liste_coup}")
            nligne, ncolonne, ncase_a_remplir, nnbr_indices_utilises, ncase_vide = self.result(ligne, colonne, case_a_remplir, nbr_indices_utilises, case_vide, coup)
            # print(self.table)
            if self.resolution(nligne, ncolonne, ncase_a_remplir, nnbr_indices_utilises, ncase_vide):
                return True
        self.table[ligne, colonne] = 0
        return False

    def create_indication_from_table(self):
        self.indication_lignes = list()
        self.indication_colonnes = list()
        for ligne in range (self.hauteur):
            nbr_pixels = 0
            self.indication_lignes.append(list())
            for j in range(self.largeur):
                if self.table[ligne, j] == 0 and nbr_pixels != 0:
                    self.indication_lignes[ligne].append(nbr_pixels)
                    nbr_pixels = 0
                elif self.table[ligne, j] == 1:
                    nbr_pixels += 1
                if j == self.largeur - 1 and nbr_pixels != 0:
                    self.indication_lignes[ligne].append(nbr_pixels)

        for colonne in range (self.largeur):
            nbr_pixels = 0
            self.indication_colonnes.append(list())
            for i in range(self.hauteur):
                if self.table[i, colonne] == 0 and nbr_pixels != 0:
                    self.indication_colonnes[colonne].append(nbr_pixels)
                    nbr_pixels = 0
                elif self.table[i, colonne] == 1:
                    nbr_pixels += 1
                if i == self.hauteur - 1 and nbr_pixels != 0:
                    self.indication_colonnes[colonne].append(nbr_pixels)

    def dessiner(self):
        fenetre = FenetreNonogram(self.largeur, self.hauteur)
        fenetre.entrer()
        self.table = np.array(fenetre.getGrid())
        print(self.table)

    def editer(self):
        fenetre = FenetreNonogram(self.largeur, self.hauteur, self.table)
        fenetre.entrer()
        self.table = np.array(fenetre.getGrid())
        print(self.table)

    def afficher(self):
        plt.imshow(self.table)
        plt.show()

    def import_board(self, board):
        self.table = np.array(board)
        self.hauteur, self.largeur = self.table.shape

    def import_indications(self, indication_lignes, indication_colonnes):
        self.indication_lignes = indication_lignes
        self.indication_colonnes = indication_colonnes
        self.largeur = len(self.indication_colonnes)  # = nombre de colonne
        self.hauteur = len(self.indication_lignes)  # = nombre de ligne
        self.table = np.zeros((self.hauteur, self.largeur), dtype=int)

    def export_board(self):
        return self.table

    def export_indications(self):
        return self.indication_lignes, self.indication_colonnes
