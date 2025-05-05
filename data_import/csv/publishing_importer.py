import csv
import logging

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)


class CSVPublisherReader:

    def __init__(self, file):
        self.csv_file = file
        logging.info("Инициализация csvreader")

    def load_from_csv(self):
        logging.info(f"Загрузка CSV: {self.csv_file}")
        publishers = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8-sig') as file:
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
                        publishers.append(publisher)
                    except (KeyError, ValueError) as e:
                        logging.warning(f"Ошибка парсинга строки: {row}. Ошибка: {str(e)}")
                logging.info(f"Загружено издательств из CSV: {len(publishers)}")
            return publishers
        except Exception as e:
            logging.error(f"Ошибка при чтении CSV: {str(e)}", exc_info=True)
            return []


b = CSVPublisherReader("test_publishers.csv")
p = b.load_from_csv()
print(*p)