from availabilities import Available
from id_machines import MachineAPI
from datetime import datetime
import tkinter as tk
import random

class Schedule_week:
    def __init__(self,token,filtre,start,end,fenetre):
        self.token = token
        self.filtre=filtre
        self.start=start 
        self.end=end
        self.fenetre = fenetre
        self.fenetre.title("Réservations du jour")
        self.horaires = [
            "09:00 - 10:00",
            "10:00 - 11:00",
            "11:00 - 12:00",
            "12:00 - 13:00",
            "13:00 - 14:00",
            "14:00 - 15:00",
            "15:00 - 16:00",
            "16:00 - 17:00",
            "17:00 - 18:00",
            "18:00 - 19:00",
            "19:00 - 20:00",
            "20:00 - 21:00"
        ]
        self.couleurs = [
    "#FF5733",  # Rouge
    "#33FF57",  # Vert
    "#3366FF",  # Bleu
    "#FF33FF",  # Magenta
    "#FFFF33",  # Jaune
    "#33FFFF",  # Cyan
    "#FF6F33",  # Orange
    "#6FFF33",  # Lime
    "#336FFF",  # Azur
    "#FF336F",  # Rose
    "#6F33FF",  # Violet
    "#33FF57"   # vert
        ]




    def week (self):
        label_horaire = tk.Label(self.fenetre, text="Horaire", padx=10, pady=5, borderwidth=1, relief="solid", font=("Arial", 10, "bold"))
        label_horaire.grid(row=0, column=0, sticky="nsew")
        column_index=1
        row_index=1
        for i in range (len(self.horaires)) :
            label_horaire = tk.Label(self.fenetre, text=self.horaires[i], padx=10, pady=5, borderwidth=1,relief="solid", font=("Arial", 10))
            label_horaire.grid(row=i+1, column=0, sticky="nsew")
            label_horaire.configure(bg=self.couleurs[i])

        

        machine_api = MachineAPI(self.token)
        machines = machine_api.get_machine_names()

        liste_cles = list(machines.keys())



        for i in range (len(self.horaires)):
                for j in range (len(self.filtre)):
                    label_machine = tk.Label(self.fenetre, text='Machine dispo', padx=10, pady=5, borderwidth=1, relief="flat", font=("Arial", 10, "bold"))
                    label_machine.grid(row=i+1, column=j+1, sticky="nsew")
                    

        for i in self.filtre :
            machine_name = machines[i]
            label_machine = tk.Label(self.fenetre, text=machine_name, padx=10, pady=5, borderwidth=1,relief="solid", font=("Arial", 10, "bold"))
            label_machine.grid(row=0, column=column_index, sticky="nsew")
            column_index+=1


        for i in liste_cles:
            if i in self.filtre :
                #print(i)
                #print('Nom machine :', machines[i])
                
                dispo = Available(self.token,self.start,self.end,i)
                booked_slots = dispo.is_machine_available()
                for slot in booked_slots:
                    start_at=slot['start_at']
                    start_at=datetime.fromisoformat(start_at[:-6])
                    start_at = start_at.strftime("%H")

                    end_at=slot['end_at']
                    end_at=datetime.fromisoformat(end_at[:-6])
                    end_at = end_at.strftime("%H")
                    a=self.filtre.index(slot["machine_id"])
                    label_machine = tk.Label(self.fenetre, text=slot['full_name'], padx=10, pady=5, borderwidth=1, relief="flat", font=("Arial", 10, "bold"))
                    label_machine.grid(row=int(start_at)-8, column=int(a)+1, sticky="nsew" )
                    label_machine.configure(bg=self.couleurs[int(start_at)-9])
                    #print(f"Debut : {start_at}, Fin : {end_at}, Reserve par : {slot['full_name']}")

                    

        
    




if __name__=='__main__':
    token = 'oPec4DpLw9mdFkqr3erCYwig'
    filtre=[1,9,18,26,27]
    start="2024-04-17T00:00:00+02:00"
    end="2024-04-17T22:00:00+02:00"
    fenetre=tk.Tk()
    instance = Schedule_week(token,filtre,start,end,fenetre)
    instance.week()
    fenetre.mainloop()