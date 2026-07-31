from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QFont

class CalcApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400,400)
        self.setWindowTitle('Calculator app')
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont('Times new roman',25))
        self.grid = QGridLayout()
        self.buttons_list = ['7','8','0','/',
                        '4','5','6','*',
                        '1','2','3','-',
                        '0','.','=','+']
        self.clear = QPushButton('Clear')
        self.delete = QPushButton('<')

        row = 0
        column = 0
        for text in self.buttons_list:
            button = QPushButton(text)
            button.clicked.connect(self.button_clicked)
            button.setStyleSheet(' QPushButton { font: sans serif; font-size: 16px; padding: 5px; border-radius: 10px; background-color: lightgrey;} ')
            self.grid.addWidget(button, row, column)
            column += 1
            if column > 3:
                column = 0
                row += 1
            
        self.clear.clicked.connect(self.button_clicked)
        self.delete.clicked.connect(self.button_clicked)
        button_row = QHBoxLayout()
        button_row.addWidget(self.clear)
        button_row.addWidget(self.delete)
        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(button_row)
        master_layout.addLayout(self.grid)
        master_layout.setContentsMargins(25,25,25,25)
        self.setLayout(master_layout)

    # creating event handler functions
    def button_clicked(self):
        button = app.sender()
        text = button.text()

        if text == '=':
            symbol = self.text_box.text()
            try:
                res = eval(symbol)
                self.text_box.setText(str(res))
            except Exception as e:
                print('Error:', e)

        elif text == 'Clear':
            self.text_box.clear()

        elif text == '<':
            symbol = self.text_box.text()
            self.text_box.setText(symbol[:-1])
        
        else:
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)  

if __name__ in '__main__':
    app = QApplication([])
    main_window = CalcApp()
    main_window.show()
    app.exec()