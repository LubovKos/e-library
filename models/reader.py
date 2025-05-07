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
        if self.full_name == "":
            raise ValueError("Имя читателя не должно быть пустым")
        # TODO: опять же душная проверка телефона и почты


