from dataclasses import dataclass
from typing import Optional


@dataclass
class Genre:
    """Модель жанра с базовой валидацией"""
    title: str
    description: str
    id: Optional[int] = None  # None при создании, будет присвоен БД

    def __post_init__(self):
        # Валидация данных при создании объекта
        if self.title == "":
            raise ValueError("Genre name must not be empty")



