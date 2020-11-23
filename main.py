import sqlite3
import sys
from PyQt5 import QtWidgets, uic, QtCore


class ShowCoffee(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('showCoffee.ui', self)
        self.setLayout(self.gridLayout)
        self.pushButton.clicked.connect(self.showSorts)
        self.conn = sqlite3.connect('coffee.sqlite')

    def showSorts(self):
        cursor = self.conn.cursor()
        data = cursor.execute('SELECT * FROM coffeeVariants').fetchall()
        names = [desc[0] for desc in cursor.description]
        self.tableWidget.setColumnCount(len(names))
        self.tableWidget.setHorizontalHeaderLabels(names)
        for i in data:
            nowRow = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(nowRow + 1)
            for j in range(len(i)):
                nowItem = QtWidgets.QTableWidgetItem(str(i[j]))
                nowItem.setFlags(nowItem.flags() ^ QtCore.Qt.ItemIsEditable)
                self.tableWidget.setItem(nowRow, j, nowItem)
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ShowCoffee()
    ex.show()
    sys.exit(app.exec_())
