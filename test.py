# import json
# import os
import datetime
print(str(datetime.datetime.today().date()).split('-'))






















# data = open('notes.json').read()
# a = json.loads(data)
# a['notes'][0]['text'] += ' редактированная'
#
# g = open('notes2.json', mode='w').write(json.dumps(a, ensure_ascii=False))
# data = open('notes2.json').read()
# print(data)
# import sys
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
# import PyQt5.QtGui as QtGui
#
#
# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setGeometry(300, 300, 150, 150)
#         self.setWindowTitle('Кто отправил сигнал')
#
#         self.button_1 = QPushButton(self)
#         self.button_1.move(20, 40)
#         self.button_1.setText("Кнопка 1")
#         self.button_1.clicked.connect(self.run)
#
#         self.button_2 = QPushButton(self)
#         self.button_2.move(20, 80)
#         self.button_2.setText("Кнопка 2")
#         self.button_2.clicked.connect(self.run)
#
#         self.show()
#
#     def run(self):
#         print(self.sender().text())
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     ex.show()
#     sys.exit(app.exec())

