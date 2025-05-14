import csv
import logging

from tables.reader_db import ReaderRepository
from models.reader import Reader

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class CSVReaderImporter:

    def __init__(self, file, repo: ReaderRepository):
        self.csv_file = file
        self.repo = repo
        logging.info("Initialization csvreader")

    def load_from_csv(self):
        logging.info(f"Downloading CSV: {self.csv_file}")
        book_readers = []
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                required_fields = ['ФИО', 'Телефон', 'Почта']

                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    logging.error(f"Missing fields in the row: {missing}")
                    raise ValueError("CSV does not contain required headers")

                logging.debug(f"Fieldnames of CSV: {reader.fieldnames}")

                for row in reader:
                    logging.debug(f"Process the line: {row}")
                    try:
                        book_reader = {
                            'full_name': row['ФИО'].strip(),
                            'phone': row['Телефон'].strip(),
                            'mail': row['Почта'].strip()
                        }
                        book_reader = Reader(full_name=book_reader['full_name'],
                                             phone=book_reader['phone'],
                                             mail=book_reader['mail'])
                        book_readers.append(book_reader)
                        self.repo.save(book_reader)
                    except (KeyError, ValueError) as e:
                        logging.warning(f"Error parsing string: {row}. Error: {str(e)}")
                logging.info(f"Downloaded readers from CSV: {len(book_readers)}")
            return book_readers
        except Exception as e:
            logging.error(f"Error reading CSV: {str(e)}", exc_info=True)
            return []
