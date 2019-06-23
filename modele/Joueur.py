class Joueur():
    def __init__(self, tour):
        self._score = 0
        self._tour = tour
        self.listeCouleurs = []
        
    def getScore(self):
        return self._score
    
    def ajouterScore(self, valeur):
        self._score += valeur
        
    def getTour(self):
        return self._tour
    
    def setTour(self, tour):
        self._tour = tour
        
    def getCouleurs(self):
        return self.listeCouleurs
    
    def ajouterCouleur(self, couleur):
        self.listeCouleurs.append(couleur)
        
    def getNombreCouleurs(self):
        return len(self.listeCouleurs)