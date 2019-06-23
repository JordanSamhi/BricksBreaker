from controleur.generateurs.Generateur import Generateur
from controleur.generateurs.GenerateurGrille import GenerateurGrille
from modele.Partie import Partie

class GenerateurPartie(Generateur):
    def __init__(self, mode):
        Generateur.__init__(self, mode)
        self._generateurGrille = GenerateurGrille(self._mode)
        
    def generer(self, *args):
        taille, listeCouleurs = args[0], args[1]
        grille = self._generateurGrille.generer(taille, listeCouleurs)
        self._mode.setPartie(Partie(grille))