from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, QMainWindow, QTreeView, QMessageBox, QFileDialog
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import os

class FinanceApp(QMainWindow):
    def __init__(self):
        super(FinanceApp, self).__init__()
        self.setWindowTitle("Finance App")
        self.resize(800, 600)
        main_window = QWidget()

        self.label1 = QLabel("Interest Rate (%): ")
        self.label2 = QLabel("initial investment: ")
        self.label3 = QLabel("Years to invest: ")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.interestRate = QLineEdit()
        self.inintialInvestment = QLineEdit()
        self.years = QLineEdit()
        # creating our tree view using the QTreeView widget
        self.model = QStandardItemModel()
        self.treeView = QTreeView()
        self.treeView.setModel(self.model)

        self.dark_mode = QCheckBox("Dark Mode")
        self.dark_mode.stateChanged.connect(self.toggle)
        self.calculateBtn = QPushButton("Calculate")
        self.calculateBtn.clicked.connect(self.calculate)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.delete)
        self.saveMe = QPushButton("Save")
        self.saveMe.clicked.connect(self.save)

        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()

        self.row1.addWidget(self.label1)
        self.row1.addWidget(self.interestRate)
        self.row1.addWidget(self.label2)
        self.row1.addWidget(self.inintialInvestment)
        self.row1.addWidget(self.label3)
        self.row1.addWidget(self.years)
        self.row1.addWidget(self.dark_mode)

        self.row2.addWidget(self.treeView, 30)
        self.row2.addWidget(self.canvas, 70)

        self.master_layout = QVBoxLayout()
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addWidget(self.calculateBtn)
        self.master_layout.addWidget(self.deleteBtn)
        self.master_layout.addWidget(self.saveMe)

        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)
        self.apply_style()

    def calculate(self):
        try:
            interestRate = float(self.interestRate.text())
            initialInvestment = float(self.inintialInvestment.text())
            years = int(self.years.text())
        
        except ValueError:
            QMessageBox.warning(self,"Error", "Please enter numeric value in 'Years To invest' field")
            return
        
        total = initialInvestment
        for year in range(1,years + 1):
            total += total * (interestRate/100)
            yeatItem = QStandardItem(str(year))
            totalItem = QStandardItem("{:.2f}".format(total))
            self.model.appendRow([yeatItem, totalItem])

        self.figure.clear()
        yrs = list(range(1,years+1))
        amount = [initialInvestment*(1 + (interestRate/100))**yr for yr in yrs]
        ax = self.figure.subplots()
        ax.plot(yrs, amount)
        ax.set_title("Interest Chart")
        ax.set_xlabel("No. of Years")
        ax.set_ylabel("Amount")
        self.canvas.draw()

    def delete(self):
        self.interestRate.clear()
        self.inintialInvestment.clear()
        self.years.clear()
        self.model.clear()
        self.figure.clear()
        self.canvas.draw()

    def file(self, base_path):
        os.makedirs(base_path)
        file_path = os.path.join(base_path, "results.csv")
        with open(file_path, 'w') as file:
            for row in range(self.model.rowCount()):
                years = self.model.index(row,0).data()
                amount = self.model.index(row,1).data()
                file.write("{},{}".format(years,amount))
        plt.savefig(f"{base_path}/charts.png")

    def save(self):
        selected_dir = QFileDialog.getExistingDirectory(self, "Select a folder")
        base_path = os.path.join(selected_dir,"Saved")
        if not os.path.exists(base_path):
            self.file(base_path)
        else:
            counter = 1
            while os.path.exists(base_path + str(counter)):
                counter += 1
            new_path = base_path + str(counter)
            self.file(new_path)

    def toggle(self):
        self.apply_style()

    def apply_style(self):
        self.setStyleSheet("""
                FinanceApp{
                            background-color: grey;
                               }
                QLabel, QLineEdit, QPushButton, QCheckBox{
                            background-color: white;
                               }
                QTreeView{
                            background-color: grey;
                               }
""")
        if self.dark_mode.isChecked():
            self.setStyleSheet("""
                FinanceApp{
                            background-color: black;
                               }
                QLabel, QLineEdit, QPushButton, QCheckBox{
                            background-color: #333333;
                            color: #eeeeee;
                               }
                QTreeView{
                            background-color: #222222;
                            color: #eeeeee;
                               }
""")

if __name__ == "__main__":
    app = QApplication([])
    window = FinanceApp()
    window.show()
    app.exec()