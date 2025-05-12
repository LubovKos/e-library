# -*- coding: utf-8 -*-
import logging
import ijson
from jsonschema import validate
from databases.author_db import AuthorRepository
from models.author import Author

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class JSONAuthorReader:

    def __init__(self, file, repo: AuthorRepository):
        self.repo = repo
        self.json_file = file
        logging.info("Инициализация jsonreader")

    def load_from_json(self):
        logging.info(f"Загрузка JSON: {self.json_file}")
        authors = []
        try:
            with open(self.json_file, 'r') as file:
                parser = ijson.items(file, 'item')
                row_number = 1
                for author in parser:
                    required_fields = {
                        "ФИО",
                        "Дата рождения",
                        "Дата смерти",
                        "Биография"
                    }

                    # Проверка наличия всех полей
                    missing_fields = required_fields - set(author.keys())
                    if missing_fields:
                        logging.warning(f"Отсутствуют поля в строке {row_number}: {missing_fields}")
                        raise ValueError("JSON не содержит необходимые заголовки")


                    logging.debug(f"Обрабатываем строку: {row_number}")
                    row_number += 1
                    try:
                        author = Author(
                            full_name=author['ФИО'],
                            date_of_birth=author['Дата рождения'],
                            date_of_death=author['Дата смерти'],
                            biography=author['Биография']
                        )
                        self.repo.save(author)
                        authors.append(author)

                    except (KeyError, ValueError) as e:
                        logging.warning(f"Ошибка парсинга строки: {row_number}. Ошибка: {str(e)}")
                logging.info(f"Загружено авторов из JSON: {len(authors)}")
                return authors

        except Exception as e:
            logging.error(f"Ошибка при чтении JSON: {str(e)}", exc_info=True)
            return []


# test
repo = AuthorRepository()
importer = JSONAuthorReader("../../data/json/authors.json", repo)
# Импорт
importer.load_from_json()
repo.show_all()

