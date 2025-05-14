import csv
import logging

from tables.author_db import AuthorRepository
from models.author import Author

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class CSVAuthorReader:

    def __init__(self, file, repo: AuthorRepository):
        self.csv_file = file
        self.repo = repo
        logging.info("Initialization csvreader")

    def load_from_csv(self):
        logging.info(f"Downloading CSV: {self.csv_file}")
        authors = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                required_fields = ['ФИО', 'Дата рождения', 'Дата смерти', 'Биография']

                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    logging.error(f"Missing required fields: {missing}")
                    raise ValueError("CSV does not contain required headers")

                logging.debug(f"Fieldnames CSV: {reader.fieldnames}")

                for row in reader:
                    logging.debug(f"Process the line: {row}")
                    try:
                        author = {
                            'full_name': row['ФИО'].strip(),
                            'date_of_birth': row['Дата рождения'].strip(),
                            'date_of_death': row['Дата смерти'].strip(),
                            'biography': row['Биография'].strip()
                        }
                        author = Author(full_name=author['full_name'],
                                        date_of_birth=author['date_of_birth'],
                                        date_of_death=author['date_of_death'],
                                        biography=author['biography'])
                        authors.append(author)
                        self.repo.save(author)
                    except (KeyError, ValueError) as e:
                        logging.warning(f"Error parsing string: {row}. Error: {str(e)}")
                logging.info(f"Downloaded authors from CSV: {len(authors)}")
            return authors
        except Exception as e:
            logging.error(f"Error reading CSV: {str(e)}", exc_info=True)
            return []
