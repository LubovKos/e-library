import csv
import json
import sqlite3
from typing import Optional
from pathlib import Path

from tabulate import tabulate

from models.author import Author


class AuthorRepository:
    def __init__(self, db_path: str = "C:/Users/student/PycharmProjects/booksdb/data/library.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Создаёт таблицу, если её нет"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS author (
                    full_name TEXT PRIMARY KEY,
                    date_of_birth TEXT,
                    date_of_death TEXT,
                    biography TEXT
                )
            """)

    def author_exists(self, author: Author) -> bool:
        """Проверяет, существует ли автор в БД"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT 1 FROM author
                WHERE full_name = ? 
                """,
                (author.full_name,)

            )
            return cursor.fetchone() is not None

    def save(self, author: Author) -> int:
        if self.author_exists(author):
            return -1
        """Сохраняет автора и возвращает ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                   INSERT INTO author (
                       full_name, date_of_birth, date_of_death, biography
                   ) VALUES (?, ?, ?, ?)
               """, (
                author.full_name, author.date_of_birth, author.date_of_death, author.biography
            ))
            return cursor.lastrowid

    def show_all(self):
        """Красивый вывод с использованием tabulate"""
        headers = ["ФИО", "Дата рождения", "Дата смерти", "Биография"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM author')
            authors = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for author in authors:
                table_data.append([
                    author[0],
                    author[1],
                    author[2],
                    author[3]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def update(self, field: str, author: str, new_val):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM author WHERE full_name = ?", (author,))
            ans = len(cursor.fetchall()) > 0
            query = 'UPDATE author SET ' + field + ' = ? WHERE full_name = ?'
            conn.execute(query, (new_val, author))
            return ans

    def delete(self, field: str, value):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM author WHERE " + field + " = ?",(value,))
            ans = len(cursor.fetchall()) > 0
            conn.execute("DELETE FROM author WHERE " + field + " = ?",(value,))
            return ans

    def filter(self, field: str, direction):
        if direction == "up":
            query = "SELECT * FROM author ORDER BY " + field + " ASC"
        elif direction == "down":
            query = "SELECT * FROM author ORDER BY " + field + " DESC"
        else:
            # записать в лог
            raise ValueError("Некорректное значение направления сортировки")
        with self._get_connection() as conn:
            cursor = conn.execute(query)
            authors = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for author in authors:
                table_data.append([
                    author[0],
                    author[1],
                    author[2],
                    author[3]
                ])

            headers = ["ФИО", "Дата рождения", "Дата смерти", "Биография"]
            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def find(self, field: str, value):
        headers = ["ФИО", "Дата рождения", "Дата смерти", "Биография"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM author WHERE ' + field + " = ?", (value,))
            authors = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for author in authors:
                table_data.append([
                    author[0],
                    author[1],
                    author[2],
                    author[3]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")
            return len(authors)

    def export(self, format_type):
        # Проверяем существование директорий, создаем их, если не существуют
        base_path = 'C:/Users/student/PycharmProjects/booksdb/export'

        with self._get_connection() as conn:
            headers = ["ФИО", "Дата рождения", "Дата смерти", "Биография"]
            cursor = conn.execute('SELECT * FROM author')
            authors = cursor.fetchall()
            if format_type == 'csv':
                with open(f'{base_path}/csv/author_export.csv', 'w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    for author in authors:
                        writer.writerow(author)
            if format_type == 'json':
                for author in authors:
                    data = {
                        headers[0]: author[0],
                        headers[1]: author[1],
                        headers[2]: author[2],
                        headers[3]: author[3]
                    }
                    with open(f'{base_path}/json/author_export.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
