# -*- coding: utf-8 -*-
import logging
import ijson
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
        logging.info("Initialization jsonreader")

    def load_from_json(self):
        logging.info(f"Downloading JSON: {self.json_file}")
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
                        logging.warning(f"Missing fields in the row {row_number}: {missing_fields}")
                        raise ValueError("JSON does not contain required headers")

                    logging.debug(f"Process the line: {row_number}")
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
                        logging.warning(f"Error parsing string: {row_number}. Error: {str(e)}")
                logging.info(f"Downloaded publishers from JSON: {len(publishers)}")
                return publishers

        except Exception as e:
            logging.error(f"Error reading JSON: {str(e)}", exc_info=True)
            return []
