'''
    Classe qui fait l'interface entre la vue et le modele
'''
from modele.Case import Case
import random as r
from modele.Partie import Partie

class Controleur():
    def __init__(self, application):
        self._application = application
        self._semblables = []
        self._tailleGrille = 0
        self.LIMITE_NOMBRE_CASES = 3
    
    def genererGrille(self, taille, listeCouleurs):
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
                
    def genererPartie(self, taille, listeCouleurs):
        grille = self.genererGrille(taille, listeCouleurs)
        self._application.setPartie(Partie(grille))
        self._tailleGrille = taille
        
    def calculerTaillesCases(self, height, width):
        return (height / self._tailleGrille),(width / self._tailleGrille)
                
    def getSemblablesCase(self, case, voisinsVisites):
        voisins = [v for v in case.getVoisins() if v is not None and v not in voisinsVisites and v.getCouleur() == case.getCouleur()]
        voisinsVisites = voisinsVisites + voisins
        for v in voisins:
            if v != case:
                pass
                voisinsVisites = self.getSemblablesCase(v, voisinsVisites)
        return voisinsVisites
    
    def desactiverSurbrillance(self):
        for case in self._semblables:
            if not case.estDetruite():
                case.couleurParDefaut()
        self._application.getPartie().setCasesModifiees(self._semblables)
        self._application.getPartie().setScorePotentiel(0)
        self._application.update()
        '''re-initialisation de la liste des semblable'''
        self._semblables = []
            
    def surbrillanceCases(self, event):
        x = int(event.x/self._application.getWidthCase())
        y = int(event.y/self._application.getHeightCase())
        caseActuelle = self._application.getPartie().getGrille()[y][x]
        '''
            Si case pas morte, on gere surbrillance
            Si case morte (case grise) on fait rien
        '''
        if not caseActuelle.estDetruite():
            ''' 
                Si on quitte les semblables on remet couleur par defaut
                Sinon on fait rien
            '''
            if caseActuelle not in self._semblables:
                self.desactiverSurbrillance()
                ''' On recupere les nouveaux semblables '''
                self._semblables = self.getSemblablesCase(caseActuelle, [caseActuelle])
                ''' Si il y en a au moins 3, on gere surbrillance '''
                if len(self._semblables) >= self.LIMITE_NOMBRE_CASES:
                    for case in self._semblables:
                        case.surbrillance()
                        self._application.getPartie().setScorePotentiel(len(self._semblables))
                self._application.getPartie().setCasesModifiees(self._semblables)
                self._application.update()
        else:
            self.desactiverSurbrillance()
            
    def isPartieFinie(self):
        for case in self._application.getPartie().getGrilleEnListe():
            if not case.estDetruite():
                semblables = self.getSemblablesCase(case, [case])
                if len(semblables) >= self.LIMITE_NOMBRE_CASES:
                    return False
        return True
    
    def detruireCases(self):
        if len(self._semblables) >= self.LIMITE_NOMBRE_CASES:
            for case in self._semblables:
                case.detruire()
            self._application.getPartie().ajouerScore(len(self._semblables))
            self.gravite()  
        
    def gravite(self):
        ''' Recuperation des colonnes concernees '''
        listeColonnes = []
        for case in self._semblables:
            listeColonnes.append(case.getX())
        listeColonnes = list(set(listeColonnes))
        casesAModifier = []
        ''' pour chaque colonne on la parcours a partir du bas '''
        for col in listeColonnes:
            nouveauBas = None
            casesDetruites = []
            casesADescendre = []
            for i in range(self._tailleGrille - 1, -1, -1):
                ''' Debut traitement de chaque colonne '''
                case =  self._application.getPartie().getGrille()[i][col]
                '''
                    Pour etre nouveau bas, la case doit avoir une case sur elle qui est detruite,
                    Il ne doit pas y avoir de cases deja detruites dans la liste, sinon il peut y en avoir en dessous,
                    Et bien sur la case elle meme ne doit pas etre detruite
                '''
                if nouveauBas == None and case.getNord() and case.getNord().estDetruite() and not casesDetruites and not case.estDetruite():
                    nouveauBas = case
                if case.estDetruite():
                    casesDetruites.append(case)
                elif not case.estDetruite() and casesDetruites:
                    casesADescendre.append(case)
            ''' S'il n'y a pas de nouveau bas, alors on est tout en bas, le nouveau bas est "virtuel" en dessous du bas '''
            if not nouveauBas:
                nouveauBas = Case(col, self._tailleGrille, None, None)
            ''' On monte les cases detruites '''
            for i in range(len(casesDetruites)):
                casesDetruites[i].setY(i)
                self._application.getPartie().getGrille()[casesDetruites[i].getY()][casesDetruites[i].getX()] = casesDetruites[i]
            ''' On descend les cases a descendre '''
            for case in casesADescendre:
                case.setY(nouveauBas.getY() - 1)
                self._application.getPartie().getGrille()[case.getY()][case.getX()] = case
                nouveauBas = case
            casesAModifier += casesDetruites + casesADescendre
        self._application.getPartie().setCasesModifiees(casesAModifier)
        self._application.update()
        self.decalageGauche()
    
    ''' Decalage gauche '''
    def decalageGauche(self):
        while self._application.getPartie().grillePeutDecalerAGauche():
            case = None
            newCase = None
            oldCase = None
            indiceDecalage = 0
            peutDecaler = False
            casesAModifier = []
            ligneBasGrille = self._application.getPartie().getGrille()[self._tailleGrille - 1]            
            for i in range(self._tailleGrille):
                case = ligneBasGrille[i]
                ''' Si colonne vide '''
                if case.estDetruite():
                    indiceDecalage += 1
                    while case.getEst() and case.getEst().estDetruite():
                        indiceDecalage += 1
                        case = case.getEst()
                    break
            ''' Ici la case contient celle du bas de la colonne a decaler '''
            ''' On se position sur la prochaine colonne non detruite a decaler '''
            while case.getEst() and case.estDetruite():
                case = case.getEst()
                peutDecaler = True
            ''' Ici on opere le decalage '''
            if indiceDecalage != 0 and peutDecaler:
                for col in range(case.getX(), self._tailleGrille):
                    for i in range(self._tailleGrille):
                        newCase = self._application.getPartie().getGrille()[i][col]
                        if not newCase.estDetruite():
                            oldCase = self._application.getPartie().getGrille()[i][col - indiceDecalage]
                            if oldCase not in casesAModifier:
                                casesAModifier.append(oldCase)
                            if newCase not in casesAModifier:
                                casesAModifier.append(newCase)
                            newCase.setX(oldCase.getX())
                            oldCase.setX(col)
                            self._application.getPartie().getGrille()[i][col - indiceDecalage] = newCase
                            self._application.getPartie().getGrille()[i][col] = oldCase
            self._application.getPartie().setCasesModifiees(casesAModifier)
            self._application.update()