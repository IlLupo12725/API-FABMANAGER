from ask import Ask

class MachineAPI:
    def __init__(self, token):
        self.token = token
        self.url = "https://roselab.fab-manager.com/open_api/v1/machines"

    def get_machine_names(self):
        params=None
        instance=Ask(self.token,params,self.url)
        response=instance.ask()
        machines={}
        for machine in response["machines"]:
                    machines[machine["id"]] = machine["name"]
        return machines
    




if __name__ == "__main__":
    token = 'oPec4DpLw9mdFkqr3erCYwig'
    machine_api = MachineAPI(token)
    machines = machine_api.get_machine_names()
    print(machines)

