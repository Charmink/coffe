import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sqlite3


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.view)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
