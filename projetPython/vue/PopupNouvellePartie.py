import tkinter as tk
from modele.couleurs.Liste4Couleurs import Liste4Couleurs
from modele.couleurs.Liste8Couleurs import Liste8Couleurs

class PopupNouvellePartie(object):
    '''
    classdocs
    '''

    def __init__(self, controleur):
        self._fenetre = tk.Toplevel()
        self._controleur = controleur
        self._fenetre.title('Nouvelle Partie')
        self._message = "Choix du mode de jeu"
        tk.Label(self._fenetre, text=self._message).grid(row = 0, column = 0, columnspan = 2)
        tk.Button(self._fenetre, text='10x10', command=self.nouvellePartie10x10).grid(row = 2, column = 0)
        tk.Button(self._fenetre, text='20x20', command=self.nouvellePartie20x20).grid(row = 2, column = 1)
    
    def nouvellePartie10x10(self):
        self._controleur.genererPartie(10, Liste4Couleurs())
        self._fenetre.destroy()
    
    def nouvellePartie20x20(self):
        self._controleur.genererPartie(20, Liste8Couleurs())
        self._fenetre.destroy()
    
    def getToplevel(self):
        return self._fenetre