import sqlite3
from typing import Optional
from pathlib import Path
from models.author import Author


class AuthorRepository:
    def __init__(self, db_path: str = "authors.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Создаёт таблицу, если её нет"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    date_of_birth TEXT,
                    date_of_death TEXT,
                    biography TEXT
                )
            """)

    def save(self, author: Author) -> int:
        """Сохраняет автора и возвращает ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO authors (
                    full_name, date_of_birth, date_of_death, biography
                ) VALUES (?, ?, ?, ?)
            """, (
                author.full_name, author.date_of_birth, author.date_of_death, author.biography
            ))
            author.id = cursor.lastrowid
            return author.id

    def find_by_id(self, author_id: int) -> Optional[Author]:
        """Находит книгу по ID"""
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT 
                    id, full_name, date_of_birth, date_of_death, biography
                FROM author WHERE id = ?
            """, (author_id,)).fetchone()

            if not row:
                return None

            return Author(
                id=row[0],
                full_name=row[1],
                date_of_birth=row[2],
                date_of_death=row[3],
                biography=row[4])
