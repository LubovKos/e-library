import csv
import logging
import os

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class CsvReader:

    def __init__(self, file):
        self.csv_file = file
        logging.info("Инициализация csvreader")

    def load_from_csv(self):
        logging.info(f"Загрузка CSV: {self.csv_file}")
        books = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                required_fields = ['Название книги', 'Автор книги', 'Жанр книги', 'Год выпуска книги']

                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    logging.error(f"Отсутствуют обязательные заголовки: {missing}")
                    raise ValueError("CSV не содержит необходимые заголовки")

                logging.debug(f"Заголовки CSV: {reader.fieldnames}")

                for row in reader:
                    logging.debug(f"Обрабатываем строку: {row}")
                    try:
                        year = int(row['Год выпуска книги'])
                        book = {
                            'title': row['Название книги'].strip(),
                            'author': row['Автор книги'].strip(),
                            'genre': row['Жанр книги'].strip(),
                            'year': year
                        }
                        books.append(book)
                    except (KeyError, ValueError) as e:
                        logging.warning(f"Ошибка парсинга строки: {row}. Ошибка: {str(e)}")
                logging.info(f"Загружено книг из CSV: {len(books)}")
            return books
        except Exception as e:
            logging.error(f"Ошибка при чтении CSV: {str(e)}", exc_info=True)
            return []
