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
        logging.info("Инициализация csvreader")

    def load_from_csv(self):
        logging.info(f"Загрузка CSV: {self.csv_file}")
        authors = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                required_fields = ['ФИО','Дата рождения','Дата смерти','Биография']

                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    logging.error(f"Отсутствуют обязательные заголовки: {missing}")
                    raise ValueError("CSV не содержит необходимые заголовки")

                logging.debug(f"Заголовки CSV: {reader.fieldnames}")

                for row in reader:
                    logging.debug(f"Обрабатываем строку: {row}")
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
                        logging.warning(f"Ошибка парсинга строки: {row}. Ошибка: {str(e)}")
                logging.info(f"Загружено авторов из CSV: {len(authors)}")
            return authors
        except Exception as e:
            logging.error(f"Ошибка при чтении CSV: {str(e)}", exc_info=True)
            return []


# test
# repo = AuthorRepository()
# importer = CSVAuthorReader("C:/Users/student/PycharmProjects/booksdb/data/csv/test_authors.csv", repo)
# # Импорт
# importer.load_from_csv()
# repo.show_all()
# repo.update("date_of_birth", "Михаил Афанасьевич Булгаков", "09.09.1881")
# repo.show_all()
# repo.delete("date_of_birth", "09.09.1881")
# repo.show_all()
# repo.filter("full_name", "down")

