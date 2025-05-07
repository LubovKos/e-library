import csv
import logging

from databases.reader_db import ReaderRepository
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
        logging.info("Инициализация csvreader")

    def load_from_csv(self):
        logging.info(f"Загрузка CSV: {self.csv_file}")
        book_readers = []
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                required_fields = ['ФИО','Телефон','Почта']

                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    logging.error(f"Отсутствуют обязательные заголовки: {missing}")
                    raise ValueError("CSV не содержит необходимые заголовки")

                logging.debug(f"Заголовки CSV: {reader.fieldnames}")

                for row in reader:
                    logging.debug(f"Обрабатываем строку: {row}")
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
                        logging.warning(f"Ошибка парсинга строки: {row}. Ошибка: {str(e)}")
                logging.info(f"Загружено издательств из CSV: {len(book_readers)}")
            return book_readers
        except Exception as e:
            logging.error(f"Ошибка при чтении CSV: {str(e)}", exc_info=True)
            return []


repo = ReaderRepository()

b = CSVReaderImporter("C:/Users/student/PycharmProjects/booksdb/data/csv/test_readers.csv", repo)
b.load_from_csv()
repo.show_all()