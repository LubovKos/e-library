import sqlite3
from typing import Optional
from pathlib import Path
from models.publishing import (Publisher)


class GenreRepository:
    def __init__(self, db_path: str = "publishers.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """Создаёт таблицу, если её нет"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS publishers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT,
                    phone TEXT,
                    mail TEXT
                )
            """)

    def save(self, publisher: Publisher) -> int:
        """Сохраняет издательство и возвращает ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO publishers (
                    name, address, phone, mail
                ) VALUES (?, ?, ?, ?)
            """, (
                publisher.name, publisher.address, publisher.phone, publisher.mail
            ))
            publisher.id = cursor.lastrowid
            return publisher.id

    def find_by_id(self, publisher_id: int) -> Optional[Publisher]:
        """Находит издательство по ID"""
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT 
                    id, name, address, phone, mail
                FROM publishers WHERE id = ?
            """, (publisher_id,)).fetchone()

            if not row:
                return None

            return Publisher(
                id=row[0],
                name=row[1],
                address=row[2],
                phone=row[3],
                mail=row[4])
