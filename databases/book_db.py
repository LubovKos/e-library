import sqlite3
from typing import Optional
from pathlib import Path
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
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    year INTEGER,
                    genre TEXT,
                    pages INTEGER,
                    description TEXT,
                    publisher_id TEXT NOT NULL,
                    FOREIGN KEY (author_id) REFERENCES authors(id),
                    FOREIGN KEY (publisher_id) REFERENCES publishers(id)
                )
               
            """)

    def save(self, book: Book) -> int:
        """Сохраняет книгу и возвращает её ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO books (
                    title, author_id, year, genre, 
                    pages, description, publisher_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                book.title,
                book.author_id,
                book.year,
                book.genre,
                book.pages,
                book.description,
                book.publisher_id
            ))
            book.id = cursor.lastrowid
            return book.id

    def find_by_id(self, book_id: int) -> Optional[Book]:
        """Находит книгу по ID"""
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT 
                    id, title, author_id, year, genre,
                    pages, description, publisher_id, created_at
                FROM books WHERE id = ?
            """, (book_id,)).fetchone()

            if not row:
                return None

            return Book(
                id=row[0],
                title=row[1],
                author_id=row[2],
                year=row[3],
                genre=row[4],
                pages=row[5],
                description=row[6],
                publisher_id=row[7])

