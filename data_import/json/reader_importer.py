# -*- coding: utf-8 -*-
import logging
import ijson
from tables.reader_db import ReaderRepository
from models.reader import Reader

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class JSONReaderImporter:

    def __init__(self, file, repo: ReaderRepository):
        self.repo = repo
        self.json_file = file
        logging.info("Инициализация jsonreader")

    def load_from_json(self):
        logging.info(f"Загрузка JSON: {self.json_file}")
        readers = []
        try:
            with open(self.json_file, 'r') as file:
                parser = ijson.items(file, 'item')
                row_number = 1
                for reader in parser:
                    required_fields = {
                        "ФИО",
                        "Телефон",
                        "Почта"
                    }

                    # Проверка наличия всех полей
                    missing_fields = required_fields - set(reader.keys())
                    if missing_fields:
                        logging.warning(f"Отсутствуют поля в строке {row_number}: {missing_fields}")
                        raise ValueError("JSON не содержит необходимые заголовки")

                    logging.debug(f"Обрабатываем строку: {row_number}")
                    row_number += 1
                    try:
                        reader = Reader(
                            full_name=reader['ФИО'],
                            phone=reader['Телефон'],
                            mail=reader['Почта']
                        )
                        self.repo.save(reader)
                        readers.append(reader)

                    except (KeyError, ValueError) as e:
                        logging.warning(f"Ошибка парсинга строки: {row_number}. Ошибка: {str(e)}")
                logging.info(f"Загружено издательств из JSON: {len(readers)}")
                return readers

        except Exception as e:
            logging.error(f"Ошибка при чтении JSON: {str(e)}", exc_info=True)
            return []


# test
# repo = ReaderRepository()
# importer = JSONReaderImporter("../../data/json/readers.json", repo)
# # Импорт
# importer.load_from_json()
# repo.show_all()
