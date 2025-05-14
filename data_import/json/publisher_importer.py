# -*- coding: utf-8 -*-
import logging
import ijson
from jsonschema import validate
from tables.publisher_db import PublisherRepository
from models.publisher import Publisher

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class JSONPublisherReader:

    def __init__(self, file, repo: PublisherRepository):
        self.repo = repo
        self.json_file = file
        logging.info("Инициализация jsonreader")

    def load_from_json(self):
        logging.info(f"Загрузка JSON: {self.json_file}")
        publishers = []
        try:
            with open(self.json_file, 'r') as file:
                parser = ijson.items(file, 'item')
                row_number = 1
                for publisher in parser:
                    required_fields = {
                        "Название",
                        "Адрес",
                        "Номер телефона",
                        "Почта"
                    }

                    # Проверка наличия всех полей
                    missing_fields = required_fields - set(publisher.keys())
                    if missing_fields:
                        logging.warning(f"Отсутствуют поля в строке {row_number}: {missing_fields}")
                        raise ValueError("JSON не содержит необходимые заголовки")

                    logging.debug(f"Обрабатываем строку: {row_number}")
                    row_number += 1
                    try:
                        publisher = Publisher(
                            name=publisher['Название'],
                            address=publisher['Адрес'],
                            phone=publisher['Номер телефона'],
                            mail=publisher['Почта']
                        )
                        self.repo.save(publisher)
                        publishers.append(publisher)

                    except (KeyError, ValueError) as e:
                        logging.warning(f"Ошибка парсинга строки: {row_number}. Ошибка: {str(e)}")
                logging.info(f"Загружено издательств из JSON: {len(publishers)}")
                return publishers

        except Exception as e:
            logging.error(f"Ошибка при чтении JSON: {str(e)}", exc_info=True)
            return []


# test
# repo = PublisherRepository()
# importer = JSONPublisherReader("../../data/json/publishers.json", repo)
# # Импорт
# importer.load_from_json()
# repo.show_all()
