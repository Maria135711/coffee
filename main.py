import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow


def database():
    conn = sqlite3.connect("coffee.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            degree_roast TEXT NOT NULL,
            ground_or_grains TEXT NOT NULL,
            taste_description TEXT,
            price REAL NOT NULL,
            package_volume INTEGER NOT NULL
        )
    ''')
    conn.commit()

    cursor.execute('''
        INSERT INTO coffee (name, degree_roast, ground_or_grains, taste_description, price, package_volume)
        VALUES (?, ?, ?, ?, ?, ?)''', [
        'Эспрессо', 'Средний', 'Молотый', 'С нотками орехов', 6.0, 100])
    conn.commit()
    conn.close()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.run()

    def run(self):
        # Зададим тип базы данных
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName('coffee.sqlite')
        # И откроем подключение
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('coffee')
        model.select()

        self.tableView.setModel(model)


if __name__ == '__main__':
    database()
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
