from modele.Joueur import Joueur
from controleur.generateurs.GenerateurSemblables import GenerateurSemblables

class Mode:
    def __init__(self, app):
        self._application = app
        self._partie = None
        self._actionsCases = None
        self._joueur = Joueur(True)
        self._generateurSemblables = GenerateurSemblables(self)
        self.LIMITE_NOMBRE_CASES = 3
        
    def debut(self):
        raise NotImplementedError("Methode <debut> non implementee !")
    
    def surbrillanceCases(self, _):
        raise NotImplementedError("Methode <surbrillanceCase> non implementee !")
    
    def desactiverSurbrillance(self, _):
        raise NotImplementedError("Methode <desactiverSurbrillance> non implementee !")
    
    def detruireCases(self, _):
        raise NotImplementedError("Methode <detruireCases> non implementee !")
    
    def gererFinPartie(self):
        raise NotImplementedError("Methode <gererFinPartie> non implementee !")
    
    def isPartieFinie(self):
        raise NotImplementedError("Methode <isPartieFinie> non implementee !")
    
    def getPartie(self):
        return self._partie
    
    def setPartie(self, partie):
        self._partie = partie
    
    def getTailleGrille(self):
        return self._partie.getTailleGrille()
    
    def getJoueur(self):
        return self._joueur
    
    def getActionsCases(self):
        return self._actionsCases
    
    def getAgentReseau(self):
        return None
    
    def getApplication(self):
        return self._application