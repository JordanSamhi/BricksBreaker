from modele.couleurs.ListeCouleurs import ListeCouleurs

class Liste4Couleurs(ListeCouleurs):
    def __init__(self):
        ListeCouleurs.__init__(self)
        
    def getLimiteCouleur(self):
        return 25
     
    def definitionCouleurs(self):    
        return ("red3", "green3", "SkyBlue3", "yellow3")
