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
        logging.info("Initialization jsonreader")

    def load_from_json(self):
        logging.info(f"Downloading JSON: {self.json_file}")
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
                        logging.warning(f"Missing fields in the row {row_number}: {missing_fields}")
                        raise ValueError("JSON does not contain required headers")

                    logging.debug(f"Process the line: {row_number}")
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
                        logging.warning(f"Error parsing string: {row_number}. Error: {str(e)}")
                logging.info(f"Downloaded readers from JSON: {len(readers)}")
                return readers

        except Exception as e:
            logging.error(f"Error reading JSON: {str(e)}", exc_info=True)
            return []
