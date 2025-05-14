from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
            raise ValueError("Book title must not be empty")
        if self.author == "":
            raise ValueError("Author field must not be empty")
        if self.year > datetime.now().year:
            raise ValueError("The year of publication cannot be in the future")




