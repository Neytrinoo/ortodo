import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QSpinBox, QScrollArea, QVBoxLayout, QScrollBar
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('Диалоговые окна')

        self.sca = QScrollArea(self)
        self.b = QPushButton('Да', self.sca)
        self.b.resize(50, 50)
        self.b.move(50, 100)
        self.b2 = QPushButton('нет', self.sca)
        self.b2.resize(50, 50)
        self.b2.move(10, 300)
        self.sca.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.sca.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.sca.setHorizontalScrollBar(QScrollBar(self.b2))
        self.show()

    def run(self):
        print(self.s.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
