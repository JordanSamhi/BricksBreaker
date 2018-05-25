from controleur.generateurs.GenerateurSemblables import GenerateurSemblables
from modele.Case import Case

class ActionCases():
    def __init__(self, mode, app):
        self._mode = mode
        self._application = app
        self._generateurSemblables = GenerateurSemblables(mode)
        self._semblables = []
        self.LIMITE_NOMBRE_CASES = 3
        self._deuxJoueurs = False
        
    def detruireCases(self):
        raise NotImplementedError("Methode <detruireCases> non implementee !")
    
    def update(self):
        raise NotImplementedError("Methode <update> non implementee !")
    
    def resetSemblables(self):
        self._semblables = []
        
    def semblablesSontDetruits(self):
        for case in self._semblables:
            if not case.estDetruite():
                return False
        return True
        
    def getCouleurSemblables(self):
        if len(self._semblables) > 0:
            return self._semblables[0].getCouleurOriginale()
        return None
    
    def surbrillanceCases(self, event):
        x = int(event.x/self._application.getWidthCase())
        y = int(event.y/self._application.getHeightCase())
        caseActuelle = self._mode.getPartie().getGrille()[y][x]
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
                self._semblables = self._generateurSemblables.generer(caseActuelle, [caseActuelle])
                ''' Si il y en a au moins 3, on gere surbrillance '''
                if len(self._semblables) >= self.LIMITE_NOMBRE_CASES:
                    for case in self._semblables:
                        case.surbrillance()
                        self._mode.getPartie().setScorePotentiel(len(self._semblables))
                self._mode.getPartie().setCasesModifiees(self._semblables)
                self.update()
        else:
            self.desactiverSurbrillance()
            
    def desactiverSurbrillance(self):
        for case in self._semblables:
            if not case.estDetruite():
                case.couleurParDefaut()
        if self._mode.getPartie():
            self._mode.getPartie().setCasesModifiees(self._semblables)
            self._mode.getPartie().setScorePotentiel(0)
            self.update()
            '''re-initialisation de la liste des semblables'''
            self.resetSemblables()
        
    def detruireCasesProvenantAdversaire(self, cases):
        self._semblables = cases
        couleur = self.getCouleurSemblables()
        if not couleur in self._mode.getAdversaire().getCouleurs():
            self._mode.getAdversaire().ajouterCouleur(couleur)
            self._application.ajouterCouleurAdversaire(couleur)
        self._mode.getAdversaire().ajouterScore(len(cases))
        for case in self._semblables:
            case.detruire()
        self.gravite()
        self._application.updateDeuxJoueurs()
            
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
            for i in range(self._mode.getPartie().getTailleGrille() - 1, -1, -1):
                ''' Debut traitement de chaque colonne '''
                case =  self._mode.getPartie().getGrille()[i][col]
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
                nouveauBas = Case(col, self._mode.getPartie().getTailleGrille(), None, None)
            ''' On monte les cases detruites '''
            for i in range(len(casesDetruites)):
                casesDetruites[i].setY(i)
                self._mode.getPartie().getGrille()[casesDetruites[i].getY()][casesDetruites[i].getX()] = casesDetruites[i]
            ''' On descend les cases a descendre '''
            for case in casesADescendre:
                case.setY(nouveauBas.getY() - 1)
                self._mode.getPartie().getGrille()[case.getY()][case.getX()] = case
                nouveauBas = case
            casesAModifier += casesDetruites + casesADescendre
        self._mode.getPartie().setCasesModifiees(casesAModifier)
        self.update()
        self.decalageGauche()
    
    ''' Decalage gauche '''
    def decalageGauche(self):
        while self._mode.getPartie().grillePeutDecalerAGauche():
            case = None
            newCase = None
            oldCase = None
            indiceDecalage = 0
            peutDecaler = False
            casesAModifier = []
            ligneBasGrille = self._mode.getPartie().getGrille()[self._mode.getPartie().getTailleGrille() - 1]            
            for i in range(self._mode.getPartie().getTailleGrille()):
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
                for col in range(case.getX(), self._mode.getPartie().getTailleGrille()):
                    for i in range(self._mode.getPartie().getTailleGrille()):
                        newCase = self._mode.getPartie().getGrille()[i][col]
                        if not newCase.estDetruite():
                            oldCase = self._mode.getPartie().getGrille()[i][col - indiceDecalage]
                            if oldCase not in casesAModifier:
                                casesAModifier.append(oldCase)
                            if newCase not in casesAModifier:
                                casesAModifier.append(newCase)
                            newCase.setX(oldCase.getX())
                            oldCase.setX(col)
                            self._mode.getPartie().getGrille()[i][col - indiceDecalage] = newCase
                            self._mode.getPartie().getGrille()[i][col] = oldCase
            self._mode.getPartie().setCasesModifiees(casesAModifier)
            self.update()