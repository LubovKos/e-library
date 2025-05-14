import logging
import ijson
from jsonschema import validate
from tables.book_db import BookRepository
from models.book import Book

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class JSONBookReader:

    def __init__(self, file, repo: BookRepository):
        self.repo = repo
        self.json_file = file
        logging.info("Initialization jsonreader")

    def load_from_json(self):
        logging.info(f"Downloading JSON: {self.json_file}")
        books = []
        try:
            with open(self.json_file, 'r') as file:
                parser = ijson.items(file, 'item')
                row_number = 1
                for book in parser:
                    schema = {
                        "required": ["Название книги"]
                    }

                    required_fields = {
                        "Название книги",
                        "Автор книги",
                        "Жанр книги",
                        "Год выпуска книги",
                        "Страниц",
                        "Описание",
                        "Издательство"
                    }

                    # Проверка наличия всех полей
                    missing_fields = required_fields - set(book.keys())
                    if missing_fields:
                        logging.warning(f"Missing fields in the row {row_number}: {missing_fields}")
                        raise ValueError("JSON does not contain required headers")
                    logging.debug(f"Process line: {row_number}")
                    row_number += 1
                    try:
                        book = Book(
                            title=book['Название книги'],
                            author=book['Автор книги'],
                            year=book['Год выпуска книги'],
                            genre=book['Жанр книги'],
                            pages=book['Страниц'],
                            description=book['Описание'],
                            publisher=book['Издательство']
                        )
                        self.repo.save(book)
                        books.append(book)

                    except (KeyError, ValueError) as e:
                        logging.warning(f"Error parsing string: {row_number}. Error: {str(e)}")
                logging.info(f"Downloaded books from JSON: {len(books)}")
                return books

        except Exception as e:
            logging.error(f"Error reading JSON: {str(e)}", exc_info=True)
            return []


# test
# repo = BookRepository()
# importer = JSONBookReader("../../data/json/books.json", repo)
# # Импорт
# importer.load_from_json()
# repo.show_all()
# repo.update("pages", "Преступление и наказание", "Фёдор Достоевский", 608)
# repo.show_all()
# repo.delete("title", "Мастер и Маргарита")
# repo.show_all()
# repo.find("pages", 480)

