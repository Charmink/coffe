import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5 import uic
import sqlite3
from GUI_1 import Ui_MainWindow
from GUI_2 import Ui_Form


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.view)
        self.pushButton_2.clicked.connect(self.change)
        self.result = None

    def view(self):
        self.result = self.cur.execute('SELECT * FROM Coffe WHERE title = ?',
                                           (self.lineEdit.text(),)).fetchall()
        if not self.result:
            return
        res = list(self.result[0])
        res[2] = self.cur.execute('SELECT title FROM Obzharka WHERE id = ?',
                                  (res[2],)).fetchall()[0][0]
        res[3] = self.cur.execute('SELECT title FROM Structura WHERE id = ?',
                                  (res[3],)).fetchall()[0][0]
        self.textBrowser.setText('Сорт: {}\nОбжарка: {}\nСтруктура: {}\nВкус: {}\nЦена: '
                                 '{}руб.\nОбьем: {}г'.format(*res[1:]))

    def change(self):
        self.changes = Changes()
        self.changes.show()


class Changes(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.change)
        self.pushButton_2.clicked.connect(self.create_)
        self.result = None

    def change(self):
        self.result = self.cur.execute('SELECT * FROM Coffe WHERE title = ?',
                                       (self.lineEdit.text(),)).fetchone()
        if self.result:
            if self.lineEdit_2.text() == '':
                self.lineEdit_2.setText(self.cur.execute('SELECT title FROM Obzharka WHERE id = ?',
                                                         (self.result[2],)).fetchone()[0])
            if self.lineEdit_3.text() == '':
                self.lineEdit_3.setText(self.cur.execute('SELECT title FROM Structura WHERE id = ?',
                                                         (self.result[3],)).fetchone()[0])
            if self.lineEdit_4.text() == '':
                self.lineEdit_4.setText(str(self.result[4]))
            if self.lineEdit_5.text() == '':
                self.lineEdit_5.setText(str(self.result[5]))
            if self.lineEdit_6.text() == '':
                self.lineEdit_6.setText(str(self.result[6]))
            if self.lineEdit_2.text() in ['Светлая', 'Средняя', 'Средне-темная', 'Темная',
                                          'Очень темная'] and self.lineEdit_3.text() in \
                    ['В зернах', 'Молотый'] and self.lineEdit_5.text().isdigit() and \
                    self.lineEdit_6.text().isdigit():
                self.cur.execute('UPDATE Coffe SET vkus = ?, price = ?, volume = ?, '
                                 'obzhar = ?, struct = ? WHERE title = ?', (self.lineEdit_4.text(),
                                                                            self.lineEdit_5.text(),
                                                                            self.lineEdit_6.text(),
                                                                            self.cur.execute(
                                                                                'SELECT id FROM '
                                                                                'Obzharka WHERE '
                                                                                'title = ?',
                                                                                (self.lineEdit_2
                                                                                 .text(),))
                                                                            .fetchone()[0],
                                                                            self.cur.execute(
                                                                                'SELECT id FROM '
                                                                                'Structura WHERE '
                                                                                'title = ?',
                                                                                (self.lineEdit_3
                                                                                 .text(),))
                                                                            .fetchone()[0],
                                                                            self.lineEdit.text(), ))

            self.con.commit()

    def create_(self):
        if self.lineEdit_2.text() in ['Светлая', 'Средняя', 'Средне-темная', 'Темная',
                                      'Очень темная'] and self.lineEdit_3.text() in \
                ['В зернах', 'Молотый'] and self.lineEdit_5.text().isdigit() and \
                self.lineEdit_6.text().isdigit() and self.lineEdit.text():
            self.cur.execute('INSERT INTO Coffe (vkus, price, volume, obzhar, struct, '
                             'title) VALUES (?, ?, ?, ?, ?, ?)',
                             (self.lineEdit_4.text(), self.lineEdit_5.text(),
                              self.lineEdit_6.text(),
                              self.cur.execute('SELECT id FROM Obzharka WHERE title = ?',
                                               (self.lineEdit_2.text(),)).fetchone()[0],
                              self.cur.execute('SELECT id FROM Structura WHERE title = ?',
                                               (self.lineEdit_3.text(),)).fetchone()[0],
                              self.lineEdit.text(),))
            self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
