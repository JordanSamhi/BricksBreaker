import tkinter as tk
from tkinter import messagebox
from vue.popups.PopupMode import PopupMode
from vue.popups.PopupChoixTaille import PopupChoixTaille
from vue.popups.PopupReseau import PopupReseau
from vue.popups.PopupAttenteClient import PopupAttenteClient
from vue.popups.PopupDelai import PopupDelai

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Projet Python")
        self.minsize(width=550, height=400)
        self._canvas = None
        self._framePanneauDroite = None
        self._canvasFinPartie = None
        self._mode = None
        self._score, self._scorePotentiel, self._scoreAdversaire = None, None, None
        self._tour, self._temps = None, None
        self.protocol("WM_DELETE_WINDOW", self.quitter)
        self.genererInterface()
        
    def quitter(self):
        if self._mode and self._mode.getAgentReseau() and self._mode.getAgentReseau().isAlive():
            self._mode.getAgentReseau().stop()
        app.destroy()
        
    def genererInterface(self):
        self.genererMenu()
        self.genererCanevas()
        self.genererPanneauDroite()
        
    def genererMenu(self):
        barreMenu = tk.Menu(self)
        jeu = tk.Menu(barreMenu,tearoff = 0)
        jeu.add_command(label="Nouvelle partie", command = self.nouvellePartie)
        jeu.add_command(label="Quitter", command = self.quitter)
        barreMenu.add_cascade(label ="Jeu", menu=jeu)        
        aPropos = tk.Menu(barreMenu, tearoff = 0)
        aPropos.add_command(label="Numeros d'anonymat", command = self.affichageNumeroAnonymat)
        barreMenu.add_cascade(label ="A Propos", menu=aPropos) 
        self.config(menu=barreMenu)
        
    def genererCanevas(self):
        self._canvas = tk.Canvas(self, bd=0, highlightthickness=0, relief=tk.GROOVE, width = self.getWidthCanevas(), height = self.getHeightCanevas())
        self._canvas.grid(row=0, column=0)
        
    def genererPanneauDroite(self):
        self._framePanneauDroite = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, width = self.getWidthFrame(), height = self.getHeightFrame())
        self._framePanneauDroite.grid(row=0, column=1)
        
    def nouvellePartie(self):
        if self._canvasFinPartie:
            self._canvasFinPartie.destroy()
            self._canvasFinPartie = None
        oldMode = self._mode
        self._canvas.delete("all")
        popup = PopupMode(self)
        self.wait_window(popup.getToplevel())
        if self._mode and self._mode != oldMode:
            self._mode.debut()
            self.activerEvenements()
        
    def popUpChoixTaille(self):
        popup = PopupChoixTaille(self._mode)
        self.wait_window(popup.getToplevel())
        
    def popUpReseau(self):
        popup = PopupReseau(self._mode)
        self.wait_window(popup.getToplevel())
        
    def popUpAttenteClient(self):
        return PopupAttenteClient()
    
    def popUpDelai(self):
        popup = PopupDelai(self._mode)
        self.wait_window(popup.getToplevel())
        
    def genererScoreUnJoueur(self):
        for widget in self._framePanneauDroite.winfo_children():
            widget.destroy()
        self._score, self._scorePotentiel = tk.IntVar(), tk.IntVar()
        tk.Label(self._framePanneauDroite, text="Score", font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, textvariable=self._score, font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, text="Score Potentiel", font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, textvariable=self._scorePotentiel, font='Helvetica 15 bold').pack()
    
    def genererScoreDeuxJoueurs(self):
        for widget in self._framePanneauDroite.winfo_children():
            widget.destroy()
        self._tour = tk.StringVar()
        self._temps = tk.IntVar()
        self._temps.set(self._mode.getDelai())
        self._score, self._scorePotentiel, self._scoreAdversaire = tk.IntVar(), tk.IntVar(), tk.IntVar()
        tk.Label(self._framePanneauDroite, textvariable=str(self._temps), font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, textvariable=self._tour, font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, text="Score Moi", font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, textvariable=self._score, font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, text="Score Adv.", font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, textvariable=self._scoreAdversaire, font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, text="Score Potentiel", font='Helvetica 15 bold').pack()
        tk.Label(self._framePanneauDroite, textvariable=self._scorePotentiel, font='Helvetica 15 bold').pack()
        self._casesAMoi = tk.Frame(self._framePanneauDroite)
        self._casesAdversaire = tk.Frame(self._framePanneauDroite)
        tk.Label(self._casesAMoi, text="Mes cases", font='Helvetica 15 bold').pack()
        tk.Label(self._casesAdversaire, text="Cases adv.", font='Helvetica 15 bold').pack()
        self._casesAMoi.pack()
        self._casesAdversaire.pack()
        self.miseAJourTemps()
        
    def miseAJourTemps(self):
        if self._temps.get() > 0:
            if self._mode.getJoueur().getTour():
                self._temps.set(self._temps.get() - 1)
                self.after(1000, self.miseAJourTemps)
        else:
            self._mode.changerTour()
        
    def affichageNumeroAnonymat(self):
        messagebox.showinfo("Numeros Anonymat", "17820006\n17820034")
        
    def activerEvenements(self):
        self.bind("<Configure>", self.updateTailleCanvas)
        self._canvas.bind("<Motion>", self._mode.surbrillanceCases)
        self._canvas.bind("<Leave>", self._mode.desactiverSurbrillance)
        self._canvas.bind("<Button-1>", self._mode.detruireCases)
        
    def desactiverEvenements(self):
        self._canvas.unbind("<Button-1>")
        self._canvas.unbind("<Motion>")
        self._canvas.unbind("<Leave>")
        
    def afficherMessageFinPartie(self):
        self._canvasFinPartie = tk.Canvas(self._canvas, width=self.getWidthCanevas(), height=self.getHeightCanevas()/4, background="navajo white")
        self._canvasFinPartie.create_text(self._canvasFinPartie.winfo_reqwidth()/2, self._canvasFinPartie.winfo_reqheight()/4, text="Partie terminee !", font="Arial 16 italic", fill="blue")
        self._canvasFinPartie.create_text(self._canvasFinPartie.winfo_reqwidth()/2, self._canvasFinPartie.winfo_reqheight()/2, text="Score : "+str(self._score.get()), font="Arial 16 italic", fill="blue")
        self._canvasFinPartie.pack()
        self._canvasFinPartie.place(x=0, y=(self.getHeightCanevas() - self.getHeightCanevas()/4) / 2)
#         
    def afficherMessageFinPartieDeuxJoueurs(self):
        self._canvasFinPartie = tk.Canvas(self._canvas, width=self.getWidthCanevas(), height=self.getHeightCanevas()/4, background="navajo white")
        self._canvasFinPartie.create_text(self._canvasFinPartie.winfo_reqwidth()/2, self._canvasFinPartie.winfo_reqheight()/5, text="Partie terminee !", font="Arial 16 italic", fill="blue")
        if self._score.get() > self._scoreAdversaire.get():
            text = "Vous avez gagne !"
            score = self._score.get()
        elif self._score.get() < self._scoreAdversaire.get():
            text = "Vous avez perdu !"
            score = self._scoreAdversaire.get()
        else:
            text = "Egalite !"
            score = self._score.get()
        self._canvasFinPartie.create_text(self._canvasFinPartie.winfo_reqwidth()/2, self._canvasFinPartie.winfo_reqheight()/2, text=text, font="Arial 16 italic", fill="blue")
        self._canvasFinPartie.create_text(self._canvasFinPartie.winfo_reqwidth()/2, self._canvasFinPartie.winfo_reqheight()/1.2, text="Score : "+str(score), font="Arial 16 italic", fill="blue")
        self._canvasFinPartie.pack()
        self._canvasFinPartie.place(x=0, y=(self.getHeightCanevas() - self.getHeightCanevas()/4) / 2)
        
    def dessiner(self, listeCases):
        if listeCases and len(listeCases) > 0:
            self._heightCases, self._widthCases = self.getHeightCanevas() / self._mode.getTailleGrille(), self.getWidthCanevas() / self._mode.getTailleGrille()
            for case in listeCases:
                self.creerRectangle(case)
            
    def creerRectangle(self, case):
        self._canvas.create_rectangle(case.getX() * self.getWidthCase(), case.getY() * self.getHeightCase(), (case.getX()+1) * self.getWidthCase(),
                                      (case.getY()+1) * self.getHeightCase(), fill=case.getCouleur())
        
    def updateTailleCanvas(self, _):
        self._canvas.configure(width = self.getWidthCanevas(), height = self.getHeightCanevas())
        self._framePanneauDroite.config(width = self.getWidthFrame(), height = self.getHeightFrame())
        if self._canvasFinPartie:
            self._canvasFinPartie.configure(width=self.getWidthCanevas(), height=self.getHeightCanevas()/4)
            self._canvasFinPartie.place(x=0, y=(self.getHeightCanevas() - self.getHeightCanevas()/4) / 2)
        if self._mode.getPartie():
            self.dessiner(self._mode.getPartie().getGrilleEnListe())
            
    def update(self):
        self.dessiner(self._mode.getPartie().getCasesModifiees())
        self._score.set(self._mode.getJoueur().getScore())
        self._scorePotentiel.set(self._mode.getPartie().getScorePotentiel())
            
    def updateDeuxJoueurs(self):
        self.update()
        self._scoreAdversaire.set(self._mode.getAdversaire().getScore())
        if self._mode.getJoueur().getTour():
            self._tour.set("Mon tour")
        else:
            self._tour.set("Pas mon tour")
        
    def setMode(self, mode):
        self._mode = mode    
        
    def getWidthCase(self):
        return self._widthCases
    
    def getHeightCase(self):
        return self._heightCases
        
    def getHeightCanevas(self):
        return self.winfo_height()
    
    ''' 70% de la largeur de la fenetre '''
    def getWidthCanevas(self):
        return self.winfo_width() * 0.7
    
    def getHeightFrame(self):
        return self.winfo_height()
    
    ''' 30% de la largeur '''
    def getWidthFrame(self):
        return self.winfo_width() * 0.3
    
    def ajouterCouleurUtilisateur(self, couleur):
        tk.Label(self._casesAMoi, text="          ", bg=couleur).pack()
         
    def ajouterCouleurAdversaire(self, couleur):
        tk.Label(self._casesAdversaire, text="          ", bg=couleur).pack()
#     
    def resetTimer(self):
        self._temps.set(self._mode.getDelai())
        
if __name__ == "__main__":
    app = Application()
    app.mainloop()