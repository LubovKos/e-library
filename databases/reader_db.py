import sqlite3
from typing import Optional
from pathlib import Path
from models.reader import (Reader)


class GenreRepository:
    def __init__(self, db_path: str = "readers.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Создаёт таблицу, если её нет"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS readers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    phone TEXT,
                    mail TEXT
                )
            """)

    def save(self, reader: Reader) -> int:
        """Сохраняет издательство и возвращает ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO readers (
                    full_name, phone, mail
                ) VALUES (?, ?, ?)
            """, (
                reader.full_name, reader.phone, reader.mail
            ))
            reader.id = cursor.lastrowid
            return reader.id

    def find_by_id(self, reader_id: int) -> Optional[Reader]:
        """Находит издательство по ID"""
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT 
                    id, full_name, address, phone, mail
                FROM readers WHERE id = ?
            """, (reader_id,)).fetchone()

            if not row:
                return None

            return Reader(
                id=row[0],
                full_name=row[1],
                phone=row[2],
                mail=row[3])
