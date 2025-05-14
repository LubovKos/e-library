import csv
import logging

from tables.genre_db import GenreRepository
from models.genre import Genre

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class CSVGenreReader:

    def __init__(self, file, repo: GenreRepository):
        self.csv_file = file
        self.repo = repo
        logging.info("initialization csvreader")

    def load_from_csv(self):
        logging.info(f"Downloading CSV: {self.csv_file}")
        genres = []
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                required_fields = ['Название', 'Описание']

                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    logging.error(f"Missing required fields: {missing}")
                    raise ValueError("CSV does not contain required headers")

                logging.debug(f"Fieldnames CSV: {reader.fieldnames}")

                for row in reader:
                    logging.debug(f"Process the line: {row}")
                    try:
                        genre = {
                            'title': row['Название'].strip(),
                            'description': row['Описание'].strip()
                        }
                        genre = Genre(title=genre['title'], description=genre['description'])
                        genres.append(genre)
                        self.repo.save(genre)
                    except (KeyError, ValueError) as e:
                        logging.warning(f"error parsing string: {row}. Error: {str(e)}")
                logging.info(f"Downloaded genres from CSV: {len(genres)}")
            return genres
        except Exception as e:
            logging.error(f"Error reading CSV: {str(e)}", exc_info=True)
            return []
