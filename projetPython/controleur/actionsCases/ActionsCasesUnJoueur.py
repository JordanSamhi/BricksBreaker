from controleur.actionsCases.ActionsCases import ActionCases

class ActionsCasesUnJoueur(ActionCases):
    def __init__(self, mode, app):
        ActionCases.__init__(self, mode, app)
    
    def detruireCases(self):
        if len(self._semblables) >= self.LIMITE_NOMBRE_CASES and not self.semblablesSontDetruits():
            for case in self._semblables:
                case.detruire()
            self._mode.getJoueur().ajouterScore(len(self._semblables))
            self.gravite()
            
    def update(self):
        self._application.update()