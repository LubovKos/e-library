from dataclasses import dataclass
from typing import Optional
import re

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
            raise ValueError("Publisher name must not be empty")
        # Регулярное выражение
        pattern = re.compile(r"^\S+@\S+\.\S+$")
        # Проводим проверку электронного адреса
        is_valid = pattern.match(self.mail)
        if not is_valid:
            raise ValueError("Incorrect mail")





