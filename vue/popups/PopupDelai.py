import tkinter as tk

class PopupDelai():
    def __init__(self, mode):
        self._mode = mode
        self._fenetre = tk.Toplevel()
        self._fenetre.grab_set()
        self._fenetre.resizable(width=False, height=False)
        self._fenetre.title('Choix delai')
        self._message = "Choisissez le delai"
        tk.Label(self._fenetre, text=self._message).pack()
        self._delai = tk.Spinbox(self._fenetre, from_=10, to=30, state="readonly")
        self._delai.pack()
        tk.Button(self._fenetre, text='Valider', command=self.valider).pack()
    
    def valider(self):
        self._mode.setDelai(int(self._delai.get()))
        self._fenetre.grab_release()
        self._fenetre.destroy()
    
    def getToplevel(self):
        return self._fenetre