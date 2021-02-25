import sqlite3
import sys

from PyQt5 import QtWidgets

from UI import addEditCoffeeUI


class addEditCoffee(QtWidgets.QDialog, addEditCoffeeUI.Ui_Dialog):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.gridLayout)
        self.conn = sqlite3.connect('data/coffee.sqlite')
        self.id = id
        self.prepare()

    def prepare(self):
        self.spinBox_cost.lineEdit().setReadOnly(True)
        self.spinBox_volume.lineEdit().setReadOnly(True)
        cursor = self.conn.cursor()
        self.comboBox_millType.addItems([i[0] for i in
                                         cursor.execute('SELECT coffeeTypeTitle FROM coffeeTypes').fetchall()])
        self.comboBox_roastType.addItems([i[0] for i in
                                          cursor.execute('SELECT roastTitle FROM roastDegrees').fetchall()])
        self.pushButton_save.clicked.connect(self.save)

        if self.id != -1:
            cursor = self.conn.cursor()
            self.lineEdit_title.setText(cursor.execute('SELECT coffeeTitle '
                                                       'FROM coffeeVariants '
                                                       'WHERE coffeeId=?',
                                                       (self.id,)).fetchone()[0])

            self.comboBox_roastType.setCurrentText(cursor.execute('SELECT roastTitle '
                                                                  'FROM roastDegrees '
                                                                  'WHERE roastId='
                                                                  '(SELECT coffeeRoast FROM coffeeVariants '
                                                                  'WHERE coffeeId=?)',
                                                                  (self.id,)
                                                                  ).fetchone()[0])

            self.lineEdit_taste.setText(cursor.execute('SELECT coffeeTaste '
                                                       'FROM coffeeVariants '
                                                       'WHERE coffeeId=?',
                                                       (self.id,)).fetchone()[0])

            self.spinBox_volume.setValue(cursor.execute('SELECT coffeeVolume '
                                                        'FROM coffeeVariants '
                                                        'WHERE coffeeId=?',
                                                        (self.id,)).fetchone()[0])

            self.spinBox_cost.setValue(cursor.execute('SELECT coffeeCost '
                                                      'FROM coffeeVariants '
                                                      'WHERE coffeeId=?',
                                                      (self.id,)).fetchone()[0])

    def save(self):
        cursor = self.conn.cursor()
        title = self.lineEdit_title.text()
        if not title:
            return
        roastType = cursor.execute('SELECT roastId FROM roastDegrees WHERE roastTitle=?',
                                   (self.comboBox_roastType.currentText(),)).fetchone()[0]
        coffeeType = cursor.execute('SELECT coffeeTypeId FROM coffeeTypes WHERE coffeeTypeTitle=?',
                                    (self.comboBox_millType.currentText(),)).fetchone()[0]
        coffeeTaste = self.lineEdit_taste.text()
        if not coffeeTaste:
            return
        coffeeCost = self.spinBox_cost.value()
        coffeeVolume = self.spinBox_volume.value()

        if self.id == -1:
            # add
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO "
                           "coffeeVariants(coffeeTitle, coffeeRoast, coffeeMillType, "
                           "coffeeTaste, coffeeCost, coffeeVolume) "
                           "VALUES (?,?,?,?,?,?)",
                           (title, roastType, coffeeType, coffeeTaste, coffeeCost, coffeeVolume))
            self.conn.commit()
            self.close()
            return

        cursor = self.conn.cursor()
        cursor.execute("UPDATE coffeeVariants SET "
                       "coffeeTitle=?, coffeeRoast=?, coffeeMillType=?, coffeeTaste=?, coffeeCost=?, coffeeVolume=? "
                       "WHERE coffeeId=?",
                       (title, roastType, coffeeType, coffeeTaste, coffeeCost, coffeeVolume, self.id))
        self.conn.commit()
        self.close()
        return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = addEditCoffee(-1)
    ex.show()
    sys.exit(app.exec_())
