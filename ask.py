import requests
class Ask:
    def __init__(self, token,params,url):
        self.token = token
        self.url = url
        self.params=params
        self.headers = {'Authorization': f'Token {self.token}'}

    def ask(self):
        try:
            response = requests.get(self.url, params=self.params,headers=self.headers)

            # Vérifier si la requête a réussi (code 200)
            if response.status_code == 200:
                return response.json()

            else:
                print(f"Erreur {response.status_code} - Impossible de récupérer les machines.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")



if __name__ == "__main__":
    token = 'oPec4DpLw9mdFkqr3erCYwig'
    params =  {
        "reservable_type":"Machine"
        }
    url = "https://roselab.fab-manager.com/open_api/v1/reservations"
    instance=Ask(token,params,url)
    a=instance.ask()
    print(a)



