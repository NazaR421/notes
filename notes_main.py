from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QListWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QInputDialog

import json


app = QApplication([])

roster = {}


window = QWidget()
window.setWindowTitle("Розумні замітки")
window.resize(900, 500)

text_edit = QTextEdit()
notes = QLabel("Список заміток")
list_notes = QListWidget()
create_note = QPushButton("Створити замітку")
del_note = QPushButton("Видалити замітку")
save_not = QPushButton("Зберегти замітку")

tag = QLabel("Список тегів")
list_tag = QListWidget()
enter_tags = QLineEdit()
enter_tags.setPlaceholderText("Введіть тег...")

add_tag = QPushButton("Додати до замітки")
del_tag = QPushButton("Відкріпити від замітки")
search_tag = QPushButton("Шукати ззамітку по тегу")

line_x = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(text_edit)

col2.addWidget(notes)
col2.addWidget(list_notes)

line1 = QHBoxLayout()
line1.addWidget(create_note)
line1.addWidget(del_note)

col2.addLayout(line1)
col2.addWidget(save_not)

col2.addWidget(tag)
col2.addWidget(list_tag)
col2.addWidget(enter_tags)

line2 = QHBoxLayout()
line2.addWidget(add_tag)
line2.addWidget(del_tag)

col2.addLayout(line2)
col2.addWidget(search_tag)


line_x.addLayout(col1, stretch = 2)
line_x.addLayout(col2, stretch = 1)

window.setLayout(line_x)

def add_note():
    name_note, check_note = QInputDialog.getText(window, 'Створити замітку', 'Запиши назву замітки')
    if check_note and name_note != '':
        roster[name_note] = {'текст': '', 'теги':[]}
        list_notes.addItem(name_note)
        list_tag.addItems(roster[name_note]['теги'])

create_note.clicked.connect(add_note)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        roster[key]['текст'] = text_edit.toPlainText()
        with open('notes.json', 'w') as file:
            json.dump(roster, file, sort_keys=True)
    else:
        print("Замітку для збереження не обрано")  


save_not.clicked.connect(save_note)

def delete_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del roster[key]
        list_notes.clear()
        list_tag.clear()
        text_edit.clear()
        list_notes.addItems(roster)
        with open('notes.json', 'w') as file:
            json.dump(roster, file, sort_keys=True)
    else:
        print("Замітку для збереження не обрано") 

del_note.clicked.connect(delete_note)

def show_note():
    note_text = list_notes.selectedItems()[0].text()
    text_edit.setText(roster[note_text]['текст'])
    list_tag.clear()
    list_tag.addItems(roster[note_text]['теги'])


list_notes.itemClicked.connect(show_note)    

def add_tags():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = enter_tags.text()
        if not tag in roster[key]['теги']:
            roster[key]['теги'].append(tag)
            list_tag.addItem(tag)
            enter_tags.clear()
        with open('notes.json', 'w') as file:
            json.dump(roster, file, sort_keys=True)
    else:
        print("Замітку для додавання тегу не обрано")     

add_tag.clicked.connect(add_tags)


def delete_tag():
    if list_tag.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tag.selectedItems()[0].text()
        roster[key]['теги'].remove(tag)
        list_tag.clear()
        list_tag.addItems(roster[key]['теги'])
        with open('notes.json', 'w') as file:
            json.dump(roster, file, sort_keys=True)
    else:
        print("Тег для видалення не обрано")

del_tag.clicked.connect(delete_tag)

def search_note():
    tag = enter_tags.text()
    if search_tag.text() == "Шукати ззамітку по тегу" and tag:
        slovnik = {}
        for rost in roster:
            if tag in roster[rost]['теги']:
                slovnik[rost] = roster[rost]
        search_tag.setText('Скинути пошук')
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(slovnik)
    elif search_tag.text() == "Скинути пошук":
        enter_tags.clear()
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(roster)
        search_tag.setText('Шукати ззамітку по тегу')            

search_tag.clicked.connect(search_note)

with open('notes.json', 'r') as file:
    roster = json.load(file)


list_notes.addItems(roster)



window.show()
app.exec_()

