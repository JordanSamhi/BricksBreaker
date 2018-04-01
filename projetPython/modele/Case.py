'''
    Une case est definie par sa couleur,
    ses coordonnees et un acces a la grille
    pour recuperer ses voisins
'''
class Case():
    def __init__(self, x, y, couleur, grille):
        self._x = x
        self._y = y
        self._couleur = couleur
        self._grille = grille
        
    def getCouleur(self):
        return self._couleur
    
    def getX(self):
        return self._x
    
    def getY(self):
        return self._y
    
    def getNord(self):
        if self.getY() > 0:
            return self._grille[self._y-1][self._x]
        return None
        
    def getSud(self):
        if self.getY() < len(self._grille) - 1:
            return self._grille[self._y+1][self._x]
        return None
        
    def getEst(self):
        if self.getX() < len(self._grille) - 1:
            return self._grille[self._y][self._x+1]
        return None
        
    def getOuest(self):
        if self.getX() > 0:
            return self._grille[self._y][self._x-1]
        return None
        
    def getVoisins(self):
        voisins = []
        voisins.append(self.getNord())
        voisins.append(self.getSud())
        voisins.append(self.getEst())
        voisins.append(self.getOuest())
        return voisins
    
    def surbrillance(self):
        self._couleur = self._couleur[:-1] + "2"
    
    def couleurParDefaut(self):
        self._couleur = self._couleur[:-1] + "3" 