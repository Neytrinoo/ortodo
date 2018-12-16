from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QColorDialog
from PyQt5.QtGui import QIcon
from PIL import Image, ImageDraw
import json
from change_note_window import Ui_MainWindow


class Change_note(QMainWindow, Ui_MainWindow):
    def __init__(self, note_id, parent, color):
        super().__init__(parent, QtCore.Qt.Window)
        self.setupUi(self)
        self.PATH_TO_NOTES_JSON = 'databases/notes.json'
        self.note_id = note_id
        self.choice_color_status = False
        self.notes_color = color

        image = Image.new('RGBA', (35, 35))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 35, 35), fill=self.notes_color)
        image.save('ellipse.png')
        self.choice_color_btn.setIcon(QIcon('ellipse.png'))

        self.yourself_color.clicked.connect(self.yourself_choice_color)
        self.choice_color_btn.clicked.connect(self.set_color_show)
        self.load_text()

    def load_text(self): # Вывод текста заметки в TexEdit
        data = open(self.PATH_TO_NOTES_JSON).read()
        data = json.loads(data)['notes']
        for i in range(len(data)):
            if data[i]['id'] == self.note_id:
                self.note_text.setText(data[i]['text'])

    def set_color_show(self):
        # Функция для показа или убирания GroupBox'а с выбором цвета для заметки
        if self.choice_color_status:
            self.choice_color.resize(0, 0)
            self.choice_color_status = False
        else:
            self.choice_color.resize(60, 210)
            self.choice_color_status = True

    def yourself_choice_color(self): # функция для выбора своего цвета с помощью диалогового окна
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
