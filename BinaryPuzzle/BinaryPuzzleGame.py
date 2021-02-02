class BinaryPuzzleGame:
    def __init__(self, board=None):
        if board is None:
            self.tailleJeu = 6
            self.board = []
            for i in range(self.tailleJeu):
                self.board.append([])
                for j in range(self.tailleJeu):
                    self.board[i].append(None)
        else:
            self.board = board
            self.tailleJeu = len(board)
        self.maxOccurence = int(self.tailleJeu / 2)

    def __copy__(self):
        return BinaryPuzzleGame(self.tailleJeu, self.board)

    def __repr__(self):
        txt = ""
        for i in range(self.tailleJeu):
            for j in range(self.tailleJeu):
                if self.board[i][j] in [0, 1]: txt += str(self.board[i][j])
                else: txt += " "
                if j < self.tailleJeu - 1: txt += "|"
                else: txt += "\n"
            if i < self.tailleJeu - 1:
                txt += "_" * (2*self.tailleJeu - 1) + "\n"
        return txt

    def import_board(self, board):
        self.board = board
        self.tailleJeu = len(board)

    def renseigner(self):
        #print("Entrer 0, 1, rien pour une case vide.")
        #for i in range(self.tailleJeu):
        #    for j in range(self.tailleJeu):
        #        temp = input("Ligne "+str(i)+", colonne "+str(j)+" :")
        #        if temp == "0": self.board[i][j] = 0
        #        elif temp == "1": self.board[i][j] = 1
        #    print(self)
        fenetre = FenetreRenseignement(self.tailleJeu)
        fenetre.entrer()
        self.board = fenetre.getGrid()
        print(self)


    def chercheIndicesSurLigne(self, ligne, binaire):
        indices = []
        for j in range(self.tailleJeu):
            if self.board[ligne][j] == binaire:
                indices.append(j)
        return indices

    def chercheIndicesSurColonne(self, colonne, binaire):
        indices = []
        for i in range(self.tailleJeu):
            if self.board[i][colonne] == binaire:
                indices.append(i)
        return indices

    def possible(self, ligne, colonne):
        possible = [0, 1]

        # on commence par vérifier que le maximum de 0 ou de 1 ne sera pas dépassé.

        compte_colonne = [0, 0]
        for i in range(self.tailleJeu):
            if self.board[i][colonne] is not None:
                compte_colonne[self.board[i][colonne]] += 1
        for binaire in possible.copy():
            if compte_colonne[binaire] == self.maxOccurence:
                possible.remove(binaire)
        if possible == []:
            return possible

        compte_ligne = [0, 0]
        for j in range(self.tailleJeu):
            if self.board[ligne][j] is not None:
                compte_ligne[self.board[ligne][j]] += 1
        for binaire in possible.copy():
            if compte_ligne[binaire] == self.maxOccurence:
                possible.remove(binaire)
        if possible == []:
            return possible
        # on va maintenant vérifier qu'autour de la case concernée, il n'y a pas de double un ou de double deux.
        # on en profite pour vérifier que l'on ne crée pas de triple avec la nouvelle entrée

        double = [False, False]
        for binaire in possible:
            if ligne > 1:
                if self.board[ligne-2][colonne] == binaire and self.board[ligne-1][colonne] == binaire:
                    double[binaire] = True
            if ligne < self.tailleJeu - 2:
                if self.board[ligne+2][colonne] == binaire and self.board[ligne+1][colonne] == binaire:
                    double[binaire] = True
            if ligne > 0 and ligne < self.tailleJeu -1:
                if self.board[ligne-1][colonne] == binaire and self.board[ligne+1][colonne] == binaire:
                    double[binaire] = True
            if colonne > 1:
                if self.board[ligne][colonne-2] == binaire and self.board[ligne][colonne-1] == binaire:
                    double[binaire] = True
            if colonne < self.tailleJeu - 2:
                if self.board[ligne][colonne+2] == binaire and self.board[ligne][colonne+1] == binaire:
                    double[binaire] = True
            if colonne > 0 and colonne < self.tailleJeu -1:
                if self.board[ligne][colonne-1] == binaire and self.board[ligne][colonne+1] == binaire:
                    double[binaire] = True

        for binaire in possible.copy():
            if double[binaire]: possible.remove(binaire)

        if possible == []:
            return possible

        # on va maintenant vérifier qu'on ne remplit pas une ligne ou une colonne à l'identique qu'une autre.

        existeLigneIdentique = [False, False]
        for binaire in possible:
            if compte_ligne[binaire] == self.tailleJeu/2 -1:
                indices = self.chercheIndicesSurLigne(ligne, binaire)
                indices.append(colonne)
                indices.sort()
                for i in range(self.tailleJeu):
                    if i != ligne:
                        indicesTemp = self.chercheIndicesSurLigne(i, binaire)
                        if indices == indicesTemp:
                            existeLigneIdentique[binaire] = True
            if existeLigneIdentique[binaire]: possible.remove(binaire)

        if possible == []:
            return possible

        existeColonneIdentique = [False, False]
        for binaire in possible:
            if compte_colonne[binaire] == self.tailleJeu / 2 - 1:
                indices = self.chercheIndicesSurColonne(colonne, binaire)
                indices.append(ligne)
                indices.sort()
                for j in range(self.tailleJeu):
                    if j != colonne:
                        indicesTemp = self.chercheIndicesSurColonne(j, binaire)
                        if indices == indicesTemp:
                            existeColonneIdentique[binaire] = True
            if existeColonneIdentique[binaire]: possible.remove(binaire)

        return possible
        # je crois que c'est bon là

    def resoudre(self, i=0, j=0):
        if i == self.tailleJeu:
            return True
        jj = j+1
        ii = i
        if jj == self.tailleJeu:
            jj = 0
            ii += 1
        if self.board[i][j] is not None:
            return self.resoudre(ii, jj)
        else:
            possible = self.possible(i, j)
            if possible == []:
                return False
            else:
                for binaire in possible:
                    self.board[i][j] = binaire
                    if self.resoudre(ii, jj):
                        return True
                self.board[i][j] = None
                return False
