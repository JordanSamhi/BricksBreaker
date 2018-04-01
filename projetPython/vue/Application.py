import tkinter as tk
from tkinter import messagebox
from vue.PopupNouvellePartie import PopupNouvellePartie
from controleur.Controleur import Controleur

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Projet Python")
        self.geometry("400x400")
        self.genererMenu()
        self.genererCanevas()
        self._grille = []
        self._tailleGrille = 1
        self._semblables = []
        self._controleur = Controleur()
        self.genererEvenements()
        
    def genererCanevas(self):
        self.update_idletasks()
        self._canvas = tk.Canvas(self, width = self.getWidth(), height = self.getHeight(), bd=0, highlightthickness=0)
        self._canvas.pack()
        
    def genererMenu(self):
        barreMenu = tk.Menu(self)
        
        jeu = tk.Menu(barreMenu,tearoff = 0)
        jeu.add_command(label="Nouveau", command = self.nouvellePartie)
        jeu.add_command(label="Quitter", command = self.destroy)
        barreMenu.add_cascade(label ="Jeu", menu=jeu)
        
        aPropos = tk.Menu(barreMenu, tearoff = 0)
        aPropos.add_command(label="Numeros d'anonymat", command = self.affichageNumeroAnonymat)
        barreMenu.add_cascade(label ="A Propos", menu=aPropos)
            
        self.config(menu=barreMenu)
        
    def affichageNumeroAnonymat(self):
        messagebox.showinfo("Numeros Anonymat", "17820006\n17820034")
        
    def nouvellePartie(self):
        popup = PopupNouvellePartie(self)
        self.wait_window(popup.getToplevel())
        grilleEnListe = self._controleur.transformerGrilleEnListe(self._grille)
        self.dessiner(grilleEnListe)
       
    def genererPartie10x10(self):
        self._grille = self._controleur.genererGrille10x10()
        self._tailleGrille = 10
        
    def genererPartie20x20(self):
        self._grille = self._controleur.genererGrille20x20()
        self._tailleGrille = 20
        
    def genererEvenements(self):
        self.bind("<Configure>", self.updateTailleCanvas)
        self.bind("<Motion>", self.surbrillanceCases)
        self.bind("<Leave>", self.desactiverSurbrillance)
        
    def surbrillanceCases(self, event):
        if self._grille:
            x = int(event.x/self._taille_width)
            y = int(event.y/self._taille_height)
            caseActuelle = self._grille[y][x]
            casesARedessiner = self._controleur.gererSurbrillance(caseActuelle)
            if casesARedessiner:
                self.dessiner(casesARedessiner)
                
    def desactiverSurbrillance(self, _):
        casesARedessiner = self._controleur.couleurParDefautSemblables()
        if casesARedessiner:
                self.dessiner(casesARedessiner)
        
    def dessiner(self, listeCases):
        self.calculerTailles()
        for case in listeCases:
            self.creerRectangle(case)
            
    def calculerTailles(self):
        self._taille_width, self._taille_height = self.getWidth() / self._tailleGrille, self.getHeight() / self._tailleGrille
        
    def creerRectangle(self, case):
        self._canvas.create_rectangle(case.getX() * self._taille_width, case.getY() * self._taille_height,
             (case.getX()+1) * self._taille_width, (case.getY()+1) * self._taille_height, fill=case.getCouleur())
        
        
    def updateTailleCanvas(self, _):
        self._canvas.configure(width = self.winfo_width(), height = self.winfo_height())
        grilleEnListe = self._controleur.transformerGrilleEnListe(self._grille)
        self.dessiner(grilleEnListe)
        
    def getWidth(self):
        return self.winfo_width()
    
    def getHeight(self):
        return self.winfo_height()
  

if __name__ == "__main__":
    app = Application()
    app.mainloop()