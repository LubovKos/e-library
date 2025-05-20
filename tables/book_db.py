import csv
import sqlite3
from typing import Optional
from pathlib import Path
from tabulate import tabulate
from models.book import Book
import json


class BookRepository:
    def __init__(self, db_path: str = "C:/Users/student/PycharmProjects/booksdb/data/library.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Создаёт таблицу, если её нет"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS book (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    genre TEXT,
                    pages INTEGER,
                    description TEXT,
                    publisher TEXT NOT NULL,
                    FOREIGN KEY (author) REFERENCES author(full_name),
                    FOREIGN KEY (genre) REFERENCES genre(title),
                    FOREIGN KEY (publisher) REFERENCES publisher(name)
                )
            """)

    def book_exists(self, book: Book) -> bool:
        """Проверяет, существует ли книга в БД"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT 1 FROM book
                WHERE title = ? AND author = ? AND year = ? AND genre = ? AND pages = ? AND publisher = ?
                """,
                (book.title, book.author, book.year, book.genre, book.pages, book.publisher)
            )
            return cursor.fetchone() is not None

    def save(self, book: Book) -> int:
        if self.book_exists(book):
            return -1
        """Сохраняет книгу и возвращает её ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO book (
                    title, author, year, genre, 
                    pages, description, publisher
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                book.title,
                book.author,
                book.year,
                book.genre,
                book.pages,
                book.description,
                book.publisher
            ))
            book.id = cursor.lastrowid
            return book.id

    def show_all(self):
        """Красивый вывод с использованием tabulate"""
        headers = ["ID", "Название", "Автор", "Год", "Жанр", "Страниц", "Издательство"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM book')
            books = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for book in books:
                table_data.append([
                    book[0],
                    book[1],
                    book[2],
                    book[3],
                    book[4],
                    book[5],
                    book[7]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def update(self, field: str, title: str, author: str, new_val):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM book WHERE title = ? AND author = ?", (title, author))
            ans = len(cursor.fetchall()) > 0
            query = 'UPDATE book SET ' + field + ' = ? WHERE title = ? AND author = ?'
            conn.execute(query, (new_val, title, author))
            return ans

    def delete(self, field: str, value):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM book WHERE " + field + " = ?", (value,))
            ans = len(cursor.fetchall()) > 0
            conn.execute("DELETE FROM book WHERE " + field + " = ?", (value,))
            return ans

    def filter(self, field: str, direction):
        if direction == "up":
            query = "SELECT * FROM book ORDER BY " + field + " ASC"
        elif direction == "down":
            query = "SELECT * FROM book ORDER BY " + field + " DESC"
        else:
            # записать в лог
            raise ValueError("Некорректное значение направления сортировки")
        with self._get_connection() as conn:
            cursor = conn.execute(query)
            books = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for book in books:
                table_data.append([
                    book[0],
                    book[1],
                    book[2],
                    book[3],
                    book[4],
                    book[5],
                    book[7]
                ])

            headers = ["ID", "Название", "Автор", "Год", "Жанр", "Страниц", "Издательство"]
            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")

    def find(self, field: str, value):
        headers = ["ID", "Название", "Автор", "Год", "Жанр", "Страниц", "Издательство"]
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM book WHERE ' + field + " = ?", (value,))
            books = cursor.fetchall()
            # Выводим результаты
            table_data = []
            for book in books:
                table_data.append([
                    book[0],
                    book[1],
                    book[2],
                    book[3],
                    book[4],
                    book[5],
                    book[7]
                ])

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")
            return len(books)

    def export(self, format_type):
        # Проверяем существование директорий, создаем их, если не существуют
        base_path = 'C:/Users/student/PycharmProjects/booksdb/export'

        with self._get_connection() as conn:
            headers = ["ID", "Название", "Автор", "Год", "Жанр", "Страниц", "Издательство"]
            cursor = conn.execute('SELECT * FROM book')
            books = cursor.fetchall()
            if format_type == 'csv':
                with open(f'{base_path}/csv/book_export.csv', 'w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    for book in books:
                        writer.writerow(book)
            if format_type == 'json':
                for book in books:
                    data = {
                        headers[0]: book[0],
                        headers[1]: book[1],
                        headers[2]: book[2],
                        headers[3]: book[3],
                        headers[4]: book[4],
                        headers[5]: book[5],
                        headers[6]: book[6]
                    }
                    with open(f'{base_path}/json/book_export.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)


