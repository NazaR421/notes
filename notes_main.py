from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton,QSpinBox, QLabel, QVBoxLayout,QRadioButton,\
    QHBoxLayout,QButtonGroup,QGroupBox,QApplication,QLineEdit,QListWidget,QTextEdit,QInputDialog
import json 

app=QApplication([])

#словник
notes={
    "Ласкаво просимо!":{
        "текст":"Це найкращий додаток замыток у світі!",
        "теги":["Замітки","інструкція"]
    }
} 
with open("notes_data.json","w") as file:
    json.dump(notes,file)



notes_window=QWidget()
notes_window.setWindowTitle("Розумні замітки")
notes_window.resize(900,600)



list_notes_label=QLabel("Список заміток")
list_notes=QListWidget()
button_note_create=QPushButton("Створити замітку")
button_note_del=QPushButton("Видалити замітку")
button_note_save=QPushButton("Зберегти зміну")
field_text=QTextEdit()
list_tags_label=QLabel("Список тегів")
list_tags=QListWidget()
field_tag=QLineEdit()
field_tag.setPlaceholderText("Введіть тег... ")
button_tag_add=QPushButton("Додати до замітки")
button_tag_del=QPushButton("Відкріпіти від замітки")
button_tag_search=QPushButton("Шукати замітку по тегу")


col_1=QVBoxLayout()
col_1.addWidget(field_text)

col_2=QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)


row_1=QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2=QHBoxLayout()
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3=QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

row_4=QHBoxLayout()
row_4.addWidget(button_tag_search)



col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes=QHBoxLayout()
layout_notes.addLayout(col_1,stretch=2)
layout_notes.addLayout(col_2,stretch=1)
notes_window.setLayout(layout_notes)

note_name=()

def add_note():
    note_name, ok=QInputDialog.getText(notes_window,"Додати замітку","Назва замітки:")
    if ok and note_name !="":
        notes[note_name]={"текст":"","теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
button_note_create.clicked.connect(add_note)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json","w")as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для вилучення не обрана!")
button_note_del.clicked.connect(del_note)



notes_window.show()
app.exec_()
