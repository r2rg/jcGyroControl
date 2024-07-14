from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel
from main import motion_controls
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Direction Selector")

        # Layout
        layout = QVBoxLayout()

        # Combo boxes and Labels
        self.comboBoxes = [QComboBox(self) for _ in range(4)]
        self.labels = ["CB1", "CB2", "CB3", "CB4"]  # List of labels for each combobox

        for combo, label_text in zip(self.comboBoxes, self.labels):
            combo.addItems(["up", "right", "down", "left"])
            layout.addWidget(QLabel(label_text))  # Add the label first
            layout.addWidget(combo)  # Then add the combobox

        self.errorLabel = QLabel('', self)
        layout.addWidget(QLabel(self.errorLabel))

        # Button
        self.button = QPushButton("Execute Function", self)
        self.button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.button)

        # Label for displaying errors
        self.errorLabel = QLabel("", self)
        layout.addWidget(self.errorLabel)

        # Central widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def on_button_clicked(self):
        directions = [combo.currentText() for combo in self.comboBoxes]

        controls = motion_controls(directions)
        if isinstance(controls, str):  # Check if myfunc returned an error message
            print('Err')
            self.errorLabel.setText('An error has occurred.')
        else:
            self.errorLabel.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
