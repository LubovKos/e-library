import sqlite3
from typing import Optional
from pathlib import Path

from tabulate import tabulate

from models.reader import (Reader)


class ReaderRepository:
    def __init__(self, db_path: str = "C:/Users/student/PycharmProjects/booksdb/data/bases/reader.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Создаёт таблицу, если её нет"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reader (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    phone TEXT,
                    mail TEXT
                )
            """)

    def reader_exists(self, reader: Reader) -> bool:
        """Проверяет, существует ли читатель в БД"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT 1 FROM reader
                WHERE full_name = ? 
                """,
                (reader.full_name,)
            )
            return cursor.fetchone() is not None

    def save(self, reader: Reader) -> int:
        if self.reader_exists(reader):
            return 0
        """Сохраняет издательство и возвращает ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO reader (
                    full_name, phone, mail
                ) VALUES (?, ?, ?)
            """, (
                reader.full_name, reader.phone, reader.mail
            ))
            reader.id = cursor.lastrowid
            return reader.id

    def show_all(self):
        """Красивый вывод с использованием tabulate"""
        headers = ["ID", "ФИО", "Телефон", "Почта"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM reader')
            readers = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for reader in readers:
                table_data.append([
                    reader[0],
                    reader[1],
                    reader[2],
                    reader[3]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def update(self, field: str, title: str, new_val):
        with self._get_connection() as conn:
            query = 'UPDATE reader SET ' + field + ' = ? WHERE full_name = ?'
            conn.execute(query, (new_val, title))

    def delete(self, field: str, value):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM reader WHERE " + field + " = ?", (value,))

    def filter(self, field: str, direction):
        if direction == "up":
            query = "SELECT * FROM reader ORDER BY " + field + " ASC"
        elif direction == "down":
            query = "SELECT * FROM reader ORDER BY " + field + " DESC"
        else:
            # записать в лог
            raise ValueError("Некорректное значение направления сортировки")
        with self._get_connection() as conn:
            cursor = conn.execute(query)
            readers = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for reader in readers:
                table_data.append([
                    reader[0],
                    reader[1],
                    reader[2],
                    reader[3]
                ])

            headers = ["ID", "ФИО", "Телефон", "Почта"]
            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def find(self, field: str, value):
        headers = ["ID", "ФИО", "Телефон", "Почта"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM reader WHERE ' + field + " = ?", (value,))
            readers = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for reader in readers:
                table_data.append([
                    reader[0],
                    reader[1],
                    reader[2],
                    reader[3]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")
            return len(readers)
