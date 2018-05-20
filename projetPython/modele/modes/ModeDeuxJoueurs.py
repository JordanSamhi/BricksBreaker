from modele.modes.Mode import Mode
from modele.Joueur import Joueur
from controleur.actionsCases.ActionsCasesDeuxJoueurs import ActionsCasesDeuxJoueurs
import threading, time

class ModeDeuxJoueurs(Mode):
    def __init__(self, app):
        Mode.__init__(self, app)
        self._adversaire= Joueur(False)
        self._agentReseau = None
        self._actionsCases = ActionsCasesDeuxJoueurs(self, self._application)
        self._delai = None
        
    def debut(self):
        self._application.popUpReseau()
        if self._agentReseau:
            popup = self._application.popUpAttenteClient()
            self.attendreClient(popup)

    def attendreClient(self, popup):
        ''' Compteur pour detecter le client du serveur '''
        compteur = 0
        def attenteClient(popup, compteur):
            if self._agentReseau.echo() != 1:
                compteur += 1
                if not popup.estOuverte():
                    self._application.desactiverEvenements()
                    self._agentReseau.stop()
                    return
                threading.Timer(0.2, lambda:attenteClient(popup, compteur)).start()
            else:
                ''' Connexion OK '''
                popup.fermerFenetre()
                if compteur > 1:
                    ''' serveur '''
                    self._application.popUpDelai()
                    self._agentReseau.envoyerDelai(self._delai)
                    self._application.popUpChoixTaille()
                    if self._partie:
                        self._agentReseau.envoyerGrille(self._partie.getGrilleEnListe())
                        self._application.genererScoreDeuxJoueurs()
                        self._application.dessiner(self._partie.getGrilleEnListe())
                        self._application.updateDeuxJoueurs()
                        self._application.activerEvenements()
                        self.gererFinPartie()
                else:
                    ''' client '''
                    self._joueur.setTour(False)
                    secondes = 0
                    ''' attente pour reprendre partie '''
                    while not self._partie:
                        if secondes == 10:
                            break
                        time.sleep(1)
                        secondes += 1
                    if self._partie:
                        self._application.genererScoreDeuxJoueurs()
                        self._application.dessiner(self._partie.getGrilleEnListe())
                        self._application.updateDeuxJoueurs()
        attenteClient(popup, compteur)

    def surbrillanceCases(self, event):
        if self.getJoueur().getTour():
            self._actionsCases.surbrillanceCases(event)
        
    def desactiverSurbrillance(self, _):
        if self.getJoueur().getTour():
            self._actionsCases.desactiverSurbrillance()
        
    def detruireCases(self, _):
        self._actionsCases.detruireCases()
        
    def gererFinPartie(self):
        if self.isPartieFinie():
            self._application.afficherMessageFinPartieDeuxJoueurs()
            self._application.desactiverEvenements()
            self._actionsCases.resetSemblables()
            self._agentReseau.envoyerFinPartie()
            
    def isPartieFinie(self):
        for case in self._partie.getGrilleEnListe():
            if not case.estDetruite():
                if ((self.getJoueur().getNombreCouleurs() < self._partie.getNombreCouleurs() / 2 
                    and (case.getCouleurOriginale() in self.getJoueur().getCouleurs() 
                    or case.getCouleurOriginale() not in self.getAdversaire().getCouleurs()))
                    or 
                    (self.getJoueur().getNombreCouleurs() == self._partie.getNombreCouleurs() / 2
                    and case.getCouleurOriginale() in self.getJoueur().getCouleurs())):
                    semblables = self._generateurSemblables.generer(case, [case])
                    if len(semblables) >= self.LIMITE_NOMBRE_CASES:
                        return False
        return True
    
    def changerTour(self):
        self._agentReseau.changerTour()

    def getAdversaire(self):
        return self._adversaire
    
    def setAgentReseau(self, agent):
        self._agentReseau = agent
        
    def getAgentReseau(self):
        return self._agentReseau
    
    def setDelai(self, delai):
        self._delai = delai
    
    def getDelai(self):
        return self._delai
