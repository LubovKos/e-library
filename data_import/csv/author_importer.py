import csv
import logging

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class CSVAuthorReader:

    def __init__(self, file):
        self.csv_file = file
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
                        authors.append(author)
                    except (KeyError, ValueError) as e:
                        logging.warning(f"Ошибка парсинга строки: {row}. Ошибка: {str(e)}")
                logging.info(f"Загружено авторов из CSV: {len(authors)}")
            return authors
        except Exception as e:
            logging.error(f"Ошибка при чтении CSV: {str(e)}", exc_info=True)
            return []


b = CSVAuthorReader("../../data/csv/test_authors.csv")
authors = b.load_from_csv()
print(*authors)