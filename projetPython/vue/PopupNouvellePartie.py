import tkinter as tk
from modele.couleurs.Liste4Couleurs import Liste4Couleurs
from modele.couleurs.Liste8Couleurs import Liste8Couleurs
from controleur.generateurs.GenerateurPartie import GenerateurPartie

class PopupNouvellePartie():
    def __init__(self, app):
        self._fenetre = tk.Toplevel()
        self._fenetre.grab_set()
        self._fenetre.resizable(width=False, height=False)
        self._generateurPartie = GenerateurPartie(app)
        self._fenetre.title('Nouvelle Partie')
        self._message = "Choix du mode de jeu"
        tk.Label(self._fenetre, text=self._message).grid(row = 0, column = 0, columnspan = 2)
        tk.Button(self._fenetre, text='10x10', command=self.nouvellePartie10x10).grid(row = 2, column = 0)
        tk.Button(self._fenetre, text='20x20', command=self.nouvellePartie20x20).grid(row = 2, column = 1)
    
    def nouvellePartie10x10(self):
        self._generateurPartie.generer(10, Liste4Couleurs())
        self._fenetre.grab_release()
        self._fenetre.destroy()
    
    def nouvellePartie20x20(self):
        self._generateurPartie.generer(20, Liste8Couleurs())
        self._fenetre.grab_release()
        self._fenetre.destroy()
    
    def getToplevel(self):
        return self._fenetre