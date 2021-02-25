import sys
from showCoffee import ShowCoffee
from PyQt5 import QtWidgets


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ShowCoffee()
    ex.show()
    sys.exit(app.exec_())
