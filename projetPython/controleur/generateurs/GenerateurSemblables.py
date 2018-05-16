from controleur.generateurs.Generateur import Generateur

class GenerateurSemblables(Generateur):
    def __init__(self, app):
        Generateur.__init__(self, app)
        
    def generer(self, *args):
        case, voisinsVisites = args[0], args[1]
        voisins = [v for v in case.getVoisins() if v is not None and v not in voisinsVisites and v.getCouleur() == case.getCouleur()]
        voisinsVisites = voisinsVisites + voisins
        for v in voisins:
            if v != case:
                voisinsVisites = self.generer(v, voisinsVisites)
        return voisinsVisites