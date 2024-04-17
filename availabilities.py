from ask import Ask
import json
import os



class Available :
    def __init__(self, token,start,end,id):
        self.token = token
        self.url = "https://roselab.fab-manager.com/open_api/v1/reservations"
        self.id=id
        self.start=start
        self.end=end
        self.update()
        self.filter_reservations()
    
    def update(self):
    
        


        params = {
        "reservation_type": "Machine",
        "per_page" : [100]
        }
        
        instance=Ask(self.token,params,self.url)
        response=instance.ask()
        try :
            with open('reservation.json', 'r') as json_file:
                # Charger le contenu JSON
                data = json.load(json_file)
        except :
            with open('reservation.json', 'w') as json_file:
                    json.dump(response, json_file, indent=4)

        
        try :
            if (response['reservations'][0]['id']!=data['reservations'][0]['id']):
                print("Ecriture du JSON")
                with open('reservation.json', 'w') as json_file:
                    json.dump(response, json_file, indent=4)
        except :
            pass

    def is_json_empty(self,file_path):
        return os.stat(file_path).st_size == 0


    def filter_reservations(self):
        with open('reservation.json', 'r') as input_json_file:
            data = json.load(input_json_file)


        try : 
            with open('opti.json', 'r') as json_file:
                # Charger le contenu JSON
                data1 = json.load(json_file)

        except :
            print("erreur json, réécriture")
            with open('opti.json', 'w') as json_file:
                json.dump([], json_file)
            
        try :
            if (data1[0]['reservation_id'])==(data['reservations'][0]['id']):
                filtered_reservations = []
                for reservation in data['reservations']:
                    for slot in reservation['reserved_slots']:
                        filtered_reservation = {
                            'reservation_id': reservation['id'],
                            'full_name' : reservation['user']['full_name'],
                            'machine_id': reservation['reservable_id'],
                            'start_at': slot['start_at'],
                            'end_at': slot['end_at']
                        }
                        filtered_reservations.append(filtered_reservation)
            else :
                pass

        except :
            filtered_reservations = []
            for reservation in data['reservations']:
                for slot in reservation['reserved_slots']:
                    filtered_reservation = {
                        'reservation_id': reservation['id'],
                        'full_name' : reservation['user']['full_name'],
                        'machine_id': reservation['reservable_id'],
                        'start_at': slot['start_at'],
                        'end_at': slot['end_at']
                    }
                    filtered_reservations.append(filtered_reservation)



        with open('opti.json', 'w') as output_json_file:
            json.dump(filtered_reservations, output_json_file, indent=4)

        

    


        

    
    def is_machine_available(self):
        with open('opti.json', 'r') as input_json_file:
            data = json.load(input_json_file)
        booked_slots=[]
        # Parcourir toutes les réservations
        for reservation in data:
            # Vérifier si la réservation concerne la machine spécifiée
            if reservation["machine_id"] == self.id:
                reserved_start = reservation['start_at']
                reserved_end = reservation['end_at']
                full_name = reservation['full_name']
                machine_id = reservation['machine_id']
                # Vérifier si le créneau réservé chevauche le créneau spécifié
                if self.start < reserved_end and self.end > reserved_start:
                    booked_slots.append({'start_at': reserved_start, 'end_at': reserved_end, 'full_name': full_name,'machine_id' : machine_id})

        
        return booked_slots



    

        

if __name__=='__main__':
    token = 'oPec4DpLw9mdFkqr3erCYwig'
    instance = Available(token,"2024-04-13T8:00:00+02:00","2024-04-13T20:00:00+02:00",1)
    oui = instance.is_machine_available()
    print(oui)
    
