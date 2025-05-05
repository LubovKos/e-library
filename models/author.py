from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Author:
    """Модель книги с базовой валидацией"""
    full_name: str
    biography: str
    date_of_birth: int
    date_of_death: str
    id: Optional[int] = None  # None при создании, будет присвоен БД