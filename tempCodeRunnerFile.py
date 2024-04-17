from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from availabilities import Available
from id_machines import MachineAPI
from datetime import datetime

class ScheduleWeek(QWidget):
    def __init__(self, token, filtre, start, end):
        super().__init__()
        self.token = token
        self.filtre = filtre
        self.start = start 
        self.end = end
        self.setWindowTitle("Réservations du jour")
        self.horaires = [
            "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
            "12:00 - 13:00", "13:00 - 14:00", "14:00 - 15:00",
            "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00",
            "18:00 - 19:00", "19:00 - 20:00", "20:00 - 21:00"
        ]
        self.couleurs = [
    "#FFC3A0",  # Saumon clair
    "#FFD2A0",  # Pêche clair
    "#FFECB3",  # Jaune pastel
    "#D0F0C0",  # Vert pastel
    "#B2EBF2",  # Bleu ciel
    "#B2CCFF",  # Bleu lavande
    "#C9B2FF",  # Lavande
    "#FFC1FF",  # Rose clair
    "#FFABAB",  # Rouge pastel
    "#FFD8B1",  # Orange pastel
    "#FFEEB8",  # Jaune citron
    "#B8F2E6"   # Vert menthe
]
# self.couleurs = [
#     "#FFFFCC",  # Saumon clair
#     "#FFCC99",  # Pêche clair
#     "#FFCCCC",  # Jaune pastel
#     "#FF99CC",  # Vert pastel
#     "#FFCCFF",  # Bleu ciel
#     "#CC99FF",  # Bleu lavande
#     "#CCCCFF",  # Lavande
#     "#99CCFF",  # Rose clair
#     "#CCFFFF",  # Rouge pastel
#     "#99FFCC",  # Orange pastel
#     "#CCFFCC",  # Jaune citron
#     "#CCFF99"   # Vert menthe
# ]

        self.layout = QGridLayout()

        # Ajouter les horaires
        for i, horaire in enumerate(self.horaires):
            label_horaire = QLabel(horaire)
            label_horaire.setStyleSheet("QLabel { background-color : " + self.couleurs[i] + "; border: 1px solid black; font-size: 14pt;}")
            self.layout.addWidget(label_horaire, i+1, 0)

        # Récupérer les noms de machines
        machine_api = MachineAPI(self.token)
        machines = machine_api.get_machine_names()
        
        # Ajouter les noms de machines
        for i, machine_id in enumerate(self.filtre):
            machine_name = machines[machine_id]
            label_machine = QLabel(machine_name)
            label_machine.setStyleSheet("QLabel { background-color : #DDDDDD; border: 1px solid black; font-size: 14pt;}")
            self.layout.addWidget(label_machine, 0, i+1)

        # Ajouter les réservations
        current_time = datetime.now().strftime("%H")
        current_row = int(current_time) - 8 # Pour convertir l'heure actuelle en ligne dans la grille

        for machine_id in self.filtre:
            dispo = Available(self.token, self.start, self.end, machine_id)
            booked_slots = dispo.is_machine_available()
            for slot in booked_slots:
                start_at = datetime.fromisoformat(slot['start_at'][:-6]).strftime("%H")
                row = int(start_at) - 8
                column = self.filtre.index(slot["machine_id"]) + 1
                label_reservation = QLabel(slot['full_name'])
                if row == current_row:  # Vérifie si c'est le créneau actuel
                    label_reservation.setStyleSheet("QLabel { background-color : " + self.couleurs[int(start_at)-9] + "; border: 5px solid red; font-size: 14pt; }")
                else:
                    label_reservation.setStyleSheet("QLabel { background-color : " + self.couleurs[int(start_at)-9] + "; border: 1px solid black; font-size: 14pt; }")
                self.layout.addWidget(label_reservation, row, column)

        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication([])
    token = 'oPec4DpLw9mdFkqr3erCYwig'
    filtre = [1, 9, 18, 26, 27]
    start = "2024-04-17T00:00:00+02:00"
    end = "2024-04-1T22:00:00+02:00"
    fenetre = ScheduleWeek(token, filtre, start, end)
    fenetre.show()
    app.exec_()
