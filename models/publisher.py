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
        if self.name == "":
            raise ValueError("Название издательства не должно быть пустым")
        # todo: можно задушнить и сделать проверку на корректность телефона и почты





