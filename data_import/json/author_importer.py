# -*- coding: utf-8 -*-
import logging
import ijson
from jsonschema import validate
from tables.author_db import AuthorRepository
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
        logging.info("Initialization jsonreader")

    def load_from_json(self):
        logging.info(f"Downloading JSON: {self.json_file}")
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
                        logging.warning(f"Missing fields in the row {row_number}: {missing_fields}")
                        raise ValueError("JSON does not contain required headers")
                    logging.debug(f"Process line: {row_number}")
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
                        logging.warning(f"Error parsing string: {row_number}. Error: {str(e)}")
                logging.info(f"Downloaded authors from JSON: {len(authors)}")
                return authors

        except Exception as e:
            logging.error(f"Error reading JSON: {str(e)}", exc_info=True)
            return []
