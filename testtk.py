import tkinter as tk
from schedule_week_yk import Schedule_week

class RoseLabMenu:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Menu d'accueil - RoseLab")

        # Création des widgets
        self.titre_label = tk.Label(self.fenetre, text="Bienvenue au RoseLab", font=("Arial", 18, "bold"))
        self.titre_label.pack(pady=20)

        self.bouton_Planning_machine = tk.Button(self.fenetre, text="Planning Machine", command=self.planning_machine)
        self.bouton_Planning_machine.pack(pady=10)

        self.bouton_ouvrir_projet = tk.Button(self.fenetre, text="Ouvrir Projet", command=self.ouvrir_projet)
        self.bouton_ouvrir_projet.pack(pady=10)

        self.bouton_quitter = tk.Button(self.fenetre, text="Quitter", command=self.fenetre.quit)
        self.bouton_quitter.pack(pady=10)

        self.filtre1_var = tk.BooleanVar()
        self.filtre9_var = tk.BooleanVar()
        self.filtre18_var = tk.BooleanVar()
        self.filtre26_var = tk.BooleanVar()
        self.filtre27_var = tk.BooleanVar()

        # Création des boutons avec les cases à cocher
        self.bouton_filtre1 = tk.Checkbutton(self.fenetre, text="Laser", variable=self.filtre1_var)
        self.bouton_filtre1.pack(side="left", padx=10, pady=10)
        
        self.bouton_filtre9 = tk.Checkbutton(self.fenetre, text="Brodeuse", variable=self.filtre9_var)
        self.bouton_filtre9.pack(side="left", padx=10, pady=10)

        self.bouton_filtre18 = tk.Checkbutton(self.fenetre, text="Fraiseuse", variable=self.filtre18_var)
        self.bouton_filtre18.pack(side="left", padx=10, pady=10)

        self.bouton_filtre26 = tk.Checkbutton(self.fenetre, text="Laser de marquage", variable=self.filtre26_var)
        self.bouton_filtre26.pack(side="left", padx=10, pady=10)

        self.bouton_filtre27 = tk.Checkbutton(self.fenetre, text="Maker Pro", variable=self.filtre27_var)
        self.bouton_filtre27.pack(side="left", padx=10, pady=10)

    def planning_machine(self):
        filtre=[]
        self.filtre1_var = self.filtre1_var.get()
        self.filtre9_var = self.filtre9_var.get()
        self.filtre18_var = self.filtre18_var.get()
        self.filtre26_var = self.filtre26_var.get()
        self.filtre27_var = self.filtre27_var.get()
        if (self.filtre1_var==True) :
            filtre.append(1)
        if (self.filtre9_var==True) :
            filtre.append(9)
        if (self.filtre18_var==True) :
            filtre.append(18)
        if (self.filtre26_var==True) :
            filtre.append(26)
        if (self.filtre27_var==True) :
            filtre.append(27)
        token = 'oPec4DpLw9mdFkqr3erCYwig'
        print(filtre)
        #filtre=[1,9,18,26,27]
        start="2024-04-13T00:00:00+02:00"
        end="2024-04-13T22:00:00+02:00"
        fenetre=tk.Tk()
        instance = Schedule_week(token,filtre,start,end,fenetre)
        instance.week()
        fenetre.mainloop()

    def ouvrir_projet(self):
        # Mettre ici le code pour ouvrir un projet existant
        print("Ouverture d'un projet existant")

if __name__ == "__main__":
    fenetre = tk.Tk()
    app = RoseLabMenu(fenetre)
    fenetre.mainloop()
