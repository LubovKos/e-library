import json
import sqlite3
from typing import Optional
from pathlib import Path

from tabulate import tabulate

from models.publisher import (Publisher)


class PublisherRepository:
    def __init__(self, db_path: str = "C:/Users/student/PycharmProjects/booksdb/data/library.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Создаёт таблицу, если её нет"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS publisher (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT,
                    phone TEXT,
                    mail TEXT
                )
            """)

    def publisher_exists(self, publisher: Publisher) -> bool:
        """Проверяет, существует ли жанр в БД"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT 1 FROM publisher
                WHERE name = ? 
                """,
                (publisher.name,)
            )
            return cursor.fetchone() is not None

    def save(self, publisher: Publisher) -> int:
        """Сохраняет издательство и возвращает ID"""
        if self.publisher_exists(publisher):
            return -1
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO publisher (
                    name, address, phone, mail
                ) VALUES (?, ?, ?, ?)
            """, (
                publisher.name, publisher.address, publisher.phone, publisher.mail
            ))
            publisher.id = cursor.lastrowid
            return publisher.id

    def show_all(self):
        """Красивый вывод с использованием tabulate"""
        headers = ["ID", "Название", "Адрес", "Телефон", "Почта"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM publisher')
            publishers = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for publisher in publishers:
                table_data.append([
                    publisher[0],
                    publisher[1],
                    publisher[2],
                    publisher[3],
                    publisher[4]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def update(self, field: str, title: str, new_val):
        with self._get_connection() as conn:
            query = 'UPDATE publisher SET ' + field + ' = ? WHERE name = ?'
            conn.execute(query, (new_val, title))

    def delete(self, field: str, value):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM publisher WHERE " + field + " = ?", (value,))

    def filter(self, field: str, direction):
        if direction == "up":
            query = "SELECT * FROM publisher ORDER BY " + field + " ASC"
        elif direction == "down":
            query = "SELECT * FROM publisher ORDER BY " + field + " DESC"
        else:
            # записать в лог
            raise ValueError("Некорректное значение направления сортировки")
        with self._get_connection() as conn:
            cursor = conn.execute(query)
            publishers = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for publisher in publishers:
                table_data.append([
                    publisher[0],
                    publisher[1],
                    publisher[2],
                    publisher[3],
                    publisher[4]
                ])

            headers = ["ID", "Название", "Адрес", "Телефон", "Почта"]
            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def find(self, field: str, value):
        headers = ["ID", "Название", "Адрес", "Телефон", "Почта"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM publisher WHERE ' + field + " = ?", (value,))
            publishers = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for publisher in publishers:
                table_data.append([
                    publisher[0],
                    publisher[1],
                    publisher[2],
                    publisher[3],
                    publisher[4]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")
            return len(publishers)

    def export(self):
        with self._get_connection() as conn:
            headers = ["ID", "Название", "Адрес", "Телефон", "Почта"]
            cursor = conn.execute('SELECT * FROM publisher')
            publishers = cursor.fetchall()
            for publisher in publishers:
                data = {
                    headers[0]: publisher[0],
                    headers[1]: publisher[1],
                    headers[2]: publisher[2],
                    headers[3]: publisher[3],
                    headers[4]: publisher[4]
                }
                with open('C:/Users/student/PycharmProjects/booksdb/export/json/publisher_export.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
