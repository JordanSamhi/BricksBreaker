import tkinter as tk
from controleur.AgentReseau import AgentReseau

class PopupReseau():
    def __init__(self, mode):
        self._mode = mode
        self._fenetre = tk.Toplevel()
        self._fenetre.grab_set()
        self._fenetre.resizable(width=False, height=False)
        self._fenetre.title('Connexion')
        self._message = "<adresse IP : port>"
        tk.Label(self._fenetre, text=self._message).pack()
        self._adresse = tk.Text(self._fenetre, height=1, width=30)
        self._adresse.insert(1.0, "127.255.255.255:2010")
        self._adresse.pack()
        tk.Button(self._fenetre, text='Connexion', command=self.connexion).pack()
    
    def connexion(self):
        self._mode.setAgentReseau(AgentReseau(self._mode, self._adresse.get(1.0, tk.END), "AgentReseau"))
        self._fenetre.grab_release()
        self._fenetre.destroy()
    
    def getToplevel(self):
        return self._fenetre