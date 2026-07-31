from PyQt6.QtWidgets import QWidget, QApplication, QFileDialog, QVBoxLayout, QHBoxLayout, QGridLayout,  QPushButton, QLineEdit, QListWidget, QComboBox, QListWidgetItem, QLabel
from PyQt6.QtCore import Qt, QBuffer, QIODevice
from PyQt6.QtGui import QPixmap
import os, io
from PIL import Image, ImageEnhance, ImageFilter
from PIL.ImageQt import ImageQt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900,700)
        self.setWindowTitle('Very basic photo editor')
        button_list = ['Left', 'Right', 'Mirror', 'Sharpen', 'B/W', 'Contrast', 'Blur']
        filterbox_items = ['Original', 'Left', 'Right', 'Mirror', 'Sharpen', 'B/W', 'Color', 'Contrast', 'Blur']

        btn_folder = QPushButton('Select and insert images')
        self.image_area = QListWidget()
        list_item = QComboBox()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        self.image = QLabel('Image will appear here')
        master_layout = QHBoxLayout()

        col1.addWidget(btn_folder)
        col1.addWidget(self.image_area)

        for button_name in button_list:
            button = QPushButton(button_name)
            col1.addWidget(button)
            button.clicked.connect(self.onClick)

        list_item.addItems(filterbox_items)
        col1.addWidget(list_item)
        col2.addWidget(self.image)
        master_layout.addLayout(col1, 20)
        master_layout.addLayout(col2, 80)
        self.setLayout(master_layout)

        btn_folder.clicked.connect(self.getWorkingDirectory)
        self.image_area.itemClicked.connect(self.load_image)

    # App functionality

    def getWorkingDirectory(self):
        file, _ = list(QFileDialog.getOpenFileName(self, "Select an image", "", "Image (*.jpg *.jpeg *.svg *.png)"))
        if file:
            self.image_area.addItem(file)

    def usePixmap(self, pil_image):
        q_image = ImageQt(pil_image).copy()
        image = QPixmap.fromImage(q_image)
        image = image.scaled(self.image.width(), self.image.height(), Qt.AspectRatioMode.KeepAspectRatio)
        self.image.setPixmap(image)

    def load_image(self, file):
        self.image.clear()
        file_path = file.text()
        pil_image = Image.open(file_path)
        pil_image = pil_image.convert('RGBA')
        self.usePixmap(pil_image)

    def onClick(self):
        button = app.sender()
        text = button.text()
        try:
            buffer = QBuffer()
            buffer.open(QIODevice.OpenModeFlag.ReadWrite)
            qimage = self.image.pixmap().toImage()
            qimage.save(buffer, 'JPG')
            byte_data = buffer.data()
            buffer.close()
            pil_image = Image.open(io.BytesIO(byte_data))

            if pil_image.mode != 'RGBA':
                pil_image = pil_image.convert('RGBA')

            if text == 'B/W':
                pil_image = pil_image.convert('L')
                self.usePixmap(pil_image)

        except Exception as e:
            self.image.setText(f'Load Your Image First')

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()