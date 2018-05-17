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
    
    def isPartieFinieDeuxJoueurs(self, partie):
        for case in partie.getGrilleEnListe():
            if not case.estDetruite():
                if ((partie.getMoi().getNombreCouleurs() < partie.getNombreCouleurs() / 2 
                    and (case.getCouleurOriginale() in partie.getMoi().getCouleurs() 
                    or case.getCouleurOriginale() not in partie.getAdversaire().getCouleurs()))
                    or 
                    (partie.getMoi().getNombreCouleurs() == partie.getNombreCouleurs() / 2
                    and case.getCouleurOriginale() in partie.getMoi().getCouleurs())):
                    semblables = self.generateurSemblables.generer(case, [case])
                    if len(semblables) >= self.LIMITE_NOMBRE_CASES:
                        return False
        return True
    
    def semblablesSontDetruits(self, semblables):
        for case in semblables:
            if not case.estDetruite():
                return False
        return True