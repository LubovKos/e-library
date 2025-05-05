from dataclasses import dataclass
from typing import Optional


@dataclass
class Publisher:
    """Модель книги с базовой валидацией"""
    name: str
    address: str
    phone: str
    mail: str
    id: Optional[int] = None  # None при создании, будет присвоен БД

    def __post_init__(self):
        # Валидация данных при создании объекта
        if not self.title:
            raise ValueError("Название книги не может быть пустым")


