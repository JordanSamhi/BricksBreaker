import tkinter as tk
from tkinter import messagebox
from vue.PopupNouvellePartie import PopupNouvellePartie
from controleur.Outils import Outils
from controleur.ActionsCases import ActionCases

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Projet Python")
        self.minsize(width=550, height=400)
        self._canvas = None
        self._frame = None
        self._canvasFinPartie = None
        self._partie = None
        self._score, self._scorePotentiel = None, None
        self._outils = Outils(self)
        self._actionCases = ActionCases(self)
        self.genererInterface()

    def genererInterface(self):
        self.genererMenu()
        self.genererCanevas()
        self.genererPanneauDroite()
        
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
        
    def genererCanevas(self):
        self._canvas = tk.Canvas(self, bd=0, highlightthickness=0, relief=tk.GROOVE, width = self.getWidthCanevas(), height = self.getHeightCanevas())
        self._canvas.grid(row=0, column=0)
        
    def genererPanneauDroite(self):
        self._frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, width = self.getWidthFrame(), height = self.getHeightFrame())
        self._frame.grid(row=0, column=1)
        
    def genererScore(self):
        self._score, self._scorePotentiel = tk.IntVar(), tk.IntVar()
        tk.Label(self._frame, text="Score", font='Helvetica 15 bold').pack()
        tk.Label(self._frame, textvariable=self._score, font='Helvetica 15 bold').pack()
        tk.Label(self._frame, text="Score Potentiel", font='Helvetica 15 bold').pack()
        tk.Label(self._frame, textvariable=self._scorePotentiel, font='Helvetica 15 bold').pack()
        
    def affichageNumeroAnonymat(self):
        messagebox.showinfo("Numeros Anonymat", "17820006\n17820034")
        
    def nouvellePartie(self):
        oldPartie = self._partie
        popup = PopupNouvellePartie(self)
        self.wait_window(popup.getToplevel())
        if self._partie and self._partie != oldPartie:
            if self._canvasFinPartie:
                self._canvasFinPartie.destroy()
                self._canvasFinPartie = None
            if self._score:
                self._score.set(0)
                self._scorePotentiel.set(0)
            else:
                self.genererScore()
            self.activerEvenements()
            self.dessiner(self._partie.getGrilleEnListe())
            self.gererFinPartie()
       
    def activerEvenements(self):
        self.bind("<Configure>", self.updateTailleCanvas)
        self._canvas.bind("<Motion>", self.surbrillanceCases)
        self._canvas.bind("<Leave>", self.desactiverSurbrillance)
        self._canvas.bind("<Button-1>", self.detruireCases)
        
    def desactiverEvenements(self):
        self._canvas.unbind("<Button-1>")
        self._canvas.unbind("<Motion>")
        self._canvas.unbind("<Leave>")
        
    def surbrillanceCases(self, event):
        self._actionCases.surbrillanceCases(event)
        
    def desactiverSurbrillance(self, _):
        self._actionCases.desactiverSurbrillance()
            
    def detruireCases(self, _):
        self._actionCases.detruireCases()
        self.gererFinPartie()
    
    def gererFinPartie(self):
        if self._outils.isPartieFinie(self._partie):
            self.afficherMessageFinPartie()
            self.desactiverEvenements()
    
    def afficherMessageFinPartie(self):
        self._canvasFinPartie = tk.Canvas(self._canvas, width=self.getWidthCanevas(), height=self.getHeightCanevas()/4, background="navajo white")
        self._canvasFinPartie.create_text(self._canvasFinPartie.winfo_reqwidth()/2, self._canvasFinPartie.winfo_reqheight()/4, text="Partie terminee !", font="Arial 16 italic", fill="blue")
        self._canvasFinPartie.create_text(self._canvasFinPartie.winfo_reqwidth()/2, self._canvasFinPartie.winfo_reqheight()/2, text="Score : "+str(self._score.get()), font="Arial 16 italic", fill="blue")
        self._canvasFinPartie.pack()
        self._canvasFinPartie.place(x=0, y=(self.getHeightCanevas() - self.getHeightCanevas()/4) / 2)
        
    def dessiner(self, listeCases):
        if listeCases and len(listeCases) > 0:
            self._taille_height, self._taille_width = self._outils.calculerTaillesCases(self.getHeightCanevas(), self.getWidthCanevas(), self._partie.getTailleGrille())
            for case in listeCases:
                self.creerRectangle(case)
            
    def creerRectangle(self, case):
        self._canvas.create_rectangle(case.getX() * self.getWidthCase(), case.getY() * self.getHeightCase(),
             (case.getX()+1) * self.getWidthCase(), (case.getY()+1) * self.getHeightCase(), fill=case.getCouleur())
        
    def updateTailleCanvas(self, _):
        self._canvas.configure(width = self.getWidthCanevas(), height = self.getHeightCanevas())
        self._frame.config(width = self.getWidthFrame(), height = self.getHeightFrame())
        if self._canvasFinPartie:
            self._canvasFinPartie.configure(width=self.getWidthCanevas(), height=self.getHeightCanevas()/4)
            self._canvasFinPartie.place(x=0, y=(self.getHeightCanevas() - self.getHeightCanevas()/4) / 2)
        self.dessiner(self._partie.getGrilleEnListe())
            
    def update(self):
        self.dessiner(self._partie.getCasesModifiees())
        self._score.set(self._partie.getScore())
        self._scorePotentiel.set(self._partie.getScorePotentiel())
        
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
    
    def getHeightCanevas(self):
        return self.getHeight()
    
    ''' 70% de la largeur de la fenetre '''
    def getWidthCanevas(self):
        return self.getWidth() * 0.7
    
    def getHeightFrame(self):
        return self.getHeight()
    
    ''' 30% de la largeur '''
    def getWidthFrame(self):
        return self.getWidth() * 0.3
    
if __name__ == "__main__":
    app = Application()
    app.mainloop()