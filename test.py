import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QSpinBox, QScrollArea, QVBoxLayout, QScrollBar, \
    QTextEdit, QLineEdit, QGroupBox, QLabel, QRadioButton
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('Диалоговые окна')

        self.sca = QScrollArea(self)
        self.gb = QGroupBox(self)
        self.tx = QPushButton('Я кнопка', self.gb)
        self.tx.clicked.connect(self.run)
        self.tx.resize(self.tx.sizeHint())
        self.gb.resize(2000, 2000)
        self.gb.move(20, 20)
        self.tx.move(0, 0)
        self.sca.resize(100, 100)
        self.sca.setWidget(self.gb)
        self.r1 = QRadioButton('Один', self)
        self.r1.resize(60, 20)
        self.r1.move(100, 200)
        self.r2 = QRadioButton('Два', self)
        self.r2.resize(60, 20)
        self.r2.move(100, 230)
        self.show()

    def run(self):
        self.r1.setAutoExclusive(False)
        self.r1.setChecked(False)
        self.r2.setAutoExclusive(False)
        self.r2.setChecked(False)
        print(self.r1.isChecked())
        print(self.r2.isChecked())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
