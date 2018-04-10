'''
    Une partie est definie par une liste de case et un score
'''
class Partie():
    def __init__(self, grille):
        self._grille = grille
        self._score = 0
        self._scorePotentiel = 0
        
    def getGrille(self):
        return self._grille
    
    def getScore(self):
        return self._score

    def getScorePotentiel(self):
        return self._scorePotentiel
    
    def setGrille(self, grille):
        self._grille = grille
    
    def getGrilleEnListe(self):
        return self.transformerGrilleEnListe()

    def transformerGrilleEnListe(self):
        l = []
        for i in self._grille:
            for elt in i:
                l.append(elt)
        return l