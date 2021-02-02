import numpy as np


def liste_indices_carre(i, j):
    ligne = i//3
    colonne = j//3
    indices = list()
    for i in range(3):
        for j in range(3):
            indices.append((3*ligne+i, 3*colonne+j))
    return indices


class SudokuGame:
    COUPS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self):
        self.board = np.zeros((9, 9))

    def __repr__(self):
        txt = ""
        for i in range(9):
            for j in range(9):
                number = self.board[i, j]
                if number != 0:
                    txt += str(self.board[i, j])
                else:
                    txt += " "
                if j == 2 or j == 5:
                    txt += "|"
            txt += "\n"
            if i == 2 or i == 5:
                txt += "---+---+---" + "\n"
        return txt

    def import_board(self, board):
        self.board = np.array(board)

    def coups_possibles(self, ligne, colonne):
        coups_possibles = list()
        coups_impossibles_droite = self.coups_impossibles_droite(ligne, colonne)
        coups_impossibles_carre = self.coups_impossibles_carre(ligne, colonne)
        for coup in range(1, 10):
            if coup not in coups_impossibles_droite and coup not in coups_impossibles_carre:
                coups_possibles.append(coup)
        return coups_possibles

    def coups_impossibles_droite(self, ligne, colonne):
        coups_impossibles = list()
        for i in range(9):
            if self.board[i, colonne] != 0:
                coups_impossibles.append(self.board[i, colonne])
        for j in range(9):
            if self.board[ligne, j] != 0:
                coups_impossibles.append(self.board[ligne, j])
        return coups_impossibles

    def coups_impossibles_carre(self, ligne, colonne):
        coups_impossibles = list()
        for i, j in liste_indices_carre(ligne, colonne):
            if self.board[i, j] != 0:
                coups_impossibles.append(self.board[i, j])
        return coups_impossibles

    def resolution(self, ligne=0, colonne=0):
        if ligne >= 9:
            return True
        c = colonne + 1
        if c >= 9:
            c = 0
            l = ligne+1
        else:
            l = ligne

        if self.board[ligne, colonne] != 0:
            return self.resolution(l, c)
        else:
            for coup in self.coups_possibles(ligne, colonne):
                self.board[ligne, colonne] = coup
                if self.resolution(l, c):
                    return True
            self.board[ligne, colonne] = 0
        return False

    def get_board(self):
        return self.board
