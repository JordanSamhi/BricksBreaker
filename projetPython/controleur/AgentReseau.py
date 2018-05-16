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
        self.bind_msg(self.gererEcho, 'echo')

    def envoyerGrille(self, grilleEnListe):
        msg = "grille="
        for case in grilleEnListe:
            msg += "("+str(case.getX())+","+str(case.getY())+","+str(case.getCouleur())+");"
        msg = msg[:-1]
        self.send_msg(msg)
        
    def receptionGrille(self, _, grilleEnListe):
        cases = grilleEnListe.split(";")
        tailleGrille = int(sqrt(len(cases)))
        grille = [[None for _ in range(tailleGrille)] for _ in range(tailleGrille)]
        for case in cases:
            caseData = case[1:-1].split(",")
            x = int(caseData[0])
            y = int(caseData[1])
            couleur = caseData[2]
            grille[y][x] = Case(x, y, couleur, grille)
        self._application.setPartie(Partie(grille))
    def echo(self):
        return self.send_msg("echo")
    
    def gererEcho(self, _):
        pass
