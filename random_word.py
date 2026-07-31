#import necessary modules
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from random import choice

words = ['hello','world','farhad','hossain','book','cook','chicken']
#main app objects
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle('My first app')
main_window.resize(400,400)

#create all app components using widgets
title = QLabel('Random word guess')
text_1 = QLabel('?')
text_2 = QLabel('?')
text_3 = QLabel('?')

button1 = QPushButton('Click Me')
button2 = QPushButton('Click Me')
button3 = QPushButton('Click Me')

#Design
master_layout = QVBoxLayout()

row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()

row1.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
row2.addWidget(text_1, alignment=Qt.AlignmentFlag.AlignCenter)
row2.addWidget(text_2,alignment=Qt.AlignmentFlag.AlignCenter)
row2.addWidget(text_3,alignment=Qt.AlignmentFlag.AlignCenter)
row3.addWidget(button1, alignment=Qt.AlignmentFlag.AlignCenter)
row3.addWidget(button2, alignment=Qt.AlignmentFlag.AlignCenter)
row3.addWidget(button3, alignment=Qt.AlignmentFlag.AlignCenter)

master_layout.addLayout(row1)
master_layout.addLayout(row2)
master_layout.addLayout(row3)

main_window.setLayout(master_layout)
#Events
def random_word1():
    word = choice(words)
    text_1.setText(word)

def random_word2():
    word = choice(words)
    text_2.setText(word)

def random_word3():
    word = choice(words)
    text_3.setText(word)

button1.clicked.connect(random_word1)
button2.clicked.connect(random_word2)
button3.clicked.connect(random_word3)

#Show and run
main_window.show()
app.exec()