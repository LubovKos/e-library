from dataclasses import dataclass
from typing import Optional


@dataclass
class Reader:
    """Модель книги с базовой валидацией"""
    full_name: str
    phone: str
    mail: str
    id: Optional[int] = None  # None при создании, будет присвоен БД

    def __post_init__(self):
        # Валидация данных при создании объекта



