import csv
import json
import sqlite3
from typing import Optional
from pathlib import Path

from tabulate import tabulate

from models.genre import Genre


class GenreRepository:
    def __init__(self, db_path: str = "C:/Users/student/PycharmProjects/booksdb/data/library.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Создаёт таблицу, если её нет"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS genre (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT
                )
            """)

    def genre_exists(self, genre: Genre) -> bool:
        """Проверяет, существует ли жанр в БД"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT 1 FROM genre
                WHERE title = ? 
                """,
                (genre.title,)
            )
            return cursor.fetchone() is not None

    def save(self, genre: Genre) -> int:
        if self.genre_exists(genre):
            return -1
        """Сохраняет жанры и возвращает ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO genre (
                    title, description
                ) VALUES (?, ?)
            """, (
                genre.title, genre.description
            ))
            genre.id = cursor.lastrowid
            return genre.id

    def show_all(self):
        """Красивый вывод с использованием tabulate"""
        headers = ["ID", "Название", "Описание"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM genre')
            genres = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for genre in genres:
                table_data.append([
                    genre[0],
                    genre[1],
                    genre[2]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def update(self, field: str, title: str, new_val):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM genre WHERE title = ?", (title, ))
            ans = len(cursor.fetchall())
            query = 'UPDATE genre SET ' + field + ' = ? WHERE title = ?'
            conn.execute(query, (new_val, title))
            return ans

    def delete(self, field: str, value):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM genre WHERE " + field + " = ?", (value,))
            ans = len(cursor.fetchall())
            conn.execute("DELETE FROM genre WHERE " + field + " = ?", (value,))
            return ans

    def filter(self, field: str, direction):
        if direction == "up":
            query = "SELECT * FROM genre ORDER BY " + field + " ASC"
        elif direction == "down":
            query = "SELECT * FROM genre ORDER BY " + field + " DESC"
        else:
            # записать в лог
            raise ValueError("Некорректное значение направления сортировки")
        with self._get_connection() as conn:
            cursor = conn.execute(query)
            genres = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for genre in genres:
                table_data.append([
                    genre[0],
                    genre[1],
                    genre[2]
                ])

            headers = ["ID", "Название", "Описание"]
            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def find(self, field: str, value):
        headers = ["ID", "Название", "Описание"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM genre WHERE ' + field + " = ?", (value,))
            genres = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for genre in genres:
                table_data.append([
                    genre[0],
                    genre[1],
                    genre[2]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")
            return len(genres)

    def export(self, format_type):
        # Проверяем существование директорий, создаем их, если не существуют
        base_path = 'C:/Users/student/PycharmProjects/booksdb/export'

        with self._get_connection() as conn:
            headers = ["ID", "Название", "Описание"]
            cursor = conn.execute('SELECT * FROM genre')
            genres = cursor.fetchall()
            if format_type == 'csv':
                with open(f'{base_path}/csv/genre_export.csv', 'w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    for genre in genres:
                        writer.writerow(genre)
            if format_type == 'json':
                for genre in genres:
                    data = {
                        headers[0]: genre[0],
                        headers[1]: genre[1],
                        headers[2]: genre[2]
                    }
                    with open(f'{base_path}/json/genre_export.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)