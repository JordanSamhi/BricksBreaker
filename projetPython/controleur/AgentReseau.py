from ivy.ivy import IvyServer
from math import sqrt
from modele.Case import Case
from modele.Partie import Partie

class AgentReseau(IvyServer):
    def __init__(self, mode, adresse, nom):
        self._mode = mode
        IvyServer.__init__(self, nom)
        self.name = "Agent Reseau"
        self.start(adresse)
        self.bind_msg(self.receptionGrille, '^grille=(.*)')
        self.bind_msg(self.receptionCasesADetruire, '^cases=(.*)')
        self.bind_msg(self.receptionDelai, '^delai=(.*)')
        self.bind_msg(self.gererEcho, 'echo')
        self.bind_msg(self.receptionChangementTour, 'changementTour')
        self.bind_msg(self.receptionFinPartie, 'finPartie')
        
    def envoyerDelai(self, delai):
        msg = "delai="+str(delai)
        self.send_msg(msg)
        
    def receptionDelai(self, _, delai):
        self._mode.setDelai(int(delai))
    
    def changerTour(self):
        msg = "changementTour"
        self._mode.getJoueur().setTour(False)
        self._mode.getApplication().updateTour()
        self.send_msg(msg)
        
    def receptionChangementTour(self, _):
        self._mode.getJoueur().setTour(True)
        self._mode.getApplication().resetTimer()
        self._mode.getApplication().miseAJourTemps()
        self._mode.getApplication().updateTour()
    
    def envoyerFinPartie(self):
        msg = "finPartie"
        self.send_msg(msg)
        
    def receptionFinPartie(self, _):
        self._mode.getApplication().afficherMessageFinPartieDeuxJoueurs()
        self._mode.getApplication().desactiverEvenements()
        self._mode.getActionsCases().resetSemblables()
        
    def envoyerGrille(self, grilleEnListe):
        msg = "grille="
        for case in grilleEnListe:
            msg += str(case.getX())+","+str(case.getY())+","+str(case.getCouleur())+";"
        msg = msg[:-1]
        self.send_msg(msg)
        
    def receptionGrille(self, _, grilleEnListe):
        cases = grilleEnListe.split(";")
        tailleGrille = int(sqrt(len(cases)))
        grille = [[None for _ in range(tailleGrille)] for _ in range(tailleGrille)]
        for case in cases:
            caseData = case.split(",")
            x = int(caseData[0])
            y = int(caseData[1])
            couleur = caseData[2]
            grille[y][x] = Case(x, y, couleur, grille)
        self._mode.setPartie(Partie(grille))
        
    def envoyerCasesADetruire(self, cases):
        msg = "cases="
        for case in cases:
            msg += str(case.getX())+","+str(case.getY())+";"
        msg = msg[:-1]
        self.send_msg(msg)
        
    def receptionCasesADetruire(self, _, casesADetruire):
        cases = []
        for case in casesADetruire.split(";"):
            y = int(case.split(",")[1])
            x = int(case.split(",")[0])
            cases.append(self._mode.getPartie().getGrille()[y][x])
        self._mode.getJoueur().setTour(True)
        self._mode.getApplication().updateTour()
        self._mode.getActionsCases().detruireCasesProvenantAdversaire(cases)
        self._mode.getApplication().resetTimer()
        self._mode.getApplication().miseAJourTemps()
        self._mode.gererFinPartie()
        
    def echo(self):
        return self.send_msg("echo")
    
    def gererEcho(self, _):
        pass
