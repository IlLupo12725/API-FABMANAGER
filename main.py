from id_machines import MachineAPI


token = 'oPec4DpLw9mdFkqr3erCYwig'






if __name__ == '__main__':
    machine_api = MachineAPI(token)
    machines = machine_api.get_machine_names()
    print(machines)
