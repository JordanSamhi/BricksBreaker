'''
    Classe qui fait l'interface entre la vue et le modele
'''
from modele.Case import Case
from modele.couleurs.Liste4Couleurs import Liste4Couleurs
from modele.couleurs.Liste8Couleurs import Liste8Couleurs
import random as r

class Controleur():
    def __init__(self):
        self._limiteNombreCases = 3
        self._semblables = []
    
    def genererGrille(self, taille, listeCouleurs):
        grille = [[None for _ in range(taille)] for _ in range(taille)]
        pile = []
        for i in range(taille):
            for j in range(taille):
                pile.append((i,j))
        r.shuffle(pile)
        for elt in pile:
            grille[elt[0]][elt[1]] = Case(elt[1], elt[0], listeCouleurs.getUneCouleur(), grille)
        return grille
                
    def genererGrille10x10(self):
        return self.genererGrille(10, Liste4Couleurs())
        
    def genererGrille20x20(self):
        return self.genererGrille(20, Liste8Couleurs())
                
    def getSemblablesCase(self, case, voisinsVisites):
        voisins = [v for v in case.getVoisins() if v is not None and v not in voisinsVisites and v.getCouleur() == case.getCouleur()]
        voisinsVisites = voisinsVisites + voisins
        for v in voisins:
            if v != case:
                pass
                voisinsVisites = self.getSemblablesCase(v, voisinsVisites)
        return voisinsVisites
    
    def surbrillanceSemblables(self, case):
        semblables = self.getSemblablesCase(case, [case])
        if len(semblables) >= self._limiteNombreCases:
            for case in semblables:
                case.surbrillance()
        return semblables
            
    def couleurParDefautSemblables(self):
        casesARedessiner = self._semblables
        for case in self._semblables:
            case.couleurParDefaut()
        self._semblables = []
        return casesARedessiner
            
    def gererSurbrillance(self, caseActuelle):
        casesARedessiner = self._semblables
        if caseActuelle not in self._semblables:
            self.couleurParDefautSemblables()
            self._semblables = self.surbrillanceSemblables(caseActuelle)
            casesARedessiner += self._semblables
            return casesARedessiner
        return None
    
    def transformerGrilleEnListe(self, grille):
        l = []
        for i in grille:
            for elt in i:
                l.append(elt)
        return l
        
