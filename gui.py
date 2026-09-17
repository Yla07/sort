import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QTextEdit,
)

from backend import sortowanie


class SortWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sorter = sortowanie()
        self.setWindowTitle("Sorting Visualizer")
        self.resize(560, 520)
        self._build_ui()
        self._update_list()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        controls = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Min:"))
        self.min_input = QLineEdit("0")
        self.min_input.setValidator(QIntValidator(-1000000, 1000000))
        row1.addWidget(self.min_input)

        row1.addWidget(QLabel("Max:"))
        self.max_input = QLineEdit("100")
        self.max_input.setValidator(QIntValidator(-1000000, 1000000))
        row1.addWidget(self.max_input)

        row1.addWidget(QLabel("Size:"))
        self.size_input = QLineEdit("10")
        self.size_input.setValidator(QIntValidator(1, 100000))
        row1.addWidget(self.size_input)

        controls.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Value:"))
        self.value_input = QLineEdit()
        self.value_input.setValidator(QIntValidator(-1000000, 1000000))
        row2.addWidget(self.value_input)

        row2.addWidget(QLabel("Algorithm:"))
        self.algorithm_box = QComboBox()
        self.algorithm_box.addItems([
            "Bubble Sort",
            "Quick Sort",
            "Insertion Sort",
            "Selection Sort",
        ])
        row2.addWidget(self.algorithm_box)
        controls.addLayout(row2)

        buttons = QHBoxLayout()
        self.generate_btn = QPushButton("Generate")
        self.add_btn = QPushButton("Add value")
        self.clear_btn = QPushButton("Clear")
        self.sort_btn = QPushButton("Sort")

        self.generate_btn.clicked.connect(self.generate_data)
        self.add_btn.clicked.connect(self.add_value)
        self.clear_btn.clicked.connect(self.clear_data)
        self.sort_btn.clicked.connect(self.sort_data)

        buttons.addWidget(self.generate_btn)
        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.clear_btn)
        buttons.addWidget(self.sort_btn)
        controls.addLayout(buttons)

        layout.addLayout(controls)

        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setSelectionMode(self.list_widget.SelectionMode.SingleSelection)
        layout.addWidget(self.list_widget)

        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)
        self.status_box.setPlaceholderText("Status will appear here...")
        layout.addWidget(self.status_box)

    def _update_list(self):
        self.list_widget.clear()
        for item in self.sorter.get_data():
            self.list_widget.addItem(str(item))

    def _show_error(self, message):
        QMessageBox.critical(self, "Input error", message)

    def generate_data(self):
        try:
            minimum = int(self.min_input.text())
            maximum = int(self.max_input.text())
            size = int(self.size_input.text())
        except ValueError:
            self._show_error("Please enter valid integer values.")
            return

        if maximum < minimum:
            self._show_error("Maximum value must be greater than or equal to minimum value.")
            return

        data = self.sorter.generate_data(minimum, maximum, size)
        self.sorter.data = data
        self._update_list()
        self.status_box.setPlainText(
            f"Generated {len(data)} random numbers from {minimum} to {maximum}."
        )

    def add_value(self):
        value_text = self.value_input.text().strip()
        if not value_text:
            self._show_error("Enter a number to add.")
            return

        try:
            value = int(value_text)
        except ValueError:
            self._show_error("Only integers are supported in this project.")
            return

        self.sorter.add(value)
        self._update_list()
        self.status_box.setPlainText(f"Added {value} to the list.")
        self.value_input.clear()

    def clear_data(self):
        self.sorter.clear()
        self._update_list()
        self.status_box.setPlainText("List cleared.")

    def sort_data(self):
        if not self.sorter.get_data():
            self._show_error("There are no numbers to sort.")
            return

        algorithm = self.algorithm_box.currentText()
        data = list(self.sorter.get_data())

        if algorithm == "Bubble Sort":
            result = self.sorter.bubble_sort(data)
        elif algorithm == "Quick Sort":
            result = self.sorter.quick_sort(data)
        elif algorithm == "Insertion Sort":
            result = self.sorter.insertion_sort(data)
        else:
            result = self.sorter.selection_sort(data)

        self.sorter.data = result
        self._update_list()
        self.status_box.setPlainText(f"Sorted with {algorithm}: {result}")


def main():
    app = QApplication(sys.argv)
    window = SortWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
