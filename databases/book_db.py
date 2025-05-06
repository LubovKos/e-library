import sqlite3
from typing import Optional
from pathlib import Path

from tabulate import tabulate

from models.book import Book


class BookRepository:
    def __init__(self, db_path: str = "books.db"):
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
                    publisher TEXT NOT NULL
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
            return 0
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

    def find_by_id(self, book_id: int) -> Optional[Book]:
        """Находит книгу по ID"""
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT 
                    id, title, author, year, genre,
                    pages, description, publisher, created_at
                FROM book WHERE id = ?
            """, (book_id,)).fetchone()

            if not row:
                return None

            return Book(
                id=row[0],
                title=row[1],
                author=row[2],
                year=row[3],
                genre=row[4],
                pages=row[5],
                description=row[6],
                publisher=row[7])

