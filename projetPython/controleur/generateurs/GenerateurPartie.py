from controleur.generateurs.Generateur import Generateur
from controleur.generateurs.GenerateurGrille import GenerateurGrille
from modele.Partie import Partie

class GenerateurPartie(Generateur):
    def __init__(self, app):
        Generateur.__init__(self, app)
        self._generateurGrille = GenerateurGrille(self._application)
        
    def generer(self, *args):
        taille, listeCouleurs = args[0], args[1]
        grille = self._generateurGrille.generer(taille, listeCouleurs)
        self._application.setPartie(Partie(grille))
        self._tailleGrille = taille