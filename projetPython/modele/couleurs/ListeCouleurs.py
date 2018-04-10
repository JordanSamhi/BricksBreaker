import random
'''
    Cette classe definie les couleurs du jeu
    Deux listes, une pour 10x10 et une pour 20x20
    Deux methodes de recuperation aleatoire de couleurs dans ces tuples
'''
class ListeCouleurs():
    def __init__(self):
        self._listeCouleurs = ()
        self._compteursCouleurs = {}
        self.generateListesCouleurs()
        
    '''
        Generation des tuples de couleur 
        Mise a 0 des compteurs de couleurs
    '''
    def generateListesCouleurs(self):
        self._listeCouleurs = self.definitionCouleurs()
        for elt in self._listeCouleurs:
            self._compteursCouleurs[elt] = 0
        
    '''
        On recupere une couleur aleatoirement dans notre liste
        On incremente notre compteur de 1
        Si le compteur atteint 25, on supprime la couleur du tuple
    '''
    def getUneCouleur(self):
        couleur = self._listeCouleurs[random.randrange(len(self._listeCouleurs))]
        self._compteursCouleurs[couleur] += 1
        if self._compteursCouleurs[couleur] == self.getLimiteCouleur():
            self._listeCouleurs = [coul for coul in self._listeCouleurs if coul != couleur]
        return couleur

    def getCouleurCaseMorte(self):
        return "grey"