from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QTableWidgetItem
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys

app = QApplication([])

database = QSqlDatabase.addDatabase('QSQLITE')
database.setDatabaseName('expense.db')
if not database.open():
    QMessageBox.critical(None,'Error',"Could not load database")
    sys.exit(1)

query = QSqlQuery()
if query.exec("""create table if not exists expenses (id integer primary key autoincrement, date text, category text, amount real, description text);"""): print('Success')


# app class
class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500,500)
        self.setWindowTitle('Expense Tracker App')
        self.dateBox = QDateEdit()
        self.dropdown = QComboBox()
        self.dropdown.addItems(['Food', 'Transportation', 'Entertainment', 'Bills', 'Clothings', 'Other'])
        self.amount = QLineEdit()
        self.description = QLineEdit()
        self.add_btn = QPushButton('Add Expense')
        self.add_btn.clicked.connect(self.add_data)
        self.delete_btn = QPushButton('Delete Expense')
        self.delete_btn.clicked.connect(self.delete_data)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Date', 'Category', 'Amount', 'Description'])

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel('Date: '))
        self.row1.addWidget(self.dateBox)
        self.row1.addWidget(QLabel('Category: '))
        self.row1.addWidget(self.dropdown)

        self.row2.addWidget(QLabel('Amount: '))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel('Description: '))
        self.row2.addWidget(self.description)

        self.row3.addWidget(self.add_btn)
        self.row3.addWidget(self.delete_btn)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        self.master_layout.addWidget(self.table)
        self.setLayout(self.master_layout)
        self.load_data()
    
    def load_data(self):
        self.table.setRowCount(0)
        row = 0
        query = QSqlQuery()
        if not query.exec("""select * from expenses"""):
            print('Error')
        while query.next():
            id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem(str(id)))
            self.table.setItem(row,1,QTableWidgetItem(date))
            self.table.setItem(row,2,QTableWidgetItem(category))
            self.table.setItem(row,3,QTableWidgetItem(str(amount)))
            self.table.setItem(row,4,QTableWidgetItem(description))
            row += 1

    def add_data(self):
        date = self.dateBox.date().toString('dd-MM-yyyy')
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        query = QSqlQuery()
        if not query.prepare("""insert into expenses (date, category, amount, description) 
                      values (?, ?, ?, ?);"""): print(query.lastError().text())  
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        if not query.exec(): print('Error Here')
        self.load_data()

    def delete_data(self):
        selected_row = self.table.currentRow()
        try:
            selectedId = int(self.table.item(selected_row,0).text())
            confirm = QMessageBox.question(self,'Are you sure?','Delete the row',QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.No:
                return
            else:
                query = QSqlQuery()
                if not query.prepare("""delete from expenses where id = ?"""): print(query.lastError().text())
                query.addBindValue(selectedId)
                query.exec()
                self.load_data()
        except AttributeError:
            QMessageBox.warning(self, 'No row selected', 'Please select a row to delete')

#Showing the app
if __name__ == '__main__':
    window = ExpenseApp()
    window.show()
    app.exec()