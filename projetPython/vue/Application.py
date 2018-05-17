import tkinter as tk
from tkinter import messagebox
from vue.PopupNouvellePartie import PopupNouvellePartie
from controleur.Outils import Outils
from controleur.ActionsCases import ActionCases
from controleur.AgentReseau import AgentReseau
from vue.PopupAttenteClient import PopupAttenteClient
import time, socket

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Projet Python")
        self.minsize(width=550, height=400)
        self._canvas = None
        self._frame = None
        self._canvasFinPartie = None
        self._partie = None
        self._score, self._scorePotentiel, self._scoreAdversaire = None, None, None
        self._monTour = None
        self._temps = None
        self._delai = 5
        self._outils = Outils(self)
        self._actionCases = ActionCases(self)
        self._agentReseau = None
        self.protocol("WM_DELETE_WINDOW", self.deconnecterAgent)
        self.genererInterface()
        
    def deconnecterAgent(self):
        if self._agentReseau:
            self._agentReseau.stop()
        self.destroy()

    def genererInterface(self):
        self.genererMenu()
        self.genererCanevas()
        self.genererPanneauDroite()
        
    def genererMenu(self):
        barreMenu = tk.Menu(self)
        jeu = tk.Menu(barreMenu,tearoff = 0)
        jeu.add_command(label="Nouvelle partie 1 joueur", command = self.nouvellePartie)
        jeu.add_command(label="Creer serveur 2 joueurs", command = self.attenteSecondJoueur)
        jeu.add_command(label="Connexion a un autre joueur", command = self.connexionAutreJoueur)
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
        
    def genererScoreUnJoueur(self):
        self._score, self._scorePotentiel = tk.IntVar(), tk.IntVar()
        tk.Label(self._frame, text="Score", font='Helvetica 15 bold').pack()
        tk.Label(self._frame, textvariable=self._score, font='Helvetica 15 bold').pack()
        tk.Label(self._frame, text="Score Potentiel", font='Helvetica 15 bold').pack()
        tk.Label(self._frame, textvariable=self._scorePotentiel, font='Helvetica 15 bold').pack()
    
    def genererScoreDeuxJoueur(self):
        self._monTour = tk.StringVar()
        self._temps = tk.IntVar()
        self._temps.set(self._delai)
        self._score, self._scorePotentiel, self._scoreAdversaire = tk.IntVar(), tk.IntVar(), tk.IntVar()
        if self._partie.getMoi().getTour():
            self._monTour.set("Mon tour")
        else:
            self._monTour.set("Pas mon tour")
        tk.Label(self._frame, textvariable=str(self._temps), font='Helvetica 15 bold').pack()
        tk.Label(self._frame, textvariable=self._monTour, font='Helvetica 15 bold').pack()
        tk.Label(self._frame, text="Score Moi", font='Helvetica 15 bold').pack()
        tk.Label(self._frame, textvariable=self._score, font='Helvetica 15 bold').pack()
        tk.Label(self._frame, text="Score Adv.", font='Helvetica 15 bold').pack()
        tk.Label(self._frame, textvariable=self._scoreAdversaire, font='Helvetica 15 bold').pack()
        tk.Label(self._frame, text="Score Potentiel", font='Helvetica 15 bold').pack()
        tk.Label(self._frame, textvariable=self._scorePotentiel, font='Helvetica 15 bold').pack()
        self._casesAMoi = tk.Frame(self._frame)
        self._casesAdversaire = tk.Frame(self._frame)
        tk.Label(self._casesAMoi, text="Mes cases", font='Helvetica 15 bold').pack()
        tk.Label(self._casesAdversaire, text="Cases adv.", font='Helvetica 15 bold').pack()
        self._casesAMoi.pack()
        self._casesAdversaire.pack()
        self.miseAJourTemps()
        
    def miseAJourTemps(self):
        if self._temps.get() > 0:
            if self._partie.getMoi().getTour():
                self._temps.set(self._temps.get() - 1)
                self.after(1000, self.miseAJourTemps)
        else:
            self._agentReseau.changerTour()
        
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
                if self._scoreAdversaire:
                    self._scoreAdversaire.set(0)
            elif self._agentReseau:
                self.genererScoreDeuxJoueur()
            else:
                self.genererScoreUnJoueur()
            self.activerEvenements()
            self.dessiner(self._partie.getGrilleEnListe())
            if self._agentReseau:
                self.gererFinPartieDeuxJoueurs()
            else:
                self.gererFinPartie()
            
    def attenteSecondJoueur(self):
        def attenteJoueur():
            if not self._agentReseau:
                self._popupAttenteClient = PopupAttenteClient()
                self._agentReseau = AgentReseau(self, "AgentReseau")
            if self._agentReseau.echo() != 1:
                if not self._popupAttenteClient.estOuverte():
                    self._agentReseau.stop()
                    self._agentReseau = None
                    return
                self.after(1000, attenteJoueur)
            else:
                ''' joueur connecte '''
                self._popupAttenteClient.fermerFenetre()
                self._actionCases.setPartieDeuxJoueurs()
                self.nouvellePartie()
                self._agentReseau.envoyerGrille(self._partie.getGrilleEnListe())
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind(("0.0.0.0", 2010))
            sock.close()
            ''' Port dispo '''
            attenteJoueur()
        except:
            messagebox.showerror("Erreur", "L'autre joueur attend deja")

    def connexionAutreJoueur(self):
        if not self._agentReseau:
            self._popupAttenteClient = PopupAttenteClient()
            self._agentReseau = AgentReseau(self, "AgentReseau")
        if self._agentReseau.echo() != 1:
            if not self._popupAttenteClient.estOuverte():
                self._agentReseau.stop()
                self._agentReseau = None
                return
            self.after(1000, self.connexionAutreJoueur)
        else:
            self._popupAttenteClient.fermerFenetre()
            while not self._partie:
                time.sleep(1)
            self._actionCases.setPartieDeuxJoueurs()
            self._partie.getMoi().setTour(False)
            self.genererScoreDeuxJoueur()
            self._score.set(0)
            self._scorePotentiel.set(0)
            self._scoreAdversaire.set(0)
            self.activerEvenements()
            self.dessiner(self._partie.getGrilleEnListe())
            self.gererFinPartieDeuxJoueurs()
            
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
        if not self._agentReseau:
            self.gererFinPartie()
    
    def gererFinPartie(self):
        if self._outils.isPartieFinie(self._partie):
            self.afficherMessageFinPartie()
            self.desactiverEvenements()
            self._actionCases.resetSemblables()
            
    def gererFinPartieDeuxJoueurs(self):
        if self._outils.isPartieFinieDeuxJoueurs(self._partie):
            self.afficherMessageFinPartieDeuxJoueurs()
            self.desactiverEvenements()
            self._actionCases.resetSemblables()
            self._agentReseau.envoyerFinPartie()
    
    def afficherMessageFinPartie(self):
        self._canvasFinPartie = tk.Canvas(self._canvas, width=self.getWidthCanevas(), height=self.getHeightCanevas()/4, background="navajo white")
        self._canvasFinPartie.create_text(self._canvasFinPartie.winfo_reqwidth()/2, self._canvasFinPartie.winfo_reqheight()/4, text="Partie terminee !", font="Arial 16 italic", fill="blue")
        self._canvasFinPartie.create_text(self._canvasFinPartie.winfo_reqwidth()/2, self._canvasFinPartie.winfo_reqheight()/2, text="Score : "+str(self._score.get()), font="Arial 16 italic", fill="blue")
        self._canvasFinPartie.pack()
        self._canvasFinPartie.place(x=0, y=(self.getHeightCanevas() - self.getHeightCanevas()/4) / 2)
        
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
        self._score.set(self._partie.getMoi().getScore())
        self._scorePotentiel.set(self._partie.getScorePotentiel())
        if self._scoreAdversaire:
            self._scoreAdversaire.set(self._partie.getAdversaire().getScore())
        
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
    
    def getAgentReseau(self):
        return self._agentReseau
    
    def getActionCases(self):
        return self._actionCases
    
    def getFrame(self):
        return self._frame
    
    def ajouterCouleurUtilisateur(self, couleur):
        tk.Label(self._casesAMoi, text="          ", bg=couleur).pack()
        
    def ajouterCouleurAdversaire(self, couleur):
        tk.Label(self._casesAdversaire, text="          ", bg=couleur).pack()
    
    def setPasMonTour(self):
        self._monTour.set("Pas mon tour")
        
    def setMonTour(self):
        self._monTour.set("Mon tour")
        
    def resetTimer(self):
        self._temps.set(self._delai)
if __name__ == "__main__":
    app = Application()
    app.mainloop()