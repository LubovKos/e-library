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
        logging.info("Инициализация csvreader")

    def load_from_csv(self):
        logging.info(f"Загрузка CSV: {self.csv_file}")
        genres = []
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                required_fields = ['Название','Описание']

                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    logging.error(f"Отсутствуют обязательные заголовки: {missing}")
                    raise ValueError("CSV не содержит необходимые заголовки")

                logging.debug(f"Заголовки CSV: {reader.fieldnames}")

                for row in reader:
                    logging.debug(f"Обрабатываем строку: {row}")
                    try:
                        genre = {
                            'title': row['Название'].strip(),
                            'description': row['Описание'].strip()
                        }
                        genre = Genre(title=genre['title'],
                                        description=genre['description'])
                        genres.append(genre)
                        self.repo.save(genre)
                    except (KeyError, ValueError) as e:
                        logging.warning(f"Ошибка парсинга строки: {row}. Ошибка: {str(e)}")
                logging.info(f"Загружено жанров из CSV: {len(genres)}")
            return genres
        except Exception as e:
            logging.error(f"Ошибка при чтении CSV: {str(e)}", exc_info=True)
            return []


# test
# repo = GenreRepository()
# importer = CSVGenreReader("C:/Users/student/PycharmProjects/booksdb/data/csv/test_genres.csv", repo)
# # Импорт
# importer.load_from_csv()
# repo.show_all()
# repo.delete("title", "Юмор")
# repo.show_all()
# repo.filter("title", "up")
# repo.find("title", "Роман")
#


