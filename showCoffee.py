import sqlite3
import sys
from PyQt5 import QtWidgets, uic, QtCore
from addEditCoffee import addEditCoffee
from UI import showCoffeeUI


class ShowCoffee(QtWidgets.QWidget, showCoffeeUI.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setLayout(self.gridLayout)
        self.pushButton_showCoffee.clicked.connect(self.showSorts)
        self.pushButton_addCoffee.clicked.connect(self.addEditCoffee)
        self.conn = sqlite3.connect('data/coffee.sqlite')

    def addEditCoffee(self):
        id1 = self.sender().text()
        try:
            id1 = int(id1)
        except ValueError:
            id1 = -1
        win = addEditCoffee(self, id1)
        win.exec_()
        self.showSorts()

    def showSorts(self):
        self.tableWidget.setRowCount(0)
        cursor = self.conn.cursor()
        data = cursor.execute('SELECT coffeeId, coffeeTitle, '
                              'rD.roastTitle, cT.coffeeTypeTitle, '
                              'coffeeTaste, coffeeCost, '
                              'coffeeVolume FROM coffeeVariants '
                              'INNER JOIN roastDegrees rD ON '
                              'coffeeVariants.coffeeRoast = rD.roastId '
                              'INNER JOIN coffeeTypes cT ON '
                              'coffeeVariants.coffeeMillType = cT.coffeeTypeId').fetchall()
        names = [desc[0] for desc in cursor.description]
        self.tableWidget.setColumnCount(len(names) + 1)
        self.tableWidget.setHorizontalHeaderLabels(names + ['Edit', ])
        for i in data:
            nowRow = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(nowRow + 1)
            for j in range(len(i)):
                nowItem = QtWidgets.QTableWidgetItem(str(i[j]))
                nowItem.setFlags(nowItem.flags() ^ QtCore.Qt.ItemIsEditable)
                self.tableWidget.setItem(nowRow, j, nowItem)

            btn = QtWidgets.QPushButton()
            btn.setText(str(i[0]))
            btn.clicked.connect(self.addEditCoffee)
            self.tableWidget.setCellWidget(nowRow, self.tableWidget.columnCount() - 1, btn)

        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ShowCoffee()
    ex.show()
    sys.exit(app.exec_())
