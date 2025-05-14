import csv
import logging
from tables.book_db import BookRepository
from models.book import Book

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class CSVBookReader:

    def __init__(self, file, repo: BookRepository):
        self.repo = repo
        self.csv_file = file
        logging.info("Initialization csvreader")

    def load_from_csv(self):
        logging.info(f"Downloading CSV: {self.csv_file}")
        books = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                required_fields = ['Название книги', 'Автор книги', 'Жанр книги', 'Год выпуска книги',
                                   'Страниц', 'Описание', 'Издательство']

                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    logging.error(f"Missing required fields: {missing}")
                    raise ValueError("CSV does not contain required headers")

                logging.debug(f"Fieldnames CSV: {reader.fieldnames}")
                for row in reader:
                    logging.debug(f"Process the line: {row}")
                    try:
                        year = int(row['Год выпуска книги'])
                        book = {
                            'title': row['Название книги'].strip(),
                            'author': row['Автор книги'].strip(),
                            'genre': row['Жанр книги'].strip(),
                            'year': year,
                            'pages': int(row['Страниц'].strip()),
                            'description': row['Описание'].strip(),
                            'publisher': row['Издательство'].strip()
                        }
                        books.append(book)

                        book2 = Book(
                            title=book['title'],
                            author=book['author'],
                            year=book['year'],
                            genre=book['genre'],
                            pages=book['pages'],
                            description=book['description'],
                            publisher=book['publisher']
                        )
                        self.repo.save(book2)
                    except (KeyError, ValueError) as e:
                        logging.warning(f"Error parsing string: {row}. Error: {str(e)}")
                logging.info(f"Downloaded books from CSV: {len(books)}")
            return books
        except Exception as e:
            logging.error(f"Error reading CSV: {str(e)}", exc_info=True)
            return []
