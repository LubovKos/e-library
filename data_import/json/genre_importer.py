# -*- coding: utf-8 -*-
import logging
import ijson
from tables.genre_db import GenreRepository
from models.genre import Genre

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class JSONGenreReader:

    def __init__(self, file, repo: GenreRepository):
        self.repo = repo
        self.json_file = file
        logging.info("Инициализация jsonreader")

    def load_from_json(self):
        logging.info(f"Загрузка JSON: {self.json_file}")
        genres = []
        try:
            with open(self.json_file, 'r') as file:
                parser = ijson.items(file, 'item')
                row_number = 1
                for genre in parser:
                    required_fields = {
                        "Название",
                        "Описание"
                    }

                    # Проверка наличия всех полей
                    missing_fields = required_fields - set(genre.keys())
                    if missing_fields:
                        logging.warning(f"Отсутствуют поля в строке {row_number}: {missing_fields}")
                        raise ValueError("JSON не содержит необходимые заголовки")

                    logging.debug(f"Обрабатываем строку: {row_number}")
                    row_number += 1
                    try:
                        genre = Genre(
                            title=genre['Название'],
                            description=genre['Описание']
                        )
                        self.repo.save(genre)
                        genres.append(genre)

                    except (KeyError, ValueError) as e:
                        logging.warning(f"Ошибка парсинга строки: {row_number}. Ошибка: {str(e)}")
                logging.info(f"Загружено жанров из JSON: {len(genres)}")
                return genres

        except Exception as e:
            logging.error(f"Ошибка при чтении JSON: {str(e)}", exc_info=True)
            return []

#
# repo = GenreRepository()
# importer = JSONGenreReader("C:/Users/student/PycharmProjects/booksdb/data/json/genres.json", repo)
# # Импорт
# importer.load_from_json()
# repo.show_all()
# repo.delete("title", "Юмор")
# repo.show_all()
# repo.filter("title", "up")
# repo.find("title", "Роман")
