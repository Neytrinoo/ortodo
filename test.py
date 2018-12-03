import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QSpinBox
from PyQt5.QtWidgets import QInputDialog


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Диалоговые окна')

        self.s = QSpinBox(self)
        self.s.resize(50, 50)
        self.s.move(100, 100)
        self.b = QPushButton('Показать', self)
        self.b.resize(self.b.sizeHint())
        self.b.move(50, 50)
        self.b.clicked.connect(self.run)
        print(self.s.text())

        self.show()

    def run(self):
        print(self.s.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
