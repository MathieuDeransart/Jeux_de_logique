from tkinter import *
from tkinter.ttk import Separator


class FenetreSudoku:
    ACCEPTED_CHARACHTER = ["", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def __init__(self, board=None, play=False, fenetre_parent=None):
        if fenetre_parent:
            self.master = Toplevel()
        else:
            self.master = Tk()
        self.master.title("Sudoku")
        self.entree = list()
        self.textvariables = list()
        okCommand = self.master.register(self.isOk)
        for i in range(9):
            self.entree.append(list())
            self.textvariables.append(list())
            for j in range(9):
                self.textvariables[i].append(StringVar())
                self.entree[i].append(Entry(self.master, width=1, validate='key', validatecommand=(okCommand, '%P'), textvariable=self.textvariables[i][j]))
                self.entree[i][j].bind('<Right>', lambda event, ligne=i, colonne=j: self.rightKey(event, ligne, colonne))
                self.entree[i][j].bind('<Left>', lambda event, ligne=i, colonne=j: self.leftKey(event, ligne, colonne))
                self.entree[i][j].bind('<Up>', lambda event, ligne=i, colonne=j: self.upKey(event, ligne, colonne))
                self.entree[i][j].bind('<Down>', lambda event, ligne=i, colonne=j: self.downKey(event, ligne, colonne))
                self.entree[i][j].bind('<FocusIn>', lambda event, ligne=i, colonne=j: self.callbackSelect(event, ligne, colonne))
                if board[i, j] != 0:
                    self.entree[i][j].insert(0, str(board[i, j]))
                    if play:
                        self.entree[i][j]["state"] = "disabled"
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
        self.quit_button = Button(self.master, text="Valider", command=self.quit)
        self.quit_button.grid(column=12, row=2)
        self.register_button = Button(self.master, text="Enregistrer", command=self.register_data)
        self.register_button.grid(column=12, row=0)

        self.data = self.getData()

    def isOk(self, nouvelle_valeur):
        return nouvelle_valeur in FenetreSudoku.ACCEPTED_CHARACHTER

    def callbackSelect(self, event, i, j):
        self.entree[i][j].selection_range(0, END)

    def rightKey(self, event, i, j):
        if j == 8:
            self.entree[i][0].focus()
        else:
            self.entree[i][j+1].focus()

    def leftKey(self, event, i, j):
        if j == 0:
            self.entree[i][8].focus()
        else:
            self.entree[i][j - 1].focus()

    def upKey(self, event, i, j):
        if i == 0:
            self.entree[8][j].focus()
        else:
            self.entree[i - 1][j].focus()

    def downKey(self, event, i, j):
        if i == 8:
            self.entree[0][j].focus()
        else:
            self.entree[i + 1][j].focus()

    def run(self):
        self.master.mainloop()

    def quit(self):
        self.master.quit()
        self.master.destroy()

    def getData(self):
        result = list()
        for i in range(9):
            result.append(list())
            for j in range(9):
                buffer = self.textvariables[i][j].get()
                if buffer == "":
                    result[i].append(0)
                else:
                    result[i].append(int(buffer))
        return result

    def register_data(self):
        self.data = self.getData()
