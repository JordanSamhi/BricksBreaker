from ivy.ivy import IvyServer
from math import sqrt
from modele.Case import Case
from modele.Partie import Partie

class AgentReseau(IvyServer):
    def __init__(self, app, nomAgent):
        self._application = app
        IvyServer.__init__(self, nomAgent)
        self.name = "Agent Reseau"
        self.start('127.255.255.255:2010')
        self.bind_msg(self.receptionGrille, '^grille=(.*)')
        self.bind_msg(self.receptionCasesADetruire, '^cases=(.*)')
        self.bind_msg(self.gererEcho, 'echo')
        self.bind_msg(self.receptionChangementTour, 'changementTour')
        self.bind_msg(self.receptionFinPartie, 'finPartie')
        
    def changerTour(self):
        msg = "changementTour"
        self._application.getPartie().getMoi().setTour(False)
        self._application.setPasMonTour()
        self.send_msg(msg)    
        
    def receptionChangementTour(self, _):
        self._application.getPartie().getMoi().setTour(True)
        self._application.resetTimer()
        self._application.setMonTour()
        self._application.miseAJourTemps()
    
    def envoyerFinPartie(self):
        msg = "finPartie"
        self.send_msg(msg)
        
    def receptionFinPartie(self, _):
        self._application.afficherMessageFinPartieDeuxJoueurs()
        
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
        self._application.setPartie(Partie(grille))
        
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
            cases.append(self._application.getPartie().getGrille()[y][x])
        self._application.getPartie().getMoi().setTour(True)
        self._application.getActionCases().detruireCasesProvenantAdversaire(cases)
        self._application.setMonTour()
        self._application.gererFinPartieDeuxJoueurs()
        
    def echo(self):
        return self.send_msg("echo")
    
    def gererEcho(self, _):
        pass
