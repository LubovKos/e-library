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
        logging.info("Initialization jsonreader")

    def load_from_json(self):
        logging.info(f"Downloading JSON: {self.json_file}")
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
                        logging.warning(f"Missing fields in the row {row_number}: {missing_fields}")
                        raise ValueError("JSON does not contain required headers")

                    logging.debug(f"Process the line: {row_number}")
                    row_number += 1
                    try:
                        genre = Genre(
                            title=genre['Название'],
                            description=genre['Описание']
                        )
                        self.repo.save(genre)
                        genres.append(genre)

                    except (KeyError, ValueError) as e:
                        logging.warning(f"Error parsing string: {row_number}. Error: {str(e)}")
                logging.info(f"Downloaded genres from JSON: {len(genres)}")
                return genres

        except Exception as e:
            logging.error(f"Error reading JSON: {str(e)}", exc_info=True)
            return []
