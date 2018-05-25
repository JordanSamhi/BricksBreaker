from controleur.actionsCases.ActionsCases import ActionCases

class ActionsCasesDeuxJoueurs(ActionCases):
    def __init__(self, mode, app):
        ActionCases.__init__(self, mode, app)
        
    def detruireCases(self):
        couleur = self.getCouleurSemblables()
        if self._mode.getJoueur().getTour():
            if len(self._semblables) >= self.LIMITE_NOMBRE_CASES and not self.semblablesSontDetruits():
                ''' Gestion appropriation couleurs '''
                if (couleur not in self._mode.getAdversaire().getCouleurs() 
                    and couleur not in self._mode.getJoueur().getCouleurs()
                    and self._mode.getJoueur().getNombreCouleurs() < self._mode.getPartie().getNombreCouleurs() / 2):
                    self._mode.getJoueur().ajouterCouleur(couleur)
                    self._application.ajouterCouleurUtilisateur(couleur)
                if couleur in self._mode.getJoueur().getCouleurs():
                    for case in self._semblables:
                        case.detruire()
                    self._mode.getJoueur().setTour(False)
                    self._application.updateTour()
                    self._mode.getAgentReseau().envoyerCasesADetruire(self._semblables)
                    self._mode.getJoueur().ajouterScore(len(self._semblables))
                    self.gravite()
                    
    def update(self):
        self._application.updateDeuxJoueurs()