class Joueur():
    def __init__(self, tour):
        self._score = 0
        self._tour = tour
        
    def getScore(self):
        return self._score
    
    def ajouterScore(self, valeur):
        self._score += valeur
        
    def getTour(self):
        return self._tour
    
    def setTour(self, tour):
        self._tour = tour