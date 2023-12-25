import io
import sqlite3
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>715</width>
    <height>453</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QComboBox" name="comboBox">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>241</width>
      <height>61</height>
     </rect>
    </property>
    <item>
     <property name="text">
      <string>Автор</string>
     </property>
    </item>
    <item>
     <property name="text">
      <string>Название</string>
     </property>
    </item>
   </widget>
   <widget class="QLineEdit" name="lineEdit">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>80</y>
      <width>241</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>510</x>
      <y>10</y>
      <width>181</width>
      <height>101</height>
     </rect>
    </property>
    <property name="text">
     <string>Искать</string>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>15</x>
      <y>121</y>
      <width>681</width>
      <height>301</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class inf_book(qtw.QWidget):
    def __init__(self, res):
        super().__init__()
        self.setWindowTitle('Информация о книге')

        # widgets
        self.label_1 = qtw.QLabel('Название:', self)
        self.label_2 = qtw.QLabel('', self)
        self.label_2.setText(res[0])
        self.label_3 = qtw.QLabel('Автор:', self)
        self.label_4 = qtw.QLabel('', self)
        self.label_4.setText(res[1])
        self.label_5 = qtw.QLabel('Год выпуска:', self)
        self.label_6 = qtw.QLabel('', self)
        self.label_6.setText(str(res[2]))
        self.label_7 = qtw.QLabel('Жанр:', self)
        self.label_8 = qtw.QLabel('', self)
        self.label_8.setText(res[-1])

        self.label = qtw.QLabel(self)
        self.pixmap = QtGui.QPixmap(f'images/{res[0]}.png')
        self.label.setPixmap(self.pixmap)
        # layouts
        self.layout_1 = qtw.QHBoxLayout()
        self.layout_2 = qtw.QHBoxLayout()
        self.layout_3 = qtw.QHBoxLayout()
        self.layout_4 = qtw.QHBoxLayout()
        self.main_layout = qtw.QVBoxLayout()
        # add
        self.main_layout.addWidget(self.label)
        self.layout_1.addWidget(self.label_1)
        self.layout_1.addWidget(self.label_2)
        self.main_layout.addLayout(self.layout_1)
        self.layout_2.addWidget(self.label_3)
        self.layout_2.addWidget(self.label_4)
        self.main_layout.addLayout(self.layout_2)
        self.layout_3.addWidget(self.label_5)
        self.layout_3.addWidget(self.label_6)
        self.main_layout.addLayout(self.layout_3)
        self.layout_4.addWidget(self.label_7)
        self.layout_4.addWidget(self.label_8)
        self.main_layout.addLayout(self.layout_4)
        
        self.setLayout(self.main_layout)


class MyWidget(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = io.StringIO(template)
        uic.loadUi(ui_file, self)
        self.con = sqlite3.connect("books.sqlite")
        self.pushButton.clicked.connect(self.clicked)
        self.setWindowTitle('Каталог библиотеки')
        # comboBox, lineEdit, pushButton, tableWidget

    def clicked(self):
        text = self.lineEdit.text().lower()[:3]
        cur = self.con.cursor()
        if not len(text):
            return
        # находим подходящих
        if self.comboBox.currentText() == 'Автор':
            result_all, lst_of_authors, good = cur.execute(f""" SELECT author FROM books """).fetchall(), set(), []
        else:
            result_all, lst_of_authors, good = cur.execute(f""" SELECT name FROM books """).fetchall(), set(), []

        for i in result_all:
            lst_of_authors.add(i[0])
        for i in list(lst_of_authors):
            if text in i.lower():
                good.append(i)
        # ищем авторов
        if len(good):
            all_good = []
            for i in good:
                if self.comboBox.currentText() == 'Автор':
                    res = cur.execute(""" SELECT * FROM books WHERE author = ? """, (i,)).fetchall()
                else:
                    res = cur.execute(""" SELECT * FROM books WHERE name = ? """, (i,)).fetchall()
                all_good += res
            # setting table
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setRowCount(len(all_good))
            self.tableWidget.setColumnWidth(0, 600)
            for i in range(len(all_good)):
                btn = qtw.QPushButton(all_good[i][0], self)
                btn.setFixedSize(600, 30)
                btn.clicked.connect(self.book_clicked)
                self.tableWidget.setCellWidget(i, 0, btn)

    def book_clicked(self):
        cur = self.con.cursor()
        res = cur.execute(""" SELECT * FROM books WHERE name = ? """, (self.sender().text(),)).fetchall()[0]
        self.copy = inf_book(res)
        self.copy.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
