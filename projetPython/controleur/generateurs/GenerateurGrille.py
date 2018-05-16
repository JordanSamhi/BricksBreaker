from controleur.generateurs.Generateur import Generateur
import random as r
from modele.Case import Case

class GenerateurGrille(Generateur):
    def __init__(self, app):
        Generateur.__init__(self, app)
        
    def generer(self, *args):
        taille, listeCouleurs = args[0], args[1]
        '''
            On melange sinon a la fin les cases ont la meme couleur
            car c'est ce qu'il reste (shuffle)
        '''
        grille = [[None for _ in range(taille)] for _ in range(taille)]
        '''La pile va'''
        listeDeCoordonnees = []
        for i in range(taille):
            for j in range(taille):
                listeDeCoordonnees.append((i,j))
        r.shuffle(listeDeCoordonnees)
        for elt in listeDeCoordonnees:
            grille[elt[0]][elt[1]] = Case(elt[1], elt[0], listeCouleurs.getUneCouleur(), grille)
        return grille