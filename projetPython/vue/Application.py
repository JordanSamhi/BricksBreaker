import tkinter as tk
from tkinter import messagebox
from vue.PopupNouvellePartie import PopupNouvellePartie
from controleur.Controleur import Controleur

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Projet Python")
        self.geometry("400x400")
        self._canvas = None
        self._canvasFinPartie = None
        self.genererMenu()
        self.genererCanevas()
        self._partie = None
        self._controleur = Controleur(self)
        
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
        if self._canvasFinPartie:
            self._canvasFinPartie.destroy()
        popup = PopupNouvellePartie(self._controleur)
        self.wait_window(popup.getToplevel())
        self.genererEvenements()
        self.dessiner(self._partie.getGrilleEnListe())
        self.gererFinPartie()
       
    def genererEvenements(self):
        self.bind("<Configure>", self.updateTailleCanvas)
        self.bind("<Motion>", self.surbrillanceCases)
        self.bind("<Leave>", self.desactiverSurbrillance)
        self.bind("<Button-1>", self.detruireCases)
        
    def surbrillanceCases(self, event):
        self._controleur.surbrillanceCases(event)
        
    def desactiverSurbrillance(self, _):
        self._controleur.desactiverSurbrillance()
            
    def detruireCases(self, _):
        self._controleur.detruireCases()
        self.gererFinPartie()
    
    def gererFinPartie(self):
        if self._controleur.isPartieFinie():
            self.unbind("<Button-1>")
            self.afficherMessageFinPartie()
    
    def afficherMessageFinPartie(self):
        self._canvasFinPartie = tk.Canvas(self._canvas, width=self.winfo_width(), height=self.winfo_height()/4, background="navajo white")
        self._canvasFinPartie.create_text(75, 60, text="Cible", font="Arial 16 italic", fill="blue")
        self._canvasFinPartie.pack()
        self._canvasFinPartie.place(x=0, y=(self.winfo_height() - self.winfo_height()/4) / 2)
        
    def dessiner(self, listeCases):
        if listeCases:
            self._taille_width, self._taille_height = self._controleur.calculerTaillesCases(self.getWidth(), self.getHeight())
            for case in listeCases:
                self.creerRectangle(case)
            
    def creerRectangle(self, case):
        self._canvas.create_rectangle(case.getX() * self._taille_width, case.getY() * self._taille_height,
             (case.getX()+1) * self._taille_width, (case.getY()+1) * self._taille_height, fill=case.getCouleur())
        
    def updateTailleCanvas(self, _):
        self._canvas.configure(width = self.winfo_width(), height = self.winfo_height())
        if self._canvasFinPartie:
            self._canvasFinPartie.configure(width = self.winfo_width(), height = self.winfo_height() / 4)
            self._canvasFinPartie.place(x=0,y=(self.winfo_height() - self.winfo_height() / 4) / 2)
        self.dessiner(self._partie.getGrilleEnListe())
            
    def update(self):
        self.dessiner(self._partie.getCasesModifiees())
        
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