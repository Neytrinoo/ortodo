import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QGroupBox, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
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
        self.switch_buy.clicked.connect(self.switch_buy_f)
        self.switch_to_do.clicked.connect(self.switch_to_do_f)

        self.start_programm()

    def start_programm(self):
        self.groupBox_2.resize(1670, 1051)
        self.groupBox_3.resize(0, 0)
        self.text_todo.resize(0, 0)
        self.time_todo.resize(0, 0)
        self.arr_to_dos = []
        self.not_todo.resize(0, 0)
        self.todo.resize(0, 0)
        self.delete_2.resize(0, 0)

        data = open('to_do.json').read()
        self.to_dos = json.loads(data)
        l = json.loads(data)
        all_to_dos = open('all_to_dos.json').read()
        self.all_to_dos = json.loads(all_to_dos)
        ind = 0
        for i in range(len(self.to_dos['to_do'])):
            day, month, year = self.to_dos['to_do'][i]['date'].split('.')
            day, month, year = int(day), int(month), int(year)
            day_r, month_r, year_r = datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year
            if self.to_dos['to_do'][i]['status'] == 'do' and (year < year_r or month < month_r or day < day_r):
                self.all_to_dos['all_to_dos'].append(l['to_do'][ind])
                del l['to_do'][ind]
                print('опа')
                ind -= 1
            ind += 1
        self.to_dos = l
        os.remove('to_do.json')
        os.remove('all_to_dos.json')
        g = open('to_do.json', mode='w').write(json.dumps(self.to_dos, ensure_ascii=False))
        g = open('all_to_dos.json', mode='w').write(json.dumps(self.all_to_dos, ensure_ascii=False))
        self.x = 350
        self.y = 288
        data = open('to_do.json').read()
        self.to_dos = json.loads(data)['to_do']

        for i in range(len(self.to_dos)):
            self.arr_to_dos.append(
                [QLabel(self), QLabel(self), QPushButton(self), self.to_dos[i]['status'], self.to_dos[i]['text'],
                 self.to_dos[i]['time'], QLabel(self), self.to_dos[i]['date'], QPushButton(self)])
            self.show_elem_todo()

    def show_elem_todo(self):  # Функция создает стили и показывает элемент списка дел
        # Стили для текста задачи
        self.arr_to_dos[-1][0].setText(self.arr_to_dos[-1][4])
        self.arr_to_dos[-1][0].setStyleSheet('color: rgb(255, 255, 255)')
        self.arr_to_dos[-1][0].resize(1323, 45)
        self.arr_to_dos[-1][0].setFont(self.text_todo.font())
        self.arr_to_dos[-1][0].move(self.x, self.y)
        self.arr_to_dos[-1][0].setCursor(self.text_todo.cursor())
        self.arr_to_dos[-1][0].show()

        # Стили для линии
        pix = QPixmap('G:/SecondYearYandexLyceum/Проект PyQt/Дизайн/icons/line.png')
        self.arr_to_dos[-1][6].setPixmap(pix)
        self.arr_to_dos[-1][6].resize(self.arr_to_dos[-1][6].sizeHint())
        self.arr_to_dos[-1][6].move(self.x - 70, self.y + 40)
        self.arr_to_dos[-1][6].show()

        # Стили для времени задачи
        self.arr_to_dos[-1][1].setText(self.arr_to_dos[-1][5])
        day, month, year = self.arr_to_dos[-1][7].split('.')
        hour, minute = self.arr_to_dos[-1][5].split(':')
        day, month, year = int(day), int(month), int(year)
        hour, minute = int(hour), int(minute)
        day_r, month_r, year_r, hour_r, minute_r = datetime.datetime.today().day, datetime.datetime.today().month, \
                                                   datetime.datetime.today().year, datetime.datetime.today().hour, datetime.datetime.today().minute
        if (year < year_r or month < month_r or day < day_r or hour < hour_r or (
                hour == hour_r and minute < minute_r)):
            self.arr_to_dos[-1][1].setStyleSheet(
                'color: rgb(255, 6, 0)')  # Проверка, каким цветом делать текст. Если просточено - красным, если нет - синим
        else:
            self.arr_to_dos[-1][1].setStyleSheet('color: rgb(7, 133, 250)')

        self.arr_to_dos[-1][1].resize(77, 33)
        self.arr_to_dos[-1][1].setFont(self.time_todo.font())
        self.arr_to_dos[-1][1].move(self.x + 1330, self.y)
        self.arr_to_dos[-1][1].show()

        # Стили для кнопки "Сделано" или "Не сделано"
        if self.arr_to_dos[-1][3] == 'not_do':
            self.arr_to_dos[-1][2].setIcon(self.not_todo.icon())
        else:
            self.arr_to_dos[-1][2].setIcon(self.todo.icon())
        self.arr_to_dos[-1][2].resize(40, 40)
        self.arr_to_dos[-1][2].setIconSize(self.not_todo.iconSize())
        self.arr_to_dos[-1][2].setCursor(self.not_todo.cursor())
        self.arr_to_dos[-1][2].move(self.x + 1500, self.y)
        self.arr_to_dos[-1][2].clicked.connect(self.change_todo_button)
        self.arr_to_dos[-1][2].show()

        # Стили для кнопки удаления задачи
        self.arr_to_dos[-1][8].setIcon(self.delete_2.icon())
        self.arr_to_dos[-1][8].resize(31, 38)
        self.arr_to_dos[-1][8].setIconSize(self.delete_2.iconSize())
        self.arr_to_dos[-1][8].setCursor(self.delete_2.cursor())
        self.arr_to_dos[-1][8].move(self.x - 60, self.y - 3)
        self.arr_to_dos[-1][8].clicked.connect(self.delete_todo)
        self.arr_to_dos[-1][8].show()

        self.y += 80

    def show_elem_buy(self):  # Функция создает стили и показывает элемент списка покупок
        # Стили для текста покупки
        self.arr_buys[-1][0].setText(self.arr_buys[-1][4])
        self.arr_buys[-1][0].setStyleSheet('color: rgb(255, 255, 255)')
        self.arr_buys[-1][0].resize(1323, 45)
        self.arr_buys[-1][0].setFont(self.text_buy.font())
        self.arr_buys[-1][0].move(self.x, self.y)
        self.arr_buys[-1][0].setCursor(self.text_buy.cursor())
        self.arr_buys[-1][0].show()

        # Стили для линии
        pix = QPixmap('Дизайн/icons/line.png')
        self.arr_buys[-1][6].setPixmap(pix)
        self.arr_buys[-1][6].resize(self.arr_buys[-1][6].sizeHint())
        self.arr_buys[-1][6].move(self.x - 70, self.y + 40)
        self.arr_buys[-1][6].show()

        # Стили для цены
        self.arr_buys[-1][1].setText(self.arr_buys[-1][5])
        self.arr_buys[-1][1].setStyleSheet('color: rgb(7, 133, 250)')
        self.arr_buys[-1][1].resize(111, 33)
        self.arr_buys[-1][1].setFont(self.price_text.font())
        self.arr_buys[-1][1].move(self.x + 1270, self.y)
        self.arr_buys[-1][1].show()

        # Стили для кнопки "Сделано" или "Не сделано"
        if self.arr_buys[-1][3] == 'not_buy':
            self.arr_buys[-1][2].setIcon(self.not_buy.icon())
        else:
            self.arr_buys[-1][2].setIcon(self.buy.icon())
        self.arr_buys[-1][2].resize(40, 40)
        self.arr_buys[-1][2].setIconSize(self.not_buy.iconSize())
        self.arr_buys[-1][2].setCursor(self.not_buy.cursor())
        self.arr_buys[-1][2].move(self.x + 1500, self.y)
        self.arr_buys[-1][2].show()

        # Стили для кнопки удаления покупки
        self.arr_buys[-1][8].setIcon(self.delete_buy.icon())
        self.arr_buys[-1][8].resize(31, 38)
        self.arr_buys[-1][8].setIconSize(self.delete_buy.iconSize())
        self.arr_buys[-1][8].setCursor(self.delete_buy.cursor())
        self.arr_buys[-1][8].move(self.x - 60, self.y - 3)
        self.arr_buys[-1][8].show()

        # Стили для иконки рубля
        pix = QPixmap('Дизайн/icons/Рубль.png')
        self.arr_buys[-1][9].setPixmap(pix)
        self.arr_buys[-1][9].resize(self.arr_buys[-1][9].sizeHint())
        self.arr_buys[-1][9].move(self.x + 1390, self.y)
        self.arr_buys[-1][9].show()

        self.arr_buys[-1][10].setText(self.arr_buys[-1][11])
        self.arr_buys[-1][10].setStyleSheet('color: rgb(7, 133, 250)')
        self.arr_buys[-1][10].resize(51, 31)
        self.arr_buys[-1][10].setFont(self.count.font())
        self.arr_buys[-1][10].move(self.x + 1445, self.y + 10)
        self.arr_buys[-1][10].show()

        self.y += 80

    def clear_buy(self):
        # Функция изменения размера всех элементов ПОКУПОК до нуля
        # Чтобы переключиться на другую вкладку
        self.switch_buy.setIcon(QIcon('Дизайн/icons/Покупки.png'))
        self.groupBox_3.resize(0, 0)
        for i in range(len(self.arr_buys)):
            self.arr_buys[i][0].resize(0, 0)
            self.arr_buys[i][1].resize(0, 0)
            self.arr_buys[i][2].resize(0, 0)
            self.arr_buys[i][6].resize(0, 0)
            self.arr_buys[i][8].resize(0, 0)
            self.arr_buys[i][9].resize(0, 0)
            self.arr_buys[i][10].resize(0, 0)

    def clear_to_dos(self):
        # Функция изменения размера всех элементов СПИСКА ДЕЛ до нуля
        # Для того, чтобы вывести другую вкладку
        self.groupBox_2.resize(0, 0)
        for i in range(len(self.arr_to_dos)):
            self.arr_to_dos[i][0].resize(0, 0)
            self.arr_to_dos[i][1].resize(0, 0)
            self.arr_to_dos[i][2].resize(0, 0)
            self.arr_to_dos[i][6].resize(0, 0)
            self.arr_to_dos[i][8].resize(0, 0)
        self.switch_to_do.setIcon(QIcon('Дизайн/icons/Список дел неактивный.png'))

    def add_buy_f(self):
        # Функция добавления покупки в json файл, проверки правильности ввода
        # И отображение нового элемента на экране с помощью сторонней функции
        try:
            text = self.product_inp.text()
            price = int(self.price_inp.text())
            if len(text) == 0:
                return False

            # Добавление в json файл записи
            self.inp_time_todo.setText('')
            self.inp_todo.setText('')
            data = open('buy.json').read()
            a = json.loads(data)
            date = str(datetime.datetime.today().date()).split('-')
            date = date[2] + '.' + date[1] + '.' + date[0]
            a['buy'].append(
                {'text': text, 'price': str(price), 'date': date, 'status': 'not_buy', 'count': self.count_inp.text()})
            os.remove('buy.json')
            g = open('buy.json', mode='w').write(json.dumps(a, ensure_ascii=False))

            # Добавление элемента в массив и его отображение
            self.arr_buys.append([QLabel(self), QLabel(self), QPushButton(self), 'not_buy', text,
                                  str(price * int(self.count_inp.text())), QLabel(self), date, QPushButton(self),
                                  QLabel(self), QLabel(self),
                                  self.count_inp.text()])

            self.show_elem_buy()
        except Exception as e:
            print(e)
            return False

    def switch_buy_f(self):
        # Функция очистки программы от других вкладок для переключения на вкладку "Покупки"
        # И изменения размеров элементов вкладки "Покупки" до НОРМАЛЬНОГО состояния
        self.clear_to_dos()
        self.switch_buy.setIcon(QIcon('Дизайн/icons/Покупки активные.png'))
        self.groupBox_3.resize(1670, 1051)
        self.text_buy.resize(0, 0)
        self.price_text.resize(0, 0)
        self.not_buy.resize(0, 0)
        self.buy.resize(0, 0)
        self.count.resize(0, 0)
        self.delete_buy.resize(0, 0)
        self.add_buy.clicked.connect(self.add_buy_f)

        data = open('buy.json').read()
        print(data)
        self.buys = json.loads(data)
        l = json.loads(data)
        all_buys = open('all_buys.json').read()
        self.all_buys = json.loads(all_buys)
        ind = 0
        for i in range(len(self.buys['buy'])):
            day, month, year = self.buys['buy'][i]['date'].split('.')
            day, month, year = int(day), int(month), int(year)
            day_r, month_r, year_r = datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year
            if self.buys['buy'][i]['status'] == 'buy' and (year < year_r or month < month_r or day < day_r):
                self.all_buys['all_buys'].append(l['buy'][ind])
                del l['buy'][ind]
                print('опа')
                ind -= 1
            ind += 1
        self.buys = l
        os.remove('buy.json')
        g = open('buy.json', mode='w').write(json.dumps(self.buys, ensure_ascii=False))
        self.x = 350
        self.arr_buys = []
        self.y = 288
        data = open('buy.json').read()
        self.buys = json.loads(data)['buy']
        print(self.buys)
        for i in range(len(self.buys)):
            self.arr_buys.append(
                [QLabel(self), QLabel(self), QPushButton(self), self.buys[i]['status'], self.buys[i]['text'],
                 str(int(self.buys[i]['price']) * int(self.buys[i]['count'])), QLabel(self), self.buys[i]['date'],
                 QPushButton(self), QLabel(self),
                 QLabel(self), self.buys[i]['count']])
            self.show_elem_buy()

    def switch_to_do_f(self):
        # Функция очистки программы от других вкладок для переключения на вкладку "Список дел"
        # И изменение размера всех элементов до НОРМАЛЬНОГО состояния
        self.groupBox_2.resize(1670, 1051)
        self.clear_buy()
        self.switch_to_do.setIcon(QIcon('Дизайн/icons/Список дел.png'))

        for i in range(len(self.arr_to_dos)):
            self.arr_to_dos[i][0].resize(1323, 45)
            self.arr_to_dos[i][1].resize(77, 33)
            self.arr_to_dos[i][2].resize(40, 40)
            self.arr_to_dos[i][6].resize(self.arr_to_dos[i][6].sizeHint())
            self.arr_to_dos[i][8].resize(31, 38)

    def delete_todo(self):
        # Функция для удаления задачи. Она удаляет задачу из json файла.
        # Также передвигает нижние задачи выше.
        result, okBtnPressed = QInputDialog.getItem(self, 'Удаление задачи', 'Вы действительно хотите удалить задачу?',
                                                    ('Да', 'Нет'), 1, False)
        if result == 'Нет' or not okBtnPressed:
            return False
        ind = 0
        for i in range(len(self.arr_to_dos)):
            if self.sender() is self.arr_to_dos[i][8]:  # Перезапись json файла и изменение размера удаленного дела
                data = open('to_do.json').read()
                a = json.loads(data)
                del a['to_do'][i]
                os.remove('to_do.json')
                ind = i
                g = open('to_do.json', mode='w').write(json.dumps(a, ensure_ascii=False))
                self.arr_to_dos[i][0].resize(0, 0)
                self.arr_to_dos[i][1].resize(0, 0)
                self.arr_to_dos[i][2].resize(0, 0)
                self.arr_to_dos[i][6].resize(0, 0)
                self.arr_to_dos[i][8].resize(0, 0)
        del self.arr_to_dos[ind]

        for i in range(ind, len(self.arr_to_dos)):  # Перемещение последующих задач
            self.arr_to_dos[i][0].move(self.arr_to_dos[i][0].x(), self.arr_to_dos[i][0].y() - 80)
            self.arr_to_dos[i][1].move(self.arr_to_dos[i][1].x(), self.arr_to_dos[i][1].y() - 80)
            self.arr_to_dos[i][2].move(self.arr_to_dos[i][2].x(), self.arr_to_dos[i][2].y() - 80)
            self.arr_to_dos[i][6].move(self.arr_to_dos[i][6].x(), self.arr_to_dos[i][6].y() - 80)
            self.arr_to_dos[i][8].move(self.arr_to_dos[i][8].x(), self.arr_to_dos[i][8].y() - 80)

        self.y -= 80

    def change_todo_button(self):
        # Функция для отметки дела как сделанного.
        # Она меняет стиль копки "Сделано" и изменяет json файл.
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
        # Проверка правильности ввода
        time = self.inp_time_todo.text().split(':')
        textt = self.inp_todo.text()
        print(time)
        if time == ['']:
            time = ['23', '59']
        if len(textt) == 0 or len(time) <= 1 or time[0].isalpha() or time[1].isalpha() or int(time[0]) > 23 or int(
                time[0]) < 0 or int(
            time[1]) > 59 or int(
            time[1]) < 0:
            return False

        # Добавление элемента в json файл
        self.inp_time_todo.setText('')
        self.inp_todo.setText('')
        data = open('to_do.json').read()
        a = json.loads(data)
        date = str(datetime.datetime.today().date()).split('-')
        date = date[2] + '.' + date[1] + '.' + date[0]
        a['to_do'].append({'text': textt, 'time': time[0] + ':' + time[1], 'date': date, 'status': 'not_do'})
        os.remove('to_do.json')
        g = open('to_do.json', mode='w').write(json.dumps(a, ensure_ascii=False))

        # Создание элемента
        self.arr_to_dos.append(
            [QLabel(self), QLabel(self), QPushButton(self), 'not_do', textt,
             time[0] + ':' + time[1], QLabel(self), date, QPushButton(self)])

        self.show_elem_todo()

        print(len(self.arr_to_dos))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
