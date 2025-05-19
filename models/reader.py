from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Reader:
    """Модель читателя с базовой валидацией"""
    full_name: str
    phone: str
    mail: str
    id: Optional[int] = None  # None при создании, будет присвоен БД

    def __post_init__(self):
        # Валидация данных при создании объекта
        if self.full_name == "":
            raise ValueError("Reader name must not be empty")
        # Регулярное выражение
        pattern = re.compile(r"^\S+@\S+\.\S+$")
        # Проводим проверку электронного адреса
        is_valid = pattern.match(self.mail)
        if not is_valid:
            raise ValueError("Incorrect mail")


