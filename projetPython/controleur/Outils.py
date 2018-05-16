from controleur.generateurs.GenerateurSemblables import GenerateurSemblables

class Outils():
    def __init__(self, app):
        self.LIMITE_NOMBRE_CASES = 3
        self.generateurSemblables = GenerateurSemblables(app)
    
    def calculerTaillesCases(self, height, width, tailleGrille):
        return (height / tailleGrille),(width / tailleGrille)
    
    def isPartieFinie(self, partie):
        for case in partie.getGrilleEnListe():
            if not case.estDetruite():
                semblables = self.generateurSemblables.generer(case, [case])
                if len(semblables) >= self.LIMITE_NOMBRE_CASES:
                    return False
        return True
    
    def semblablesSontDetruits(self, semblables):
        for case in semblables:
            if not case.estDetruite():
                return False
        return True