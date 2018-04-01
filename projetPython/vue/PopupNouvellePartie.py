import tkinter as tk
from Tools.demo.ss1 import center

class PopupNouvellePartie(object):
    '''
    classdocs
    '''

    def __init__(self, application):
        self._fenetre = tk.Toplevel()
        self._application = application
        self._fenetre.title('Nouvelle Partie')
        self._message = "Choix du mode de jeu"
        tk.Label(self._fenetre, text=self._message).grid(row = 0, column = 0, columnspan = 2)
        tk.Button(self._fenetre, text='10x10', command=self.nouvellePartie10x10).grid(row = 2, column = 0)
        tk.Button(self._fenetre, text='20x20', command=self.nouvellePartie20x20).grid(row = 2, column = 1)
    
    def nouvellePartie10x10(self):
        self._application.genererPartie10x10()
        self._fenetre.destroy()
    
    def nouvellePartie20x20(self):
        self._application.genererPartie20x20()
        self._fenetre.destroy()
    
    def getToplevel(self):
        return self._fenetre