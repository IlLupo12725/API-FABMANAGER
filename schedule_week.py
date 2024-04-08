from availabilities import Available
from id_machines import MachineAPI
from datetime import datetime

class Schedule_week:
    def __init__(self,token,filtre,start,end):
        self.token = token
        self.filtre=filtre
        self.start=start 
        self.end=end

    def week (self):
        machine_api = MachineAPI(token)
        machines = machine_api.get_machine_names()

        liste_cles = list(machines.keys())
        for i in liste_cles:
            if i in self.filtre :
                print("---------------------------------")
                print('Nom machine :', machines[i])
                dispo = Available(token,self.start,self.end,i)
                booked_slots = dispo.is_machine_available()
                if booked_slots:
                    print("Creneaux deja utilise  :")
                    for slot in booked_slots:
                        start_at=slot['start_at']
                        start_at=datetime.fromisoformat(start_at[:-6])
                        start_at = start_at.strftime("%Y-%m-%d %H:%M:%S")

                        end_at=slot['end_at']
                        end_at=datetime.fromisoformat(end_at[:-6])
                        end_at = end_at.strftime("%Y-%m-%d %H:%M:%S")
                        print(f"Debut : {start_at}, Fin : {end_at}, Reserve par : {slot['full_name']}")
                    else:
                        print('La machine est disponible')
            
                





if __name__=='__main__':
    token = 'oPec4DpLw9mdFkqr3erCYwig'
    filtre=[1,9,18,26,27]
    start="2024-04-10T00:00:00+02:00"
    end="2024-04-11T00:00:00+02:00"
    instance = Schedule_week(token,filtre,start,end)
    instance.week()