import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QGroupBox, QInputDialog, \
    QVBoxLayout, QColorDialog, QScrollArea, QScrollBar
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image, ImageDraw
from PyQt5.QtCore import Qt
from change_note import Change_note
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
        self.PATH_TO_TODO_JSON = 'to_do.json'
        self.PATH_TO_BUY_JSON = 'buy.json'
        self.PATH_ALL_TODOS_JSON = 'all_to_dos.json'
        self.PATH_ALL_BUYS_JSON = 'all_buys.json'
        self.PATH_TO_LINE_ICON = 'Дизайн/icons/line.png'
        self.PATH_TO_RUBLE_ICON = 'Дизайн/icons/Рубль.png'
        self.PATH_TO_BUYS_NOACTIVE_ICON = 'Дизайн/icons/Покупки.png'
        self.PATH_TO_TODO_NOACTIVE_ICON = 'Дизайн/icons/Список дел неактивный.png'
        self.PATH_TO_BUYS_ACTIVE_ICON = 'Дизайн/icons/Покупки активные.png'
        self.PATH_TO_TODO_ACTIVE_ICON = 'Дизайн/icons/Список дел.png'
        self.PATH_TO_NOACTIVE_PROGRESS_ICON = 'Дизайн/icons/Прогресс.png'
        self.PATH_TO_ACTIVE_PROGRESS_ICON = 'Дизайн/icons/Прогресс активный.png'
        self.PATH_TO_NOACTIVE_ALL_TASKS_ICON = 'Дизайн/icons/Все дела неактивное.png'
        self.PATH_TO_ACTIVE_ALL_TASKS_ICON = 'Дизайн/icons/Все дела активное.png'
        self.PATH_TO_NOACTIVE_NOTES_ICON = 'Дизайн/icons/Заметки неактивные.png'
        self.PATH_TO_ACTIVE_NOTES_ICON = 'Дизайн/icons/Заметки активные.png'
        self.PATH_TO_NOTES_JSON = 'notes.json'
        self.PATH_TO_CHOICE_NOTE_COLOR_ICON = 'Дизайн/icons/выбор цвета.png'
        self.PATH_TO_ACTIVE_ALL_BUYS_ICON = 'Дизайн/icons/все покупки активные.png'
        self.PATH_TO_NOACTIVE_ALL_BUYS_ICON = 'Дизайн/icons/все покупки неактивные.png'
        self.PATH_TO_ALL_BUYS_JSON = 'all_buys.json'

        self.arr_buys = []
        self.all_tasks_scroll = QScrollArea(self)
        self.add_todo.clicked.connect(self.add_todo_f)
        self.switch_buy.clicked.connect(self.switch_buy_f)
        self.switch_to_do.clicked.connect(self.switch_to_do_f)
        self.switch_progress.clicked.connect(self.switch_progress_f)
        self.switch_all_tasks.clicked.connect(self.switch_all_tasks_f)
        self.switch_notes.clicked.connect(self.switch_notes_f)
        self.choice_color_btn.clicked.connect(self.set_color_show)
        self.switch_all_buys.clicked.connect(self.switch_all_buys_f)

        data = open(self.PATH_TO_NOTES_JSON).read()
        js_f = json.loads(data)
        if len(js_f['notes']) > 0:
            self.last_note_id = int(js_f['notes'][-1]['id'])
        else:
            self.last_note_id = 0
        self.start_programm()

    def start_programm(self):
        self.groupBox_2.resize(1670, 1051)
        self.groupBox_3.resize(0, 0)
        self.text_todo.resize(0, 0)
        self.time_todo.resize(0, 0)
        self.arr_to_dos = []
        self.not_todo.resize(0, 0)
        self.todo.resize(0, 0)
        self.clear_all_buys()
        self.delete_2.resize(0, 0)
        self.clear_progress()
        self.clear_all_tasks()
        self.clear_notes()

        data = open(self.PATH_TO_TODO_JSON).read()
        self.to_dos = json.loads(data)
        l = json.loads(data)
        all_to_dos = open(self.PATH_ALL_TODOS_JSON).read()
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
        os.remove(self.PATH_TO_TODO_JSON)
        os.remove(self.PATH_ALL_TODOS_JSON)
        g = open(self.PATH_TO_TODO_JSON, mode='w').write(json.dumps(self.to_dos, ensure_ascii=False))
        g = open(self.PATH_ALL_TODOS_JSON, mode='w').write(json.dumps(self.all_to_dos, ensure_ascii=False))

        self.scroll_tasks = QScrollArea(self.groupBox_2)
        self.tasks_gb = QGroupBox(self.groupBox_2)
        self.len_scroll_task = 810
        if len(self.to_dos['to_do']) * 80 + 80 >= self.len_scroll_task:
            self.tasks_gb.resize(1671, len(self.to_dos['to_do']) * 80 + 80)
        else:
            self.tasks_gb.resize(1671, self.len_scroll_task)

        self.scroll_tasks.setWidget(self.tasks_gb)
        self.scroll_tasks.resize(1635, 805)
        self.scroll_tasks.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_tasks.move(0, 200)
        self.scroll_tasks.show()
        self.tasks_gb.show()

        self.x = 70
        self.y = 20
        data = open(self.PATH_TO_TODO_JSON).read()
        self.to_dos = json.loads(data)['to_do']

        for i in range(len(self.to_dos)):
            self.arr_to_dos.append(
                [QLabel(self.tasks_gb), QLabel(self.tasks_gb), QPushButton(self.tasks_gb),
                 self.to_dos[i]['status'], self.to_dos[i]['text'],
                 self.to_dos[i]['time'], QLabel(self.tasks_gb), self.to_dos[i]['date'], QPushButton(self.tasks_gb)])
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
        pix = QPixmap(self.PATH_TO_LINE_ICON)
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
        self.arr_buys[-1][0].resize(1200, 45)
        self.arr_buys[-1][0].setFont(self.text_buy.font())
        self.arr_buys[-1][0].move(self.x, self.y)
        self.arr_buys[-1][0].setCursor(self.text_buy.cursor())
        self.arr_buys[-1][0].show()

        # Стили для линии
        pix = QPixmap(self.PATH_TO_LINE_ICON)
        self.arr_buys[-1][6].setPixmap(pix)
        self.arr_buys[-1][6].resize(self.arr_buys[-1][6].sizeHint())
        self.arr_buys[-1][6].move(self.x - 70, self.y + 40)
        self.arr_buys[-1][6].show()

        # Стили для цены
        self.arr_buys[-1][1].setText(self.arr_buys[-1][5])
        self.arr_buys[-1][1].setStyleSheet('color: rgb(7, 133, 250)')
        self.arr_buys[-1][1].resize(121, 33)
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
        self.arr_buys[-1][2].clicked.connect(self.change_buy_not_buy_button)
        self.arr_buys[-1][2].show()

        # Стили для кнопки удаления покупки
        self.arr_buys[-1][8].setIcon(self.delete_buy.icon())
        self.arr_buys[-1][8].resize(31, 38)
        self.arr_buys[-1][8].setIconSize(self.delete_buy.iconSize())
        self.arr_buys[-1][8].setCursor(self.delete_buy.cursor())
        self.arr_buys[-1][8].move(self.x - 60, self.y - 3)
        self.arr_buys[-1][8].clicked.connect(self.delete_buy_f)
        self.arr_buys[-1][8].show()

        # Стили для иконки рубля
        pix = QPixmap(self.PATH_TO_RUBLE_ICON)
        self.arr_buys[-1][9].setPixmap(pix)
        self.arr_buys[-1][9].resize(self.arr_buys[-1][9].sizeHint())
        self.arr_buys[-1][9].move(self.x + 1390, self.y)
        self.arr_buys[-1][9].show()

        # Для цены за один x количество
        self.arr_buys[-1][11].setText(
            str(int(self.arr_buys[-1][5]) // int(self.arr_buys[-1][10])) + ' x ' + self.arr_buys[-1][10] + ' =')
        self.arr_buys[-1][11].setStyleSheet('color: rgb(7, 133, 250)')
        self.arr_buys[-1][11].setFont(self.price_for_one.font())
        self.arr_buys[-1][11].resize(self.arr_buys[-1][11].sizeHint())
        self.arr_buys[-1][11].move(self.x + 1260 - self.arr_buys[-1][11].size().width(), self.y + 10)
        self.arr_buys[-1][11].show()

        if self.arr_buys[-1][3] == 'buy':
            self.already_pay.setText(str(int(self.already_pay.text()) + int(self.arr_buys[-1][5])))
        self.itogo_price.setText(str(int(self.itogo_price.text()) + int(self.arr_buys[-1][5])))
        self.y += 80

    def clear_buy(self):
        # Функция изменения размера всех элементов ПОКУПОК до нуля
        # Чтобы переключиться на другую вкладку
        self.switch_buy.setIcon(QIcon(self.PATH_TO_BUYS_NOACTIVE_ICON))
        self.groupBox_3.resize(0, 0)

    def clear_to_dos(self):
        # Функция изменения размера всех элементов СПИСКА ДЕЛ до нуля
        # Для того, чтобы вывести другую вкладку
        self.groupBox_2.resize(0, 0)
        self.switch_to_do.setIcon(QIcon(self.PATH_TO_TODO_NOACTIVE_ICON))

    def delete_buy_f(self):
        # Функция для удаления задачи. Она удаляет задачу из json файла.
        # Также передвигает нижние задачи выше.
        result, okBtnPressed = QInputDialog.getItem(self, 'Удаление покупки',
                                                    'Вы действительно хотите удалить покупку?',
                                                    ('Да', 'Нет'), 0, False)
        if result == 'Нет' or not okBtnPressed:
            return False
        ind = 0
        for i in range(len(self.arr_buys)):
            if self.sender() is self.arr_buys[i][8]:  # Перезапись json файла и изменение размера удаленного дела
                if self.groupBox_3.size().height() != 0:
                    path = self.PATH_TO_BUY_JSON
                else:
                    path = self.PATH_TO_ALL_BUYS_JSON
                    self.itogo_price_all.setText(str(int(self.itogo_price_all.text()) - int(self.arr_buys[i][5])))
                data = open(path).read()
                if self.arr_buys[i][3] == 'buy':
                    self.already_pay.setText(str(int(self.already_pay.text()) - int(self.arr_buys[i][5])))
                a = json.loads(data)
                self.itogo_price.setText(str(int(self.itogo_price.text()) - int(self.arr_buys[i][5])))
                if path == self.PATH_TO_BUY_JSON:
                    del a['buy'][i]
                else:
                    del a['all_buys'][i]
                os.remove(path)
                ind = i
                g = open(path, mode='w').write(json.dumps(a, ensure_ascii=False))
                self.arr_buys[i][0].resize(0, 0)
                self.arr_buys[i][1].resize(0, 0)
                self.arr_buys[i][2].resize(0, 0)
                self.arr_buys[i][6].resize(0, 0)
                self.arr_buys[i][8].resize(0, 0)
                self.arr_buys[i][9].resize(0, 0)
                self.arr_buys[i][11].resize(0, 0)
        del self.arr_buys[ind]

        for i in range(ind, len(self.arr_buys)):  # Перемещение последующих покупок выше
            self.arr_buys[i][0].move(self.arr_buys[i][0].x(), self.arr_buys[i][0].y() - 80)
            self.arr_buys[i][1].move(self.arr_buys[i][1].x(), self.arr_buys[i][1].y() - 80)
            self.arr_buys[i][2].move(self.arr_buys[i][2].x(), self.arr_buys[i][2].y() - 80)
            self.arr_buys[i][6].move(self.arr_buys[i][6].x(), self.arr_buys[i][6].y() - 80)
            self.arr_buys[i][8].move(self.arr_buys[i][8].x(), self.arr_buys[i][8].y() - 80)
            self.arr_buys[i][9].move(self.arr_buys[i][9].x(), self.arr_buys[i][9].y() - 80)
            self.arr_buys[i][11].move(self.arr_buys[i][11].x(), self.arr_buys[i][11].y() - 80)
        if path == self.PATH_TO_BUY_JSON:
            if self.buys_gb.size().height() - 80 > self.len_scroll_buy:
                self.buys_gb.resize(1630, self.buys_gb.size().height() - 80)
            else:
                self.buys_gb.resize(1630, self.len_scroll_buy)
        else:
            if self.all_buys_gb.size().height() - 80 > self.len_scroll_all_buy:
                self.all_buys_gb.resize(1631, self.all_buys_gb.size().height() - 80)
            else:
                self.all_buys_gb.resize(1631, self.len_scroll_all_buy)
        self.y -= 80

    def change_buy_not_buy_button(self):
        js = ''
        ind = 0
        for i in range(len(self.arr_buys)):
            if self.sender() is self.arr_buys[i][2]:
                if self.arr_buys[i][3] == 'not_buy':
                    self.sender().setIcon(self.buy.icon())
                    self.sender().setIconSize(self.buy.iconSize())
                    self.already_pay.setText(str(int(self.already_pay.text()) + int(self.arr_buys[i][5])))
                    js = 'buy'
                    ind = i
                    self.arr_buys[i][3] = 'buy'
                    break
                else:
                    self.sender().setIcon(self.not_buy.icon())
                    self.sender().setIconSize(self.not_buy.iconSize())
                    self.already_pay.setText(str(int(self.already_pay.text()) - int(self.arr_buys[i][5])))
                    js = 'not_buy'
                    ind = i
                    self.arr_buys[i][3] = 'not_buy'
                    break
        if self.groupBox_3.size().height() != 0:
            path_js = self.PATH_TO_BUY_JSON
        else:
            path_js = self.PATH_TO_ALL_BUYS_JSON
            self.itogo_price_all.setText(str(int(self.itogo_price_all.text()) - int(self.arr_buys[ind][5])))
        data = open(path_js).read()
        a = json.loads(data)
        if path_js == self.PATH_TO_BUY_JSON:
            a['buy'][ind]['status'] = js
        else:
            a['all_buys'][ind]['status'] = js
        os.remove(path_js)
        g = open(path_js, mode='w').write(json.dumps(a, ensure_ascii=False))

    def add_buy_f(self):
        # Функция добавления покупки в json файл, проверки правильности ввода
        # И отображение нового элемента на экране с помощью сторонней функции
        try:
            text = self.product_inp.text()
            price = int(self.price_inp.text())
            if len(text) == 0:
                return False

            # Добавление в json файл записи
            self.product_inp.setText('')
            self.price_inp.setText('')
            data = open(self.PATH_TO_BUY_JSON).read()
            a = json.loads(data)
            date = str(datetime.datetime.today().date()).split('-')
            date = date[2] + '.' + date[1] + '.' + date[0]
            a['buy'].append(
                {'text': text, 'price': str(price), 'date': date, 'status': 'not_buy', 'count': self.count_inp.text()})
            os.remove(self.PATH_TO_BUY_JSON)
            g = open(self.PATH_TO_BUY_JSON, mode='w').write(json.dumps(a, ensure_ascii=False))

            # Добавление элемента в массив и его отображение
            self.arr_buys.append(
                [QLabel(self.buys_gb), QLabel(self.buys_gb), QPushButton(self.buys_gb), 'not_buy', text,
                 str(price * int(self.count_inp.text())), QLabel(self.buys_gb), date, QPushButton(self.buys_gb),
                 QLabel(self.buys_gb),
                 self.count_inp.text(), QLabel(self.buys_gb)])
            if len(self.arr_buys) * 80 >= self.len_scroll_buy:
                self.buys_gb.resize(1630, len(self.arr_buys) * 80 + 80)

            self.show_elem_buy()
        except Exception as e:
            print(e)
            return False

    def switch_buy_f(self):
        # Функция очистки программы от других вкладок для переключения на вкладку "Покупки"
        # И изменения размеров элементов вкладки "Покупки" до НОРМАЛЬНОГО состояния
        self.clear_to_dos()
        self.clear_progress()
        self.clear_notes()
        self.clear_all_tasks()
        self.clear_all_buys()
        self.y = 288
        self.switch_buy.setIcon(QIcon(self.PATH_TO_BUYS_ACTIVE_ICON))
        self.groupBox_3.resize(1670, 1071)
        self.text_buy.resize(0, 0)
        self.price_text.resize(0, 0)
        self.not_buy.resize(0, 0)
        self.buy.resize(0, 0)
        self.count.resize(0, 0)
        self.delete_buy.resize(0, 0)
        self.price_for_one.resize(0, 0)
        self.already_pay.setStyleSheet('color: rgb(7, 133, 250)')
        self.already_pay.setText('0')
        self.itogo_price.setStyleSheet('color: rgb(7, 133, 250)')
        self.itogo_price.setText('0')
        self.add_buy.clicked.connect(self.add_buy_f)

        pix = QPixmap(self.PATH_TO_RUBLE_ICON)
        self.itogo_icon.setPixmap(pix)
        self.already_pay_icon.setPixmap(pix)
        self.itogo_icon.resize(self.itogo_icon.sizeHint())
        self.already_pay_icon.resize(self.itogo_icon.sizeHint())

        # Проверка выполненных покупок за предыдущие дни
        data = open(self.PATH_TO_BUY_JSON).read()
        self.buys = json.loads(data)
        l = json.loads(data)
        all_buys = open(self.PATH_ALL_BUYS_JSON).read()
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
        os.remove(self.PATH_TO_BUY_JSON)
        os.remove(self.PATH_ALL_BUYS_JSON)
        g = open(self.PATH_TO_BUY_JSON, mode='w').write(json.dumps(self.buys, ensure_ascii=False))
        g = open(self.PATH_ALL_BUYS_JSON, mode='w').write(json.dumps(self.all_buys, ensure_ascii=False))

        self.len_scroll_buy = 690

        self.scroll_buys = QScrollArea(self.groupBox_3)
        self.buys_gb = QGroupBox(self.groupBox_3)

        self.scroll_buys.setWidget(self.buys_gb)
        self.scroll_buys.resize(1630, self.len_scroll_buy + 2)
        self.scroll_buys.move(0, 200)
        self.scroll_buys.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_buys.show()
        self.buys_gb.show()
        self.y = 20

        self.x = 70
        self.arr_buys = []

        data = open(self.PATH_TO_BUY_JSON).read()
        self.buys = json.loads(data)['buy']
        print(self.buys)
        for i in range(len(self.buys)):
            self.arr_buys.append(
                [QLabel(self.buys_gb), QLabel(self.buys_gb), QPushButton(self.buys_gb), self.buys[i]['status'],
                 self.buys[i]['text'],
                 str(int(self.buys[i]['price']) * int(self.buys[i]['count'])), QLabel(self.buys_gb),
                 self.buys[i]['date'],
                 QPushButton(self.buys_gb), QLabel(self.buys_gb), self.buys[i]['count'], QLabel(self.buys_gb)])
            self.show_elem_buy()

        if len(self.buys) * 80 + 80 > self.len_scroll_buy:
            self.buys_gb.resize(1630, len(self.buys) * 80 + 80)
        else:
            self.buys_gb.resize(1630, self.len_scroll_buy)

    def switch_to_do_f(self):
        # Функция очистки программы от других вкладок для переключения на вкладку "Список дел"
        # И изменение размера всех элементов до НОРМАЛЬНОГО состояния

        self.groupBox_2.resize(1670, 1071)
        self.y = 288
        self.clear_buy()
        self.clear_all_buys()
        self.clear_progress()
        self.clear_all_tasks()
        self.clear_notes()
        self.switch_to_do.setIcon(QIcon(self.PATH_TO_TODO_ACTIVE_ICON))
        self.start_programm()

    def delete_todo(self):
        # Функция для удаления задачи. Она удаляет задачу из json файла.
        # Также передвигает нижние задачи выше.
        result, okBtnPressed = QInputDialog.getItem(self, 'Удаление задачи', 'Вы действительно хотите удалить задачу?',
                                                    ('Да', 'Нет'), 0, False)
        if result == 'Нет' or not okBtnPressed:
            return False
        ind = 0
        for i in range(len(self.arr_to_dos)):
            if self.sender() is self.arr_to_dos[i][8]:  # Перезапись json файла и изменение размера удаленного дела
                if self.groupBox_2.size().height() != 0:
                    path_js = self.PATH_TO_TODO_JSON
                    tasks = True
                else:
                    tasks = False
                    path_js = self.PATH_ALL_TODOS_JSON
                data = open(path_js).read()
                a = json.loads(data)
                if tasks:
                    del a['to_do'][i]
                else:
                    del a['all_to_dos'][i]
                os.remove(path_js)
                ind = i
                g = open(path_js, mode='w').write(json.dumps(a, ensure_ascii=False))
                self.arr_to_dos[i][0].resize(0, 0)
                self.arr_to_dos[i][1].resize(0, 0)
                self.arr_to_dos[i][2].resize(0, 0)
                self.arr_to_dos[i][6].resize(0, 0)
                self.arr_to_dos[i][8].resize(0, 0)
                break
        del self.arr_to_dos[ind]

        for i in range(ind, len(self.arr_to_dos)):  # Перемещение последующих задач
            self.arr_to_dos[i][0].move(self.arr_to_dos[i][0].x(), self.arr_to_dos[i][0].y() - 80)
            self.arr_to_dos[i][1].move(self.arr_to_dos[i][1].x(), self.arr_to_dos[i][1].y() - 80)
            self.arr_to_dos[i][2].move(self.arr_to_dos[i][2].x(), self.arr_to_dos[i][2].y() - 80)
            self.arr_to_dos[i][6].move(self.arr_to_dos[i][6].x(), self.arr_to_dos[i][6].y() - 80)
            self.arr_to_dos[i][8].move(self.arr_to_dos[i][8].x(), self.arr_to_dos[i][8].y() - 80)
        if not tasks:
            self.clear_all_tasks()
            self.switch_all_tasks_f()

        if tasks:
            if self.tasks_gb.size().height() - 80 >= self.len_scroll_task:
                self.tasks_gb.resize(1671, self.tasks_gb.size().height() - 80)
            else:
                self.tasks_gb.resize(1671, self.len_scroll_task)
        else:
            if self.all_tasks_gb.size().height() - 80 >= 1041:
                self.all_tasks_gb.resize(1631, self.all_tasks_gb.size().height() - 80)
            else:
                self.all_tasks_gb.resize(1631, 1041)
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
                    break
                else:
                    self.sender().setIcon(self.not_todo.icon())
                    self.sender().setIconSize(self.not_todo.iconSize())
                    js = 'not_do'
                    ind = i
                    self.arr_to_dos[i][3] = 'not_do'
                    break
        if self.groupBox_2.size().height() != 0:
            data = open(self.PATH_TO_TODO_JSON).read()
            a = json.loads(data)
            a['to_do'][ind]['status'] = js
            os.remove(self.PATH_TO_TODO_JSON)
            g = open(self.PATH_TO_TODO_JSON, mode='w').write(json.dumps(a, ensure_ascii=False))
        else:
            data = open(self.PATH_ALL_TODOS_JSON).read()
            a = json.loads(data)
            a['all_to_dos'][ind]['status'] = js
            os.remove(self.PATH_ALL_TODOS_JSON)
            g = open(self.PATH_ALL_TODOS_JSON, mode='w').write(json.dumps(a, ensure_ascii=False))

    def clear_progress(self):
        # Очистка вкладки "Прогресс" для переключения на другие вкладки
        self.groupBox_4.resize(0, 0)
        self.switch_progress.setIcon(QIcon(self.PATH_TO_NOACTIVE_PROGRESS_ICON))

    def switch_progress_f(self):
        self.groupBox_4.resize(1670, 1071)
        self.switch_progress.setIcon(QIcon(self.PATH_TO_ACTIVE_PROGRESS_ICON))
        self.clear_buy()
        self.clear_to_dos()
        self.clear_all_buys()
        self.clear_all_tasks()
        self.clear_notes()
        # Вывод потраченных сумм по дням
        self.already_buys = json.loads(open(self.PATH_ALL_BUYS_JSON).read())
        sort_for_date = sorted(self.already_buys['all_buys'], key=lambda x: (
            x['date'].split('.')[2], x['date'].split('.')[1], x['date'].split('.')[0]))
        prices = {}
        for elem in sort_for_date:
            if elem['date'] in prices:
                prices[elem['date']] += int(elem['price'])
            else:
                prices[elem['date']] = int(elem['price'])
        prices = [j for i, j in prices.items()]
        self.graphicsBuys.clear()
        self.graphicsBuys.plot([i for i in range(len(prices))],
                               [price for price in prices], pen='r')

        # Вывод количества сделанных дел по дням
        self.already_done = json.loads(open(self.PATH_ALL_TODOS_JSON).read())
        sort_for_date = sorted(self.already_done['all_to_dos'], key=lambda x: (
            x['date'].split('.')[2], x['date'].split('.')[1], x['date'].split('.')[0]))
        dones = {}
        for elem in sort_for_date:
            if elem['date'] in dones:
                dones[elem['date']] += 1
            else:
                dones[elem['date']] = 1
        dones = [j for i, j in dones.items()]
        self.graphicsView.clear()
        self.graphicsView.plot([i for i in range(len(dones))],
                               [count for count in dones], pen='r')

    def clear_all_tasks(self):
        # Функция для изменения размера всех элементов вкладки "Все дела"
        self.all_tasks_scroll.resize(0, 0)
        for i in range(len(self.arr_to_dos)):
            self.arr_to_dos[i][0].resize(0, 0)
            self.arr_to_dos[i][1].resize(0, 0)
            self.arr_to_dos[i][2].resize(0, 0)
            self.arr_to_dos[i][6].resize(0, 0)
            self.arr_to_dos[i][8].resize(0, 0)
        self.switch_all_tasks.setIcon(QIcon(self.PATH_TO_NOACTIVE_ALL_TASKS_ICON))

    def switch_all_tasks_f(self):
        # Функция очистки пространства для переключения на вкладку "Все дела"
        self.clear_progress()
        self.clear_to_dos()
        self.clear_buy()
        self.clear_all_buys()
        self.clear_notes()
        self.switch_all_tasks.setIcon(QIcon(self.PATH_TO_ACTIVE_ALL_TASKS_ICON))
        self.arr_to_dos = []
        data = open(self.PATH_ALL_TODOS_JSON).read()
        self.to_dos = json.loads(data)['all_to_dos']
        self.y = 80

        self.all_tasks_scroll.resize(1631, 1041)

        self.all_tasks_gb = QGroupBox(self)
        self.all_tasks_gb.resize(1671, len(self.to_dos) * 90)
        self.all_tasks_scroll.move(280, -2)
        self.labels_date = [QLabel(self.all_tasks_gb)]
        self.labels_date[0].setText(self.to_dos[0]['date'])
        self.labels_date[0].setStyleSheet('color: rgb(7, 133, 250)')
        self.labels_date[0].setFont(self.text_todo.font())
        self.labels_date[0].resize(self.labels_date[0].sizeHint())
        self.labels_date[0].move(self.x - 50, self.y - 30)
        self.labels_date[0].show()
        self.now_date = self.to_dos[0]['date']

        for i in range(len(self.to_dos)):
            self.arr_to_dos.append(
                [QLabel(self.all_tasks_gb), QLabel(self.all_tasks_gb), QPushButton(self.all_tasks_gb),
                 self.to_dos[i]['status'], self.to_dos[i]['text'],
                 self.to_dos[i]['time'], QLabel(self.all_tasks_gb), self.to_dos[i]['date'],
                 QPushButton(self.all_tasks_gb)])
            if self.now_date != self.to_dos[i]['date']:
                self.now_date = self.to_dos[i]['date']
                self.labels_date.append(QLabel(self.all_tasks_gb))
                self.labels_date[-1].setText(self.to_dos[i]['date'])
                self.labels_date[-1].setStyleSheet('color: rgb(7, 133, 250)')
                self.labels_date[-1].setFont(self.text_todo.font())
                self.labels_date[-1].resize(self.labels_date[0].sizeHint())
                self.labels_date[-1].move(self.x - 50, self.y)
                self.labels_date[-1].show()
                self.y += 40

            self.show_elem_todo()
        self.all_tasks_scroll.setWidget(self.all_tasks_gb)
        self.all_tasks_gb.resize(1671, len(self.to_dos) * 90 + len(self.labels_date) * 50)
        self.all_tasks_gb.show()
        self.all_tasks_scroll.show()
        print(self.all_tasks_gb.size())

    def clear_notes(self):
        self.groupBox_5.resize(0, 0)
        self.switch_notes.setIcon(QIcon(self.PATH_TO_NOACTIVE_NOTES_ICON))

    def set_color_show(self):
        # Функция для показа или убирания GroupBox'а с выбором цвета для заметки
        if self.choice_color_status:
            self.choice_color.resize(0, 0)
            self.choice_color_status = False
        else:
            self.choice_color_status = True
            self.choice_color.resize(60, 210)
            self.choice_color.show()

        print(self.choice_color.size())

    def yourself_choice_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            image = Image.new('RGBA', (35, 35))
            draw = ImageDraw.Draw(image)

            # Сбрасывание выбора других цветов
            self.red.setAutoExclusive(False)
            self.red.setChecked(False)
            self.blue.setAutoExclusive(False)
            self.blue.setChecked(False)
            self.pink.setAutoExclusive(False)
            self.pink.setChecked(False)

            self.notes_color = color.getRgb()
            draw.ellipse((0, 0, 35, 35), fill=color.getRgb())
            image.save('ellipse.png')
            print(color.getRgb())
            self.choice_color_btn.setIcon(QIcon('ellipse.png'))

    def show_elem_notes(self):
        # Функция для отображения элементов заметок
        # Стили для иконки цвета заметки
        image = Image.new('RGBA', (35, 35))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 35, 35), fill=self.arr_notes[-1][5])
        image.save('ellipse.png')
        pix = QPixmap('ellipse.png')
        self.arr_notes[-1][0].setPixmap(pix)
        self.arr_notes[-1][0].resize(35, 35)
        self.arr_notes[-1][0].move(self.x - 45, self.y)
        self.arr_notes[-1][0].show()

        # Стили для текста заметки
        self.arr_notes[-1][1].setStyleSheet('color: rgb(255, 255, 255)')
        self.arr_notes[-1][1].setText(self.arr_notes[-1][4])
        self.arr_notes[-1][1].resize(1200, 45)
        self.arr_notes[-1][1].setFont(self.text_todo.font())
        self.arr_notes[-1][1].move(self.x + 70, self.y - 4)
        self.arr_notes[-1][1].setCursor(self.text_todo.cursor())
        self.arr_notes[-1][1].show()

        # Стили для кнопки удаления заметки
        self.arr_notes[-1][2].setIcon(self.delete_buy.icon())
        self.arr_notes[-1][2].resize(31, 38)
        self.arr_notes[-1][2].setIconSize(self.delete_buy.iconSize())
        self.arr_notes[-1][2].setCursor(self.delete_buy.cursor())
        self.arr_notes[-1][2].move(self.x + 1470, self.y - 3)
        self.arr_notes[-1][2].clicked.connect(self.delete_notes)
        self.arr_notes[-1][2].show()

        # Стили для линии
        pix = QPixmap(self.PATH_TO_LINE_ICON)
        self.arr_notes[-1][3].setPixmap(pix)
        self.arr_notes[-1][3].resize(self.arr_notes[-1][3].sizeHint())
        self.arr_notes[-1][3].move(self.x - 68, self.y + 40)
        self.arr_notes[-1][3].show()

        # Стили для кнопки "Редактировать"
        self.arr_notes[-1][7].setStyleSheet('color: rgb(255, 255, 255)')
        self.arr_notes[-1][7].resize(121, 41)
        self.arr_notes[-1][7].setCursor(self.change_note.cursor())
        self.arr_notes[-1][7].setFont(self.change_note.font())
        self.arr_notes[-1][7].move(self.x + 1300, self.y - 4)
        self.arr_notes[-1][7].clicked.connect(self.change_note_f)
        self.arr_notes[-1][7].show()
        self.y += 80

    def change_open_note(self):
        if self.change_note_window.note_text.toPlainText() == '':
            self.change_note_window.close()
            return False
        print(self.change_note_window.note_text.toPlainText())
        data = json.loads(open(self.PATH_TO_NOTES_JSON).read())

        if self.change_note_window.red.isChecked():
            self.change_note_window.notes_color = (255, 0, 0, 255)
        elif self.change_note_window.blue.isChecked():
            self.change_note_window.notes_color = (0, 0, 255, 255)
        elif self.change_note_window.pink.isChecked():
            self.change_note_window.notes_color = (255, 0, 246, 255)
        r, g, b, a = list(map(str, list(self.change_note_window.notes_color)))
        for i in range(len(data['notes'])):
            if data['notes'][i]['id'] == self.change_note_window.note_id:
                self.arr_notes[i][1].setText(self.change_note_window.note_text.toPlainText())
                self.arr_notes[i][5] = self.change_note_window.notes_color
                data['notes'][i]['text'] = self.change_note_window.note_text.toPlainText()
                data['notes'][i]['r'] = r
                data['notes'][i]['g'] = g
                data['notes'][i]['b'] = b
                data['notes'][i]['a'] = a

                image = Image.new('RGBA', (35, 35))
                draw = ImageDraw.Draw(image)
                draw.ellipse((0, 0, 35, 35), fill=self.change_note_window.notes_color)
                image.save('ellipse.png')
                pix = QPixmap('ellipse.png')
                self.arr_notes[i][0].setPixmap(pix)
                break
        os.remove(self.PATH_TO_NOTES_JSON)
        g = open(self.PATH_TO_NOTES_JSON, mode='w').write(json.dumps(data, ensure_ascii=False))

        self.change_note_window.close()

    def close_open_note(self):
        self.change_note_window.close()

    def change_note_f(self):
        # Функция для вызова окна редактирования заметки
        for i in range(len(self.arr_notes)):
            if self.sender() is self.arr_notes[i][7]:
                id = str(self.arr_notes[i][6])
                color = self.arr_notes[i][5]
                break
        self.change_note_window = Change_note(id, self, color)
        self.change_note_window.ok_btn.clicked.connect(self.change_open_note)
        self.change_note_window.cancel_btn.clicked.connect(self.close_open_note)
        self.change_note_window.show()

    def delete_notes(self):
        result, okBtnPressed = QInputDialog.getItem(self, 'Удаление заметки',
                                                    'Вы действительно хотите удалить заметку?',
                                                    ('Да', 'Нет'), 0, False)
        if result == 'Нет' or not okBtnPressed:
            return False
        ind = 0
        for i in range(len(self.arr_notes)):
            if self.sender() is self.arr_notes[i][2]:  # Перезапись json файла и изменение размера удаленного дела
                data = open(self.PATH_TO_NOTES_JSON).read()
                a = json.loads(data)
                del a['notes'][i]
                os.remove(self.PATH_TO_NOTES_JSON)
                ind = i
                g = open(self.PATH_TO_NOTES_JSON, mode='w').write(json.dumps(a, ensure_ascii=False))
                self.arr_notes[i][0].resize(0, 0)
                self.arr_notes[i][1].resize(0, 0)
                self.arr_notes[i][2].resize(0, 0)
                self.arr_notes[i][3].resize(0, 0)
                self.arr_notes[i][7].resize(0, 0)
                break
        del self.arr_notes[ind]

        for i in range(ind, len(self.arr_notes)):  # Перемещение последующих задач
            self.arr_notes[i][0].move(self.arr_notes[i][0].x(), self.arr_notes[i][0].y() - 80)
            self.arr_notes[i][1].move(self.arr_notes[i][1].x(), self.arr_notes[i][1].y() - 80)
            self.arr_notes[i][2].move(self.arr_notes[i][2].x(), self.arr_notes[i][2].y() - 80)
            self.arr_notes[i][3].move(self.arr_notes[i][3].x(), self.arr_notes[i][3].y() - 80)
            self.arr_notes[i][7].move(self.arr_notes[i][7].x(), self.arr_notes[i][7].y() - 80)
        if self.notes_gb.size().height() - 90 >= 580:
            self.notes_gb.resize(1671, self.notes_gb.size().height() - 90)
        else:
            self.notes_gb.resize(1671, 580)
        self.y -= 80

    def add_note_f(self):
        # Функция для добавления заметки в json файл и вывод заметки на экран
        if self.text_note.toPlainText() == '':
            return False

        if (len(self.arr_notes) + 1) * 90 + 90 >= 580:
            self.notes_gb.resize(1671, self.notes_gb.size().height() + 90)

        if self.red.isChecked():
            self.notes_color = (255, 0, 0, 255)
        elif self.blue.isChecked():
            self.notes_color = (0, 0, 255, 255)
        elif self.pink.isChecked():
            self.notes_color = (255, 0, 246, 255)
        self.arr_notes.append(
            [QLabel(self.notes_gb), QLabel(self.notes_gb), QPushButton(self.notes_gb), QLabel(self.notes_gb),
             self.text_note.toPlainText(),
             self.notes_color, str(self.last_note_id + 1), QPushButton('Редактировать', self.notes_gb)])
        self.show_elem_notes()
        self.choice_color_btn.setIcon(QIcon(self.PATH_TO_CHOICE_NOTE_COLOR_ICON))
        # Запись в json файл
        data = open(self.PATH_TO_NOTES_JSON).read()
        js_f = json.loads(data)
        date = str(datetime.datetime.today().date()).split('-')
        date = date[2] + '.' + date[1] + '.' + date[0]

        r, g, b, a = self.notes_color
        r, g, b, a = str(r), str(g), str(b), str(a)
        print(type(self.text_note.toPlainText()))
        js_f['notes'].append(
            {'text': self.text_note.toPlainText(), 'r': r, 'g': g, 'b': b, 'a': a, 'data': date,
             'id': str(self.last_note_id + 1)})
        self.last_note_id += 1
        os.remove(self.PATH_TO_NOTES_JSON)
        g = open(self.PATH_TO_NOTES_JSON, mode='w').write(json.dumps(js_f, ensure_ascii=False))
        self.text_note.setText('')
        self.notes_color = (0, 255, 0, 255)

    def switch_notes_f(self):
        # Функция для переключения на вкладку "Заметки"
        self.groupBox_5.resize(1671, 1071)
        self.add_notes.clicked.connect(self.add_note_f)
        self.switch_notes.setIcon(QIcon(self.PATH_TO_ACTIVE_NOTES_ICON))
        self.clear_all_tasks()
        self.notes_color = (0, 255, 0, 255)
        self.clear_buy()
        self.clear_to_dos()
        self.clear_progress()
        self.clear_all_buys()
        self.choice_color_status = False
        self.choice_color.resize(0, 0)
        self.yourself_color.clicked.connect(self.yourself_choice_color)

        self.scroll_notes = QScrollArea(self.groupBox_5)
        self.notes_gb = QGroupBox(self.groupBox_5)

        self.scroll_notes.setWidget(self.notes_gb)
        self.scroll_notes.resize(1630, 800)
        self.scroll_notes.move(0, 440)
        self.scroll_notes.show()
        self.notes_gb.show()
        self.y = 10

        data = open(self.PATH_TO_NOTES_JSON).read()
        self.notes = json.loads(data)['notes']
        self.arr_notes = []
        if len(self.notes) * 90 + 90 >= 580:
            self.notes_gb.resize(1671, len(self.notes) * 90 + 90)
        else:
            self.notes_gb.resize(1671, 580)
        for i in range(len(self.notes)):
            self.arr_notes.append(
                [QLabel(self.notes_gb), QLabel(self.notes_gb), QPushButton(self.notes_gb), QLabel(self.notes_gb),
                 self.notes[i]['text'],
                 (int(self.notes[i]['r']), int(self.notes[i]['g']), int(self.notes[i]['b']), int(self.notes[i]['a'])),
                 self.notes[i]['id'], QPushButton('Редактировать', self.notes_gb)])
            self.show_elem_notes()

    def clear_all_buys(self):
        # Функция для очистки вкладки Все покупки
        self.switch_all_buys.setIcon(QIcon(self.PATH_TO_NOACTIVE_ALL_BUYS_ICON))
        self.groupBox_6.resize(0, 0)

    def switch_all_buys_f(self):
        # Функция для переключения на вкладку Все покупки
        self.switch_all_buys.setIcon(QIcon(self.PATH_TO_ACTIVE_ALL_BUYS_ICON))
        self.clear_notes()
        self.clear_all_tasks()
        self.clear_to_dos()
        self.clear_buy()
        self.clear_progress()
        self.groupBox_6.resize(1671, 1071)
        self.len_scroll_all_buy = 900

        self.scroll_all_buys = QScrollArea(self.groupBox_6)
        self.all_buys_gb = QGroupBox(self.groupBox_6)

        self.scroll_all_buys.setWidget(self.all_buys_gb)
        self.scroll_all_buys.resize(1631, self.len_scroll_all_buy)
        self.scroll_all_buys.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_all_buys.show()
        self.all_buys_gb.show()
        self.scroll_all_buys.move(0, 8)
        self.y = 80

        self.x = 70
        self.arr_buys = []
        self.all_price = 0
        data = open(self.PATH_TO_ALL_BUYS_JSON).read()
        self.buys = json.loads(data)['all_buys']
        print(self.buys)
        for i in range(len(self.buys)):
            self.arr_buys.append(
                [QLabel(self.all_buys_gb), QLabel(self.all_buys_gb), QPushButton(self.all_buys_gb),
                 self.buys[i]['status'],
                 self.buys[i]['text'],
                 str(int(self.buys[i]['price']) * int(self.buys[i]['count'])), QLabel(self.all_buys_gb),
                 self.buys[i]['date'],
                 QPushButton(self.all_buys_gb), QLabel(self.all_buys_gb), self.buys[i]['count'],
                 QLabel(self.all_buys_gb)])
            self.all_price += int(self.buys[i]['price']) * int(self.buys[i]['count'])
            self.show_elem_buy()
        self.itogo_price_all.setText(str(self.all_price))
        pix = QPixmap(self.PATH_TO_RUBLE_ICON)
        self.itogo_icon_all.setPixmap(pix)
        self.itogo_icon_all.resize(self.itogo_icon_all.sizeHint())
        if len(self.buys) * 80 + 80 > self.len_scroll_all_buy:
            self.all_buys_gb.resize(1630, len(self.buys) * 80 + 80)
        else:
            self.all_buys_gb.resize(1630, self.len_scroll_all_buy)

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
        data = open(self.PATH_TO_TODO_JSON).read()
        a = json.loads(data)
        date = str(datetime.datetime.today().date()).split('-')
        date = date[2] + '.' + date[1] + '.' + date[0]
        a['to_do'].append({'text': textt, 'time': time[0] + ':' + time[1], 'date': date, 'status': 'not_do'})
        os.remove(self.PATH_TO_TODO_JSON)
        g = open(self.PATH_TO_TODO_JSON, mode='w').write(json.dumps(a, ensure_ascii=False))

        # Создание элемента
        self.arr_to_dos.append(
            [QLabel(self.tasks_gb), QLabel(self.tasks_gb), QPushButton(self.tasks_gb), 'not_do', textt,
             time[0] + ':' + time[1], QLabel(self.tasks_gb), date, QPushButton(self.tasks_gb)])
        if len(self.arr_to_dos) * 80 >= self.len_scroll_task:
            self.tasks_gb.resize(1671, self.tasks_gb.size().height() + 80)
        self.show_elem_todo()

        print(len(self.arr_to_dos))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
