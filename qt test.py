import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QProgressBar, QDialog
from PyQt5.QtCore import QTimer, Qt
from availabilities import Available
from id_machines import MachineAPI
from datetime import datetime

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chargement...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def start_loading(self):
        self.show()
        self.progress_value = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)

    def update_progress(self):
        self.progress_bar.setValue(int(self.progress_value))
        if self.progress_value >= 100:
            self.timer.stop()
            print('fermer')
            self.accept()
            self.close()

class ScheduleWeek(QWidget):
   
    def __init__(self, token, filtre, start, end, progress_dialog):
        super().__init__()
        self.token = token
        self.filtre = filtre
        self.start = start 
        self.end = end
        self.progress_dialog = progress_dialog
        self.setWindowTitle("Réservations du jour")
        self.progress_value=0
        self.horaires = [
            "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
            "12:00 - 13:00", "13:00 - 14:00", "14:00 - 15:00",
            "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00",
            "18:00 - 19:00", "19:00 - 20:00", "20:00 - 21:00"
        ]
        self.couleurs = [
            "#FFC3A0", "#FFD2A0", "#FFECB3", "#D0F0C0", "#B2EBF2", "#B2CCFF",
            "#C9B2FF", "#FFC1FF", "#FFABAB", "#FFD8B1", "#FFEEB8", "#B8F2E6"
        ]

        self.layout = QGridLayout()

        for i, horaire in enumerate(self.horaires):
            label_horaire = QLabel(horaire)
            label_horaire.setStyleSheet("QLabel { background-color : " + self.couleurs[i] + "; border: 1px solid black; font-size: 14pt;}")
            self.layout.addWidget(label_horaire, i+1, 0)

        machine_api = MachineAPI(self.token)
        machines = machine_api.get_machine_names()
        
        for i, machine_id in enumerate(self.filtre):
            machine_name = machines[machine_id]
            label_machine = QLabel(machine_name)
            label_machine.setStyleSheet("QLabel { background-color : #DDDDDD; border: 1px solid black; font-size: 14pt;}")
            self.layout.addWidget(label_machine, 0, i+1)

        current_time = datetime.now().strftime("%H")
        current_row = int(current_time) - 8

        for machine_id in self.filtre:
            dispo = Available(self.token, self.start, self.end, machine_id)
            booked_slots = dispo.is_machine_available()
            total_slots = len(booked_slots)
            for idx, slot in enumerate(booked_slots):
                start_at = datetime.fromisoformat(slot['start_at'][:-6]).strftime("%H")
                row = int(start_at) - 8
                column = self.filtre.index(slot["machine_id"]) + 1
                label_reservation = QLabel(slot['full_name'])
                if row == current_row:
                    label_reservation.setStyleSheet("QLabel { background-color : " + self.couleurs[int(start_at)-9] + "; border: 5px solid red; font-size: 14pt; }")
                else:
                    label_reservation.setStyleSheet("QLabel { background-color : " + self.couleurs[int(start_at)-9] + "; border: 1px solid black; font-size: 14pt; }")
                self.layout.addWidget(label_reservation, row, column)
                self.progress_value = total_slots * 100 / len(self.filtre)  # Calcule la progression en pourcentage
                self.progress_dialog.progress_bar.setValue(int(self.progress_value))
        self.progress_dialog.progress_bar.setValue(100)
        self.close()

        self.setLayout(self.layout)

    def closeEvent(self, event):
        self.progress_dialog.close()

if __name__ == '__main__':
    app = QApplication([])

    token = 'oPec4DpLw9mdFkqr3erCYwig'
    filtre = [1, 9, 18, 26, 27]
    start = "2024-04-17T00:00:00+02:00"
    end = "2024-04-17T22:00:00+02:00"
    
    progress_dialog = ProgressDialog()
    progress_dialog.start_loading()

    fenetre = ScheduleWeek(token, filtre, start, end, progress_dialog)
    fenetre.show()
    
    sys.exit(app.exec_())
