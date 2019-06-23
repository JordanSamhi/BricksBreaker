import tkinter as tk
from modele.modes.ModeUnJoueur import ModeUnJoueur
from modele.modes.ModeDeuxJoueurs import ModeDeuxJoueurs

class PopupMode():
    def __init__(self, app):
        self._application = app
        self._fenetre = tk.Toplevel()
        self._fenetre.grab_set()
        self._fenetre.resizable(width=False, height=False)
        self._fenetre.title('Choix mode')
        self._message = "Choisissez votre mode de jeu"
        tk.Label(self._fenetre, text=self._message).grid(row = 0, column = 0, columnspan = 2)
        tk.Button(self._fenetre, text='1 Joueur', command=self.modeUnJoueur).grid(row = 2, column = 0)
        tk.Button(self._fenetre, text='2 Joueurs', command=self.modeDeuxJoueurs).grid(row = 2, column = 1)
    
    def modeUnJoueur(self):
        self._application.setMode(ModeUnJoueur(self._application))
        self._fenetre.grab_release()
        self._fenetre.destroy()
    
    def modeDeuxJoueurs(self):
        self._application.setMode(ModeDeuxJoueurs(self._application))
        self._fenetre.grab_release()
        self._fenetre.destroy()
    
    def getToplevel(self):
        return self._fenetre