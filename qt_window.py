from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from utils import *
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.run_button = QPushButton("Run")
        self.step_button = QPushButton("Step")
        self.load_button = QPushButton("Load")
        self.safe_button = QPushButton("Safe")
        self.text_edit = QPlainTextEdit()
        self.line_numbers = QTextEdit()
        self.terminal = QTextEdit()
        self.terminal_label = QLabel("Terminal")
        self.selection = QTextEdit.ExtraSelection()
        self.ui_init()

        self.A = Register_16_bit('A')
        self.B = Register_16_bit('B')
        self.C = Register_16_bit('C')
        self.D = Register_16_bit('D')

        self.selection.cursor = self.text_edit.textCursor()
        self.first_step = True
        self.step_num = 0

    def ui_init(self):
        self.run_button.clicked.connect(self.run)
        self.step_button.clicked.connect(self.step)
        self.load_button.clicked.connect(self.load)
        self.safe_button.clicked.connect(self.safe)

        self.text_edit.setPlainText('ADD A, B\nMOV BH, CH\nSUB C, D\nADD D, A')

        self.line_numbers.setReadOnly(True)
        self.line_numbers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.line_numbers.setFixedWidth(30)
        self.line_numbers.setPlainText('1')

        self.terminal.setReadOnly(True)
        self.terminal.setFixedHeight(150)

        self.selection.format.setBackground(QColor('#616161'))
        self.selection.format.setProperty(QTextFormat.FullWidthSelection, True)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.step_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.safe_button)

        text_layout = QHBoxLayout()
        text_layout.addWidget(self.line_numbers)
        text_layout.addWidget(self.text_edit)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(text_layout)
        main_layout.addWidget(self.terminal_label, Qt.AlignCenter)
        main_layout.addWidget(self.terminal)
        self.setLayout(main_layout)

        self.update_line_numbers()
        self.text_edit.cursorPositionChanged.connect(self.update_line_numbers)

    def load(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file')
        with open(file_name[0], 'r') as file:
            text = file.read()
            self.text_edit.setPlainText(text)

    def safe(self):
        file_name = QFileDialog.getSaveFileName(self, 'Save File')
        file = open(file_name[0], 'w')
        text = self.text_edit.toPlainText()
        file.write(text)
        file.close()

    def update_line_numbers(self):
        line_count = self.text_edit.blockCount()
        if line_count < 10:
            if self.line_numbers.toPlainText()[-1] != line_count:
                text = ""
                for i in range(1, line_count + 1):
                    text += str(i) + "\n"
                self.line_numbers.setPlainText(text)
        else:
            if self.line_numbers.toPlainText()[-2:] != line_count:
                text = ""
                for i in range(1, line_count + 1):
                    text += str(i) + "\n"
                self.line_numbers.setPlainText(text)

    def run(self):
        all_text = self.text_edit.toPlainText()
        lines = all_text.split('\n')

        for line in lines:
            self.parser(line)

    def step(self):
        if not self.first_step:
            self.selection.cursor.clearSelection()
            self.selection.cursor.movePosition(QTextCursor.Down)

        self.first_step = False
        self.selection.cursor.select(QTextCursor.LineUnderCursor)
        self.text_edit.setExtraSelections([self.selection])

        all_text = self.text_edit.toPlainText()
        lines = all_text.split('\n')

        if self.step_num == len(lines):
            self.step_num = 0
            self.selection.cursor.movePosition(QTextCursor.Start)
            self.first_step = True
        else:
            self.parser(lines[self.step_num])
            self.step_num += 1

    def parser(self, line):
        if len(line) == 0:
            return
        commands = line.split(' ')
        commands[1] = commands[1][:-1]
        match commands[1][0]:
            case 'A':
                firs_attribute = self.A
            case 'B':
                firs_attribute = self.B
            case 'C':
                firs_attribute = self.C
            case 'D':
                firs_attribute = self.D
            case _:
                self.terminal.append('zly rejestr')

        if len(commands[1]) == 2:
            match commands[1][1]:
                case 'L':
                    firs_attribute = firs_attribute.L
                case 'H':
                    firs_attribute = firs_attribute.H
                case _:
                    self.terminal.append('zly rejestr')

        # second atribute
        is_register = True

        match commands[2][0]:
            case 'A':
                second_attribute = self.A
            case 'B':
                second_attribute = self.B
            case 'C':
                second_attribute = self.C
            case 'D':
                second_attribute = self.D
            case '#':
                is_register = False
                second_attribute = [int(bit) for bit in commands[2][1:]]
                self.terminal.append(second_attribute)
            case _:
                self.terminal.append('zly rejestr')

        if is_register and len(commands[2]) == 2:
            match commands[2][1]:
                case 'L':
                    second_attribute = second_attribute.L
                case 'H':
                    second_attribute = second_attribute.H
                case _:
                    self.terminal.append('zly rejestr')

        self.terminal.append(f'First attribute: {firs_attribute.name}')
        if type(second_attribute) == list:
            self.terminal.append(f'Second attribute: {second_attribute}')
        else:
            self.terminal.append(f'Second attribute: {second_attribute.name}')
        # command
        match commands[0]:
            case 'ADD':
                self.terminal.append('Command: ADD')
                ADD(firs_attribute, second_attribute)
                self.terminal.append(f'Register {firs_attribute.name} value: {firs_attribute.register()}\n')
            case 'SUB':
                self.terminal.append('Command: SUB')
                SUB(firs_attribute, second_attribute)
                self.terminal.append(f'Register {firs_attribute.name} value: {firs_attribute.register()}\n', )
            case 'MOV':
                self.terminal.append('Command: MOV')
                MOV(firs_attribute, second_attribute)
                self.terminal.append(f'Register {firs_attribute.name} value: {firs_attribute.register()}\n')
            case _:
                self.terminal.append('zla komenda')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
