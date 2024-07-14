from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QWidget, QPushButton, QComboBox, QLabel)
from PyQt6.QtCore import QThread
from main import motion_controls
import sys


class WorkerThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        with open('config.txt', 'r') as file:
            directions = file.read().split('\n')[:4]
        motion_controls(directions)
        self.quit()


class MainWindow(QMainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self):
        super().__init__()

        self.thread = None
        self.setWindowTitle("Motion Controls")
        self.p = None

        # Layout
        layout = QVBoxLayout()

        # Combo boxes and Labels
        self.comboBoxes = [QComboBox(self) for _ in range(4)]
        self.labels = ["Click button", "Exit tracking process button",
                       "Center the pointer", "Toggle tracking on/off"]  # List of labels for each combobox

        for combo, label_text in zip(self.comboBoxes, self.labels):
            combo.addItems(["up", "right", "down", "left"])
            layout.addWidget(QLabel(label_text))  # Add the label first
            layout.addWidget(combo)  # Then add the combobox

        for i in range(4):
            self.comboBoxes[i].setCurrentIndex(i)

        # Button
        self.button = QPushButton("Execute Function", self)
        self.button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.button)

        # Label for displaying errors
        self.statusLabel = QLabel('Not connected.', self)
        layout.addWidget(self.statusLabel)

        # Central widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def on_button_clicked(self):
        directions = [combo.currentText() for combo in self.comboBoxes]
        with open("config.txt", "w") as file:
            pass
        with open("config.txt", "w") as file:
            for element in directions:
                file.write(element + "\n")

        try:
            print('Executing')
            self.thread = WorkerThread(self)
            self.thread.start()
            self.statusLabel.setText('Connected.')
        except WindowsError:
            print('Err')
            sys.exit(app.exec())

    def process_finished(self):
        print("Process finished.")
        self.p = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
