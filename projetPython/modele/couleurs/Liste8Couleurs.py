from modele.couleurs.ListeCouleurs import ListeCouleurs

class Liste8Couleurs(ListeCouleurs):
    def __init__(self):
        ListeCouleurs.__init__(self)
        
    def getLimiteCouleur(self):
        return 50
     
    def definitionCouleurs(self):    
        return ("red3", "green3", "SkyBlue3", "yellow3", "chocolate3", "ivory3", "purple3", "turquoise3")
