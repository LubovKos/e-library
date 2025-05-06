import logging
import ijson
from jsonschema import validate
from databases.book_db import BookRepository
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
        logging.info("Инициализация jsonreader")

    def load_from_json(self):
        logging.info(f"Загрузка JSON: {self.json_file}")
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
                        logging.warning(f"Отсутствуют поля в строке {row_number}: {missing_fields}")
                        raise ValueError("JSON не содержит необходимые заголовки")


                    logging.debug(f"Обрабатываем строку: {row_number}")
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
                        logging.warning(f"Ошибка парсинга строки: {row_number}. Ошибка: {str(e)}")
                logging.info(f"Загружено книг из JSON: {len(books)}")
                return books

        except Exception as e:
            logging.error(f"Ошибка при чтении JSON: {str(e)}", exc_info=True)
            return []


# test
repo = BookRepository()
importer = JSONBookReader("books.json", repo)
# Импорт
importer.load_from_json()
repo.show_all()

