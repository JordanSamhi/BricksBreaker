from modele.modes.Mode import Mode
from controleur.actionsCases.ActionsCasesUnJoueur import ActionsCasesUnJoueur

class ModeUnJoueur(Mode):
    def __init__(self, app):
        Mode.__init__(self, app)
        self._actionsCases = ActionsCasesUnJoueur(self, self._application)
        
    def debut(self):
        self._application.popUpChoixTaille()
        if self._partie:
            self._application.genererScoreUnJoueur()
            self._application.initialiserGrille(self._partie.getGrilleEnListe())
            self.gererFinPartie()
        
    def surbrillanceCases(self, event):
        self._actionsCases.surbrillanceCases(event)
        
    def desactiverSurbrillance(self, _):
        self._actionsCases.desactiverSurbrillance()
        
    def detruireCases(self, _):
        self._actionsCases.detruireCases()
        self.gererFinPartie()
        
    def gererFinPartie(self):
        if self.isPartieFinie():
            self._application.afficherMessageFinPartie()
            self._application.desactiverEvenements()
            self._actionsCases.resetSemblables()
            
    def isPartieFinie(self):
        for case in self._partie.getGrilleEnListe():
            if not case.estDetruite():
                semblables = self._generateurSemblables.generer(case, [case])
                if len(semblables) >= self.LIMITE_NOMBRE_CASES:
                    return False
        return True
    
