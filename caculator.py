import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
)
from PyQt5.QtCore import Qt


class IPhoneCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(360, 540)
        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

     
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(80)
        self.display.setReadOnly(True)
        self.display.setStyleSheet(
            "background-color: black; color: white; font-size: 32px; border: none; padding: 10px;"
        )
        main_layout.addWidget(self.display)

        # Buttons grid
        grid = QGridLayout()
        main_layout.addLayout(grid)

        buttons = [
            ('C', 0, 0), ('+/-', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        for text, row, col, rowspan, colspan in [b if len(b) == 5 else (*b, 1, 1) for b in buttons]:
            button = QPushButton(text)
            button.setFixedHeight(80)
            if text in {'/', '*', '-', '+', '='}:
                button.setStyleSheet(self.orange_button_style())
            elif text in {'C', '+/-', '%'}:
                button.setStyleSheet(self.gray_button_style())
            else:
                button.setStyleSheet(self.dark_button_style())

            grid.addWidget(button, row, col, rowspan, colspan)

            if text == '=':
                button.clicked.connect(self.calculate_result)
            elif text == 'C':
                button.clicked.connect(self.clear_display)
            elif text == '+/-':
                button.clicked.connect(self.toggle_sign)
            else:
                button.clicked.connect(lambda checked, t=text: self.append_to_display(t))

    def dark_button_style(self):
        return (
            "background-color: #505050; color: white; font-size: 24px; border-radius: 40px;"
        )

    def gray_button_style(self):
        return (
            "background-color: #d4d4d2; color: black; font-size: 24px; border-radius: 40px;"
        )

    def orange_button_style(self):
        return (
            "background-color: #ff9500; color: white; font-size: 24px; border-radius: 40px;"
        )

    def append_to_display(self, text):
        self.display.setText(self.display.text() + text)

    def clear_display(self):
        self.display.clear()

    def toggle_sign(self):
        current = self.display.text()
        if current:
            if current.startswith('-'):
                self.display.setText(current[1:])
            else:
                self.display.setText('-' + current)

    def calculate_result(self):
        expression = self.display.text()
        try:
            expression = expression.replace('%', '/100')
            result = str(eval(expression))
            self.display.setText(result)
        except Exception:
            self.display.setText("Error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IPhoneCalculator()
    window.show()
    sys.exit(app.exec_())
