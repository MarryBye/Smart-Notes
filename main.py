# ЧТОБІ СДЕЛАТЬ ui.py: python -m PyQt5.uic.pyuic -x untitled.ui -o ui.py

from PyQt5.QtWidgets import *
from ui import Ui_MainWindow

import json

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

app = QApplication([])
ex = Widget()

notes = {}

# Добавить заметку
def add_note():
    # Показать окно для создания заметки
    note_name, ok = QInputDialog.getText(ex, "Створити замітку", "Введіть замітку")
    # Если нажали ок, название не пустое и такой заметки нет
    if ok and note_name != "" and note_name not in notes:
        # Создаем пустую заметку с названием
        notes[note_name] = {
            "текст": "Пусто...",
            "теги": []
        }
        # Добавляем в список в программе
        ex.ui.listWidget.addItem(note_name)

def del_note():
    # Получаем кол-во вібранніх заметок
    if len(ex.ui.listWidget.selectedItems()) > 0:
        # Отримали замітку, на яку натиснули
        note = ex.ui.listWidget.selectedItems()[0].text()
        # Видалили замітку, яку обрали
        del notes[note]
        # Очистили список заміток й заповнили заново
        ex.ui.listWidget.clear()
        ex.ui.listWidget.addItems(notes)
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=True, indent=4)

def save_note():
    if len(ex.ui.listWidget.selectedItems()) > 0:
        note = ex.ui.listWidget.selectedItems()[0].text()
        notes[note] = {
            "текст": ex.ui.textEdit.toPlainText(),
            "теги": []
        }
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=True, indent=4)

def show_note():
    note = ex.ui.listWidget.selectedItems()[0].text()
    ex.ui.textEdit.setText(notes[note]["текст"])
    ex.ui.listWidget_2.clear()
    ex.ui.listWidget_2.addItems(notes[note]["теги"])

def add_tag():
    if len(ex.ui.listWidget.selectedItems()) > 0:
        note = ex.ui.listWidget.selectedItems()[0].text()
        new_tag = ex.ui.lineEdit.text()
        if new_tag != "" and new_tag not in notes[note]["теги"]:
            notes[note]["теги"].append(new_tag)
            ex.ui.listWidget_2.addItem(new_tag)

            with open("notes.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, ensure_ascii=True, indent=4)

def del_tag():
    # Нажали ли на заметку?
    if len(ex.ui.listWidget.selectedItems()) > 0:
        # Нажали ли на тег?
        if len(ex.ui.listWidget_2.selectedItems()) > 0:
            # Получаем заметку и тег на которіе нажали
            note = ex.ui.listWidget.selectedItems()[0].text()
            tag = ex.ui.listWidget_2.selectedItems()[0].text()
            # Удаляем заметку и обновляем списки
            notes[note]["теги"].remove(tag)
            ex.ui.listWidget_2.clear()
            ex.ui.listWidget_2.addItems(notes[note]["теги"])
            # Сохраняем обновленную заметку
            with open("notes.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, ensure_ascii=True, indent=4)



def find_by_tag():
    # Кнопка все время меняет названия "Поиск по тегу" и "Сбросить поиск"
    if ex.ui.pushButton_6.text() == "Поиск по тегу":
        # Если на кнопке біло написано "Поиск по тегу"
        ex.ui.pushButton_6.setText("Сбросить поиск")
        # Получаем тег,которій написалии делаем копию заметок
        tag = ex.ui.lineEdit.text()
        notes_copy = {}
        # Фильтруем заметки с нужнім тегом
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_copy[note] = notes[note]
        ex.ui.listWidget.clear()
        ex.ui.listWidget.addItems(notes_copy)
        ex.ui.listWidget_2.clear()
        ex.ui.textEdit.clear()
    else:
        ex.ui.pushButton_6.setText("Поиск по тегу")
        ex.ui.listWidget.clear()
        ex.ui.listWidget.addItems(notes)
        ex.ui.listWidget_2.clear()
        ex.ui.textEdit.clear()

with open("notes.json", "r", encoding="utf-8") as file:
    notes = json.load(file)

ex.ui.listWidget.addItems(notes)

ex.ui.listWidget.itemClicked.connect(show_note)
ex.ui.pushButton_2.clicked.connect(add_note)
ex.ui.pushButton.clicked.connect(del_note)
ex.ui.pushButton_3.clicked.connect(save_note)
ex.ui.pushButton_5.clicked.connect(add_tag)
ex.ui.pushButton_4.clicked.connect(del_tag)
ex.ui.pushButton_6.clicked.connect(find_by_tag)

ex.show()
app.exec_()
