'''
    Classe qui fait l'interface entre la vue et le modele
'''
from modele.Case import Case
import random as r
from modele.Partie import Partie

class Controleur():
    def __init__(self, application):
        self._application = application
        self._limiteNombreCases = 3
        self._semblables = []
        self._tailleGrille = 0
    
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
                
    def genererPartie(self, taille, listeCouleurs):
        grille = self.genererGrille(taille, listeCouleurs)
        self._application.setPartie(Partie(grille))
        self._tailleGrille = taille
        
    def calculerTaillesCases(self, width, height):
        return (width / self._tailleGrille), (height / self._tailleGrille)
                
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
            if not case.estMorte():
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
    
    def surbrillanceCases(self, event):
        x = int(event.x/self._application.getWidthCase())
        y = int(event.y/self._application.getHeightCase())
        caseActuelle = self._application.getPartie().getGrille()[y][x]
        if not caseActuelle.estMorte():
            casesARedessiner = self.gererSurbrillance(caseActuelle)
            return casesARedessiner
        return None
                
    def desactiverSurbrillance(self, _):
        return self.couleurParDefautSemblables()
    
    def isPartieFinie(self):
        for case in self._application.getPartie().getGrilleEnListe():
            semblables = self.getSemblablesCase(case, [case])
            if len(semblables) >= 3:
                return False
        return True
    
    def TuerCase(self, case):
        case.setCouleur("grey")
    
    
    '''A VOIR !!!!!!!!!!!!!!! '''
    def detruireCase(self, event):
        if len(self._semblables) >= 3:
            for case in self._semblables:
                self.TuerCase(case)
        '''Recuperation des colonnes'''
        listeColonnes = []
        for case in self._semblables:
            listeColonnes.append(case.getX())
        listeColonnes = list(set(listeColonnes))
        '''Pour chaque colonne on compte nombre de cases grises'''
        for col in listeColonnes:
            colonneInverse = [ligne[col] for ligne in self._application.getPartie().getGrille()][::-1]
            for case in colonneInverse:
                if case.getSud():
                    while not case.estMorte() and case.getSud().estMorte():
                        tmp = case
                        case.setY(tmp.getSud().getY())
                        case.setX(tmp.getSud().getX())
        return self._application.updateTailleCanvas(None)
