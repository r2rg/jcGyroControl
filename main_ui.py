from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QWidget, QPushButton, QComboBox, QLabel)
from PyQt6.QtCore import QThread, pyqtSlot, pyqtSignal
from main import motion_controls
import sys


class WorkerThread(QThread):
    status_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.directions = []

    def run(self):
        with open('config.txt', 'r') as file:
            for line in file:
                line = line.rstrip("\n")
                try:
                    line = int(line)
                    self.directions.append(line)
                except ValueError:
                    pass
        print(self.directions)
        motion_controls(self.directions)
        self.status_signal.emit("Not connected.")
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

        directions = []
        with open('config.txt', 'r') as file:
            for line in file:
                line = line.rstrip("\n")
                try:
                    line = int(line)
                    directions.append(line)
                except ValueError:
                    pass

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["L", "R"])
        layout.addWidget(QLabel("Hand"))  # Add the label first
        layout.addWidget(self.comboBox)
        self.comboBox.setCurrentIndex(directions[0])

        items_l = ["up", "right", "down", "left"]
        items_r = ["a", "b", "y", "x"]
        items = (items_l if self.comboBox.currentText() == "L" else items_r)

        # Combo boxes and Labels
        self.comboBoxes = [QComboBox(self) for _ in range(4)]
        self.labels = ["Click button", "Exit tracking process button",
                       "Center the pointer", "Toggle tracking on/off"]  # List of labels for each combobox

        for combo, label_text, direction in zip(self.comboBoxes, self.labels, directions[1:]):
            combo.addItems(items)
            combo.setCurrentIndex(direction)
            layout.addWidget(QLabel(label_text))  # Add the label first
            layout.addWidget(combo)  # Then add the combobox

        self.comboBox.currentIndexChanged.connect(self.update_combo)

        # Button
        self.button = QPushButton("Execute Function", self)
        self.button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.button)

        # Label for displaying errors
        self.statusLabel = QLabel('Not connected.', self)
        layout.addWidget(self.statusLabel)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_button_clicked(self):
        directions = [str(combo.currentIndex()) for combo in self.comboBoxes]
        directions.insert(0, str(self.comboBox.currentIndex()))
        with open("config.txt", "w"):
            pass
        with open("config.txt", "w") as file:
            for element in directions:
                file.write(element + "\n")

        try:
            print('Executing')
            self.thread = WorkerThread(self)
            self.thread.start()
            self.thread.status_signal.connect(self.update_status_label)
            self.update_status_label('Connected.')
        except Exception:
            print('Err')
            sys.exit(app.exec())

    def process_finished(self):
        print("Process finished.")
        self.p = None

    @pyqtSlot(str)
    def update_status_label(self, message):
        self.statusLabel.setText(message)

    def update_combo(self):
        items_l = ["up", "right", "down", "left"]
        items_r = ["x", "a", "b", "y"]
        items = (items_l if self.comboBox.currentText() == "L" else items_r)

        for combo in self.comboBoxes:
            combo.clear()
            combo.addItems(items)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
