import csv
import json
import logging
import os
import sqlite3

from data_import.csv.book_importer import CSVBookReader
from databases.book_db import BookRepository

#
# # Настройка логирования
# logging.basicConfig(
#     filename='library.log',
#     level=logging.DEBUG,
#     format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
# )
#
#
# class Library:
#     def __init__(self):
#         self.books = []
#         logging.info("Инициализация библиотеки")
#
#     def load_books(self, file_path):
#         logging.info(f"Начало загрузки файла: {file_path}")
#         try:
#             _, ext = os.path.splitext(file_path)
#             logging.debug(f"Расширение файла: {ext}")
#             if ext.lower() not in ['.csv', '.json']:
#                 logging.error(f"Неподдерживаемое расширение: {ext}")
#                 raise ValueError("Неверное расширение файла. Ожидаются .csv или .json")
#
#             if ext.lower() == '.csv':
#                 books = self.load_from_csv(file_path)
#             else:
#                 books = self.load_from_json(file_path)
#
#             logging.info(f"Загружено книг: {len(books)}")
#             return books
#         except Exception as e:
#             logging.error(f"Ошибка при загрузке: {str(e)}", exc_info=True)
#             return []
#
#     def load_from_csv(self, csv_file):
#         logging.info(f"Загрузка CSV: {csv_file}")
#         books = []
#         try:
#             with open(csv_file, 'r', encoding='utf-8-sig') as file:
#                 reader = csv.DictReader(file)
#                 required_fields = ['Название книги', 'Автор книги', 'Жанр книги', 'Год выпуска книги']
#
#                 if not all(field in reader.fieldnames for field in required_fields):
#                     missing = [f for f in required_fields if f not in reader.fieldnames]
#                     logging.error(f"Отсутствуют обязательные заголовки: {missing}")
#                     raise ValueError("CSV не содержит необходимые заголовки")
#
#                 logging.debug(f"Заголовки CSV: {reader.fieldnames}")
#
#                 for row in reader:
#                     logging.debug(f"Обрабатываем строку: {row}")
#                     try:
#                         year = int(row['Год выпуска книги'])
#                         book = {
#                             'title': row['Название книги'].strip(),
#                             'author': row['Автор книги'].strip(),
#                             'genre': row['Жанр книги'].strip(),
#                             'year': year
#                         }
#                         books.append(book)
#                     except (KeyError, ValueError) as e:
#                         logging.warning(f"Ошибка парсинга строки: {row}. Ошибка: {str(e)}")
#                 logging.info(f"Загружено книг из CSV: {len(books)}")
#             return books
#         except Exception as e:
#             logging.error(f"Ошибка при чтении CSV: {str(e)}", exc_info=True)
#             return []
#
#     def load_from_json(self, json_file):
#         logging.info(f"Загрузка JSON: {json_file}")
#         books = []
#         try:
#             with open(json_file, 'r', encoding='utf-8') as file:
#                 data = json.load(file)
#                 for item in data:
#                     logging.debug(f"Обрабатываем элемент JSON: {item}")
#                     try:
#                         books.append({
#                             'title': item['title'].strip(),
#                             'author': item['author'].strip(),
#                             'genre': item['genre'].strip(),
#                             'year': int(item['year'])
#                         })
#                     except (KeyError, ValueError) as e:
#                         logging.warning(f"Ошибка парсинга JSON: {item}. Ошибка: {str(e)}")
#                 logging.info(f"Загружено книг из JSON: {len(books)}")
#             return books
#         except Exception as e:
#             logging.error(f"Ошибка при чтении JSON: {str(e)}", exc_info=True)
#             return []
#
#     def search(self, query, field):
#         logging.info(f"Начало поиска по {field}: {query}")
#         results = []
#         query = query.strip().lower()
#         for book in self.books:
#             if field == 'year':
#                 if str(book['year']).startswith(query):
#                     results.append(book)
#             else:
#                 if query in str(book.get(field, '')).lower():
#                     results.append(book)
#         logging.info(f"Найдено результатов: {len(results)}")
#         return results
#
#     def format_results(self, results):
#         if not results:
#             return "Ничего не найдено"
#         output = f"Найдено: {len(results)}\n"
#         for idx, book in enumerate(results, 1):
#             output += f"{idx}. Название: {book['title']}\n"
#             output += f"   Автор: {book['author']}\n"
#             output += f"   Жанр: {book['genre']}\n"
#             output += f"   Год: {book['year']}\n"
#         return output
#
#
# def main_menu(library):
#     logging.info("Запуск главного меню")
#     while True:
#         print("\nМеню:")
#         print("1. Поиск")
#         print("2. Выход")
#         choice = input("Выберите пункт: ").strip()
#         logging.debug(f"Пользователь выбрал: {choice}")
#
#         if choice == '1':
#             search_menu(library)
#         elif choice == '2':
#             logging.info("Пользователь выбрал выход")
#             logging.info("Программа завершена")
#             break
#         else:
#             logging.warning(f"Неверный выбор: {choice}")
#             print("Неверный выбор")
#
#
# def search_menu(library):
#     logging.info("Запуск меню поиска")
#     while True:
#         print("\nПоиск:")
#         print("1. По названию")
#         print("2. По жанру")
#         print("3. По автору")
#         print("4. По годам")
#         print("0. Назад")
#         choice = input("Выберите пункт: ").strip()
#         logging.debug(f"Пользователь выбрал: {choice}")
#
#         if choice == '0':
#             logging.info("Возврат в главное меню")
#             break
#         elif choice in ['1', '2', '3', '4']:
#             field_map = {
#                 '1': 'title',
#                 '2': 'genre',
#                 '3': 'author',
#                 '4': 'year'
#             }
#             field = field_map[choice]
#
#             if field == 'year':
#                 query = input("Введите год (например '2000' или диапазон '2000-2020'): ").strip()
#             else:
#                 query = input(f"Введите {field}: ").strip()
#
#             logging.info(f"Поиск по {field}: {query}")
#             results = library.search(query, field)
#             formatted = library.format_results(results)
#             print(formatted)
#             logging.info(f"Результаты поиска: {len(results)} записей")
#         else:
#             logging.warning(f"Неверный выбор: {choice}")
#             print("Неверный выбор")
#
#
# def import_data(library):
#     logging.info("Запуск импорта данных")
#     while True:
#         print("\nИмпорт данных:")
#         path = input("Введите путь к файлу (CSV/JSON): ").strip()
#         logging.debug(f"Пользователь ввел путь: {path}")
#
#         if not path:
#             logging.warning("Путь не указан")
#             print("Путь не указан")
#             continue
#
#         if not os.path.isfile(path):
#             logging.error(f"Файл не найден: {path}")
#             print(f"Файл '{path}' не найден")
#             continue
#
#         books = library.load_books(path)
#         if books:
#             library.books = books
#             logging.info(f"Успешно загружено {len(books)} книг")
#             return True
#         else:
#             logging.error("Файл пуст или содержит ошибки")
#             print("Файл пуст или содержит ошибки")
#             continue
#
#
# def main():
#     library = Library()
#
#     # Импорт данных до запуска меню
#     while True:
#         logging.info("Инициализация импорта данных")
#         print("Для начала работы импортируйте базу данных:")
#         if import_data(library):
#             break
#
#     main_menu(library)
#
#
# if __name__ == "__main__":
#     logging.info("Запуск программы")
#     main()



repo = BookRepository()

importer = CSVBookReader("data/csv/test_books.csv", repo)

# Импорт
importer.load_from_csv()
repo.show_all()

