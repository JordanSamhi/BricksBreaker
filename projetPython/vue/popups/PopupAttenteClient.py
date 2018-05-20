import tkinter as tk

class PopupAttenteClient():
    def __init__(self):
        self._fenetre = tk.Toplevel()
        self._fenetre.grab_set()
        self._fenetre.resizable(width=False, height=False)
        self._fenetre.title('Attente client')
        self._message = "Attente d'un second joueur"
        tk.Label(self._fenetre, text=self._message).pack()
        self._fenetre.protocol("WM_DELETE_WINDOW", self.disableFermeture)
        tk.Button(self._fenetre, text='Quitter', command=self.fermerFenetre).pack()
    
    def getToplevel(self):
        return self._fenetre
    
    def disableFermeture(self):
        pass
    
    def fermerFenetre(self):
        if self._fenetre:
            self._fenetre.grab_release()
            self._fenetre.destroy()
            self._fenetre = None
        
    def estOuverte(self):
        if self._fenetre:
            return True
        return False