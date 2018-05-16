from modele.Joueur import Joueur

'''
    Une partie est definie par une liste de case et un score
'''
class Partie():
    def __init__(self, grille):
        self._grille = grille
        self._score = 0
        self._scorePotentiel = 0
        self._casesModifiees = []
        self._moi, self._adversaire = Joueur(True), Joueur(False)
        
    def getMoi(self):
        return self._moi
    
    def getAdversaire(self):
        return self._adversaire
        
    def getGrille(self):
        return self._grille
    
    def getScore(self):
        return self._score
    
    def getTailleGrille(self):
        return len(self._grille)

    def getScorePotentiel(self):
        return self._scorePotentiel
    
    def setScore(self, newScore):
        self._score = newScore
    
    def setScorePotentiel(self, newScorePotentiel):
        self._scorePotentiel = newScorePotentiel
        
    def ajouerScore(self, scoreEnPlus):
        self._score += scoreEnPlus
    
    def setGrille(self, grille):
        self._grille = grille
        
    def getCasesModifiees(self):
        return self._casesModifiees
    
    def setCasesModifiees(self, casesModifiees):
        self._casesModifiees = casesModifiees
    
    def getGrilleEnListe(self):
        return self.transformerGrilleEnListe()

    def transformerGrilleEnListe(self):
        l = []
        for i in self._grille:
            for elt in i:
                l.append(elt)
        return l
    
    def grillePeutDecalerAGauche(self):
        for i in range(len(self._grille)):
            case = self._grille[len(self._grille) - 1][i] 
            if case.estDetruite():
                while case.getEst():
                    case = case.getEst()
                    if not case.estDetruite():
                        return True
        return False
            
    
    