from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from models.author import Author


@dataclass
class Book:
    """Модель книги с базовой валидацией"""
    title: str
    author: str
    description: str
    year: int
    genre: str
    publisher: str
    pages: int = 0
    id: Optional[int] = None  # None при создании, будет присвоен БД

    def __post_init__(self):
        # Валидация данных при создании объекта
        if self.title == "":
            raise ValueError("Название книги не может быть пустым")
        # if not self.author:
        #     raise ValueError("Поле автора не может быть пустым")
        if self.year > datetime.now().year:
            raise ValueError("Год издания не может быть в будущем")




