from ask import Ask
import json



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
            with open('reservation.json', 'w') as json_file:
                    json.dump(response, json_file, indent=4)
        


    def filter_reservations(self):
        with open('reservation.json', 'r') as input_json_file:
            data = json.load(input_json_file)

        
        


        filtered_reservations = []
        for reservation in data['reservations']:
            for i in range (len(reservation['reserved_slots'])):
                filtered_reservation = {
                    'reservation_id': reservation['id'],
                    'full_name' : reservation['user']['full_name'],
                    'machine_id': reservation['reservable_id'],
                    'start_at': reservation['reserved_slots'][i]['start_at'],  # Assuming there's at least one slot
                    'end_at': reservation['reserved_slots'][i]['end_at']
                                # Assuming there's at least one slot
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
                # Vérifier si le créneau réservé chevauche le créneau spécifié
                if self.start < reserved_end and self.end > reserved_start:
                    booked_slots.append({'start_at': reserved_start, 'end_at': reserved_end, 'full_name': full_name})

        
        return booked_slots



    

        

if __name__=='__main__':
    token = 'oPec4DpLw9mdFkqr3erCYwig'
    instance = Available(token,"2024-04-10T18:00:00+02:00","2024-04-10T20:00:00+02:00",1)
    availbilities = instance.is_machine_available()
    
