import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QGroupBox, QVBoxLayout
from PyQt5.QtGui import QPixmap
import json
import os
import datetime


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        # self.b = QPushButton('', self)
        # self.b.setIcon(self.add_todo.icon())
        # self.b.resize(self.add_todo.size())
        # self.b.setIconSize(self.add_todo.iconSize())
        # self.b.setCursor(self.add_todo.cursor())
        # self.b.move(500, 500)
        # self.lab = QLabel(self)
        # self.lab.setStyleSheet('color: rgb(50, 0, 70)')
        # self.lab.setPalette(self.text_todo.palette())
        # self.lab.setText(self.text_todo.text())
        # self.lab.resize(self.text_todo.size())
        # self.lab.setFont(self.text_todo.font())
        # self.lab.move(100, 500)

        # vbox = QVBoxLayout()
        # vbox.addWidget(self.lab)
        # vbox.addStretch(1)
        # self.groupBox_2.resize(0, 0)
        self.add_todo.clicked.connect(self.add_todo_f)
        self.arr_to_dos = []

        self.start_programm()

    def start_programm(self):
        self.text_todo.resize(0, 0)
        self.time_todo.resize(0, 0)
        self.not_todo.resize(0, 0)
        self.todo.resize(0, 0)

        data = open('to_do.json').read()
        self.to_dos = json.loads(data)
        l = self.to_dos.copy()
        ind = 0
        for i in range(len(self.to_dos['to_do'])):
            day, month, year = self.to_dos['to_do'][i]['date'].split('.')
            day, month, year = int(day), int(month), int(year)
            day_r, month_r, year_r = datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year
            if self.to_dos['to_do'][i]['status'] == 'do' and (year < year_r or month < month_r or day < day_r):
                del l['to_do'][ind]
                print('опа')
                ind -= 1
            ind += 1
        self.to_dos = l
        os.remove('to_do.json')
        g = open('to_do.json', mode='w').write(json.dumps(self.to_dos, ensure_ascii=False))
        self.x = 350
        self.y = 288
        data = open('to_do.json').read()
        self.to_dos = json.loads(data)['to_do']

        for i in range(len(self.to_dos)):
            self.arr_to_dos.append(
                [QLabel(self), QLabel(self), QPushButton(self), self.to_dos[i]['status'], self.to_dos[i]['text'],
                 self.to_dos[i]['time'], QLabel(self), self.to_dos[i]['date']])

            self.arr_to_dos[-1][0].setText(self.arr_to_dos[-1][4])
            self.arr_to_dos[-1][0].setStyleSheet('color: rgb(255, 255, 255)')
            self.arr_to_dos[-1][0].resize(1323, 45)
            self.arr_to_dos[-1][0].setFont(self.text_todo.font())
            self.arr_to_dos[-1][0].move(self.x, self.y)
            self.arr_to_dos[-1][0].setCursor(self.text_todo.cursor())

            pix = QPixmap('G:/SecondYearYandexLyceum/Проект PyQt/Дизайн/icons/line.png')
            self.arr_to_dos[-1][6].setPixmap(pix)
            self.arr_to_dos[-1][6].resize(self.arr_to_dos[-1][6].sizeHint())
            self.arr_to_dos[-1][6].move(self.x - 70, self.y + 40)

            self.arr_to_dos[-1][1].setText(self.arr_to_dos[-1][5])
            day, month, year = self.arr_to_dos[-1][7].split('.')
            hour, minute = self.arr_to_dos[-1][5].split(':')
            day, month, year = int(day), int(month), int(year)
            hour, minute = int(hour), int(minute)
            day_r, month_r, year_r, hour_r, minute_r = datetime.datetime.today().day, datetime.datetime.today().month, \
                                                       datetime.datetime.today().year, datetime.datetime.today().hour, datetime.datetime.today().minute
            if (year < year_r or month < month_r or day < day_r or hour < hour_r or (
                    hour == hour_r and minute < minute_r)):
                self.arr_to_dos[-1][1].setStyleSheet('color: rgb(255, 6, 0)')
            else:
                self.arr_to_dos[-1][1].setStyleSheet('color: rgb(7, 133, 250)')

            self.arr_to_dos[-1][1].resize(77, 33)
            self.arr_to_dos[-1][1].setFont(self.time_todo.font())
            self.arr_to_dos[-1][1].move(self.x + 1330, self.y)

            if self.arr_to_dos[-1][3] == 'not_do':
                self.arr_to_dos[-1][2].setIcon(self.not_todo.icon())
            else:
                self.arr_to_dos[-1][2].setIcon(self.todo.icon())
            self.arr_to_dos[-1][2].resize(40, 40)
            self.arr_to_dos[-1][2].setIconSize(self.not_todo.iconSize())
            self.arr_to_dos[-1][2].setCursor(self.not_todo.cursor())
            self.arr_to_dos[-1][2].move(self.x + 1500, self.y + 5)
            self.arr_to_dos[-1][2].clicked.connect(self.change_todo_button)

            self.y += 80

    def change_todo_button(self):
        js = ''
        ind = 0
        for i in range(len(self.arr_to_dos)):
            if self.sender() is self.arr_to_dos[i][2]:
                if self.arr_to_dos[i][3] == 'not_do':
                    self.sender().setIcon(self.todo.icon())
                    self.sender().setIconSize(self.todo.iconSize())
                    js = 'do'
                    ind = i
                    self.arr_to_dos[i][3] = 'do'
                else:
                    self.sender().setIcon(self.not_todo.icon())
                    self.sender().setIconSize(self.not_todo.iconSize())
                    js = 'not_do'
                    ind = i
                    self.arr_to_dos[i][3] = 'not_do'
        data = open('to_do.json').read()
        a = json.loads(data)
        a['to_do'][ind]['status'] = js
        os.remove('to_do.json')
        g = open('to_do.json', mode='w').write(json.dumps(a, ensure_ascii=False))

    def add_todo_f(self):
        time = self.inp_time_todo.text().split(':')
        textt = self.inp_todo.text()
        print(time)
        if time == ['']:
            time = ['23', '59']
        if len(textt) == 0 or time[0].isalpha() or time[1].isalpha() or int(time[0]) > 23 or int(time[0]) < 0 or int(
                time[1]) > 59 or int(
            time[1]) < 0:
            return False
        self.inp_time_todo.setText('')
        self.inp_todo.setText('')
        data = open('to_do.json').read()
        a = json.loads(data)
        date = str(datetime.datetime.today().date()).split('-')
        date = date[2] + '.' + date[1] + '.' + date[0]
        a['to_do'].append({'text': textt, 'time': time[0] + ':' + time[1], 'date': date, 'status': 'not_do'})
        os.remove('to_do.json')
        g = open('to_do.json', mode='w').write(json.dumps(a, ensure_ascii=False))
        self.arr_to_dos.append(
            [QLabel(self), QLabel(self), QPushButton(self), 'not_do', textt,
             time[0] + ':' + time[1], QLabel(self)])

        self.arr_to_dos[-1][0].setText(self.arr_to_dos[-1][4])
        self.arr_to_dos[-1][0].setStyleSheet('color: rgb(255, 255, 255)')
        self.arr_to_dos[-1][0].resize(1323, 45)
        self.arr_to_dos[-1][0].setFont(self.text_todo.font())
        self.arr_to_dos[-1][0].move(self.x, self.y)
        self.arr_to_dos[-1][0].setCursor(self.text_todo.cursor())
        self.arr_to_dos[-1][0].show()

        pix = QPixmap('G:/SecondYearYandexLyceum/Проект PyQt/Дизайн/icons/line.png')
        self.arr_to_dos[-1][6].setPixmap(pix)
        self.arr_to_dos[-1][6].resize(self.arr_to_dos[-1][6].sizeHint())
        self.arr_to_dos[-1][6].move(self.x - 70, self.y + 40)
        self.arr_to_dos[-1][6].show()

        hour, minute = self.arr_to_dos[-1][5].split(':')
        hour, minute = int(hour), int(minute)
        hour_r, minute_r = datetime.datetime.today().hour, datetime.datetime.today().minute
        if hour < hour_r or (hour == hour_r and minute < minute_r):
            self.arr_to_dos[-1][1].setStyleSheet('color: rgb(255, 6, 0)')
        else:
            self.arr_to_dos[-1][1].setStyleSheet('color: rgb(7, 133, 250)')

        self.arr_to_dos[-1][1].setText(self.arr_to_dos[-1][5])
        self.arr_to_dos[-1][1].resize(77, 33)
        self.arr_to_dos[-1][1].setFont(self.time_todo.font())
        self.arr_to_dos[-1][1].move(self.x + 1330, self.y)
        self.arr_to_dos[-1][1].show()

        if self.arr_to_dos[-1][3] == 'not_do':
            self.arr_to_dos[-1][2].setIcon(self.not_todo.icon())
        else:
            self.arr_to_dos[-1][2].setIcon(self.todo.icon())
        self.arr_to_dos[-1][2].resize(40, 40)
        self.arr_to_dos[-1][2].setIconSize(self.not_todo.iconSize())
        self.arr_to_dos[-1][2].setCursor(self.not_todo.cursor())
        self.arr_to_dos[-1][2].move(self.x + 1500, self.y + 5)
        self.arr_to_dos[-1][2].clicked.connect(self.change_todo_button)

        self.arr_to_dos[-1][2].show()
        self.y += 80

        print(len(self.arr_to_dos))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
