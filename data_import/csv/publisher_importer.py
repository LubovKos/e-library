import csv
import logging

from tables.publisher_db import PublisherRepository
from models.publisher import Publisher

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class CSVPublisherReader:

    def __init__(self, file, repo: PublisherRepository):
        self.csv_file = file
        self.repo = repo
        logging.info("Инициализация csvreader")

    def load_from_csv(self):
        logging.info(f"Загрузка CSV: {self.csv_file}")
        publishers = []
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                required_fields = ['Название','Адрес','Номер телефона','Почта']

                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    logging.error(f"Отсутствуют обязательные заголовки: {missing}")
                    raise ValueError("CSV не содержит необходимые заголовки")

                logging.debug(f"Заголовки CSV: {reader.fieldnames}")

                for row in reader:
                    logging.debug(f"Обрабатываем строку: {row}")
                    try:
                        publisher = {
                            'name': row['Название'].strip(),
                            'address': row['Адрес'].strip(),
                            'phone': row['Номер телефона'].strip(),
                            'mail': row['Почта'].strip()
                        }
                        publisher = Publisher(name=publisher['name'],
                                              address=publisher['address'],
                                              phone=publisher['phone'],
                                              mail=publisher['mail'])
                        publishers.append(publisher)
                        self.repo.save(publisher)
                    except (KeyError, ValueError) as e:
                        logging.warning(f"Ошибка парсинга строки: {row}. Ошибка: {str(e)}")
                logging.info(f"Загружено издательств из CSV: {len(publishers)}")
            return publishers
        except Exception as e:
            logging.error(f"Ошибка при чтении CSV: {str(e)}", exc_info=True)
            return []

#
# repo = PublisherRepository()
# b = CSVPublisherReader("C:/Users/student/PycharmProjects/booksdb/data/csv/test_publishers.csv", repo)
# b.load_from_csv()
# repo.show_all()