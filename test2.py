import sys

from PyQt5 import QtWidgets, QtCore


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, QtCore.Qt.Window)
        self.build()

    def build(self):
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.buttons = []
        for i in range(5):
            but = QtWidgets.QPushButton('button {}'.format(i), self)
            self.mainLayout.addWidget(but)
            self.buttons.append(but)

        self.setLayout(self.mainLayout)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.secondWin = None
        self.build()

    def build(self):
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.lab = QtWidgets.QLabel('simple text', self)
        self.mainLayout.addWidget(self.lab)

        self.but1 = QtWidgets.QPushButton('open window', self)
        self.but1.clicked.connect(self.openWin)
        self.mainLayout.addWidget(self.but1)

        self.setLayout(self.mainLayout)

    def openWin(self):
        if not self.secondWin:
            self.secondWin = SecondWindow(self)
        self.secondWin.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())