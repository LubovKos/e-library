from dataclasses import dataclass
from datetime import datetime as dt
from typing import Optional, List


@dataclass
class Author:
    """Модель книги с базовой валидацией"""
    full_name: str
    biography: str
    date_of_birth: str
    date_of_death: str

    def __post_init__(self):
        # Валидация данных при создании объекта
        if self.full_name == "":
            raise ValueError("ФИО автора не может быть пустым")
        print(len(self.date_of_death))
        if len(self.date_of_birth) != 0 and len(self.date_of_death) != 0:
            if dt.strptime(self.date_of_birth, '%d.%m.%Y') > dt.strptime(self.date_of_death, '%d.%m.%Y'):
                raise ValueError("Дата смерти не может быть раньше даты рождения")
        if len(self.date_of_birth) != 0 and dt.strptime(self.date_of_birth, '%d.%m.%Y') > dt.now():
            raise ValueError("Дата рождения не может быть в будущем")
        if len(self.date_of_death) != 0 and dt.strptime(self.date_of_death, '%d.%m.%Y') > dt.now():
            raise ValueError("Дата смерти не может быть в будущем")