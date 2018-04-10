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
        self._partie = None
        self._controleur = Controleur(self)
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
        popup = PopupNouvellePartie(self._controleur)
        self.wait_window(popup.getToplevel())
        self.dessiner(self._partie.getGrilleEnListe())
       
    def genererEvenements(self):
        self.bind("<Configure>", self.updateTailleCanvas)
        self.bind("<Motion>", self.surbrillanceCases)
        self.bind("<Leave>", self.desactiverSurbrillance)
        self.bind("<Button-1>", self.detruireCase)
        
    def detruireCase(self, event):
        if self._partie:
            self.dessiner(self._controleur.detruireCase(event))
        
    def surbrillanceCases(self, event):
        if self._partie:
            self.dessiner(self._controleur.surbrillanceCases(event))
        
    def desactiverSurbrillance(self, event):
        if self._partie:
            self.dessiner(self._controleur.desactiverSurbrillance(event))
        
    def dessiner(self, listeCases):
        if listeCases:
            self._taille_width, self._taille_height = self._controleur.calculerTaillesCases(self.getWidth(), self.getHeight())
            for case in listeCases:
                self.creerRectangle(case)
            
    def creerRectangle(self, case):
        self._canvas.create_rectangle(case.getX() * self._taille_width, case.getY() * self._taille_height,
             (case.getX()+1) * self._taille_width, (case.getY()+1) * self._taille_height, fill=case.getCouleur())
        
    def updateTailleCanvas(self, _):
        if self._partie:
            self._canvas.configure(width = self.winfo_width(), height = self.winfo_height())
            self.dessiner(self._partie.getGrilleEnListe())
        
    def getWidth(self):
        return self.winfo_width()
    
    def getHeight(self):
        return self.winfo_height()
    
    def getPartie(self):
        return self._partie
    
    def setPartie(self, partie):
        self._partie = partie
        
    def getWidthCase(self):
        return self._taille_width
    
    def getHeightCase(self):
        return self._taille_height
    
if __name__ == "__main__":
    app = Application()
    app.mainloop()