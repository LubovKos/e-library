import sqlite3
from typing import Optional
from pathlib import Path
from models.genre import Genre


class GenreRepository:
    def __init__(self, db_path: str = "genres.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Создаёт таблицу, если её нет"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT
                )
            """)

    def save(self, genre: Genre) -> int:
        """Сохраняет жанры и возвращает ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO genres (
                    title, description
                ) VALUES (?, ?)
            """, (
                genre.title, genre.description
            ))
            genre.id = cursor.lastrowid
            return genre.id

    def find_by_id(self, genre_id: int) -> Optional[Genre]:
        """Находит книгу по ID"""
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT 
                    id, title, description
                FROM author WHERE id = ?
            """, (genre_id,)).fetchone()

            if not row:
                return None

            return Genre(
                id=row[0],
                title=row[1],
                description=row[2])
