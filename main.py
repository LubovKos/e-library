import logging
import os
import json
import csv

from data_import.csv.author_importer import CSVAuthorReader
from data_import.csv.book_importer import CSVBookReader
from data_import.csv.genre_importer import CSVGenreReader
from data_import.csv.publisher_importer import CSVPublisherReader
from data_import.csv.reader_importer import CSVReaderImporter
from data_import.json.book_importer import JSONBookReader
from data_import.json.author_importer import JSONAuthorReader
from data_import.json.genre_importer import JSONGenreReader
from data_import.json.publisher_importer import JSONPublisherReader
from data_import.json.reader_importer import JSONReaderImporter
from databases.book_db import BookRepository
from databases.author_db import AuthorRepository
from databases.publisher_db import PublisherRepository
from databases.genre_db import GenreRepository
from databases.reader_db import ReaderRepository
from csv import *

# Настройка логирования
logging.basicConfig(
    filename='library.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s'
)

class Library:
    def __init__(self):
        self.book_repo = BookRepository()
        self.author_repo = AuthorRepository()
        self.publisher_repo = PublisherRepository()
        self.genre_repo = GenreRepository()
        self.reader_repo = ReaderRepository()
        self.path = "C:/Users/student/PycharmProjects/booksdb/data/"

    def load(self, path, choice):
        try:
            if path.endswith('.json'):
                if choice == '1':
                    data = JSONBookReader(path, self.book_repo)
                elif choice == '2':
                    data = JSONAuthorReader(path, self.author_repo)
                elif choice == '3':
                    data = JSONPublisherReader(path, self.publisher_repo)
                elif choice == '4':
                    data = JSONGenreReader(path, self.genre_repo)
                else:
                    data = JSONReaderImporter(path, self.reader_repo)
                return data.load_from_json()
            elif path.endswith('.csv'):
                if choice == '1':
                    data = CSVBookReader(path, self.book_repo)
                elif choice == '2':
                    data = CSVAuthorReader(path, self.author_repo)
                elif choice == '3':
                    data = CSVPublisherReader(path, self.publisher_repo)
                elif choice == '4':
                    data = CSVGenreReader(path, self.genre_repo)
                else:
                    data = CSVReaderImporter(path, self.reader_repo)
                return data.load_from_csv()
            else:
                logging.error("Unsupported file format")
                return []
        except Exception as e:
            logging.error(f"Error loading file {path}: {e}")
            return []

    def search(self, query, field, entity_type='book'):
        """Search records by field and entity type."""
        return

    def add_record(self, entity_type, record):
        """Add a new record to the specified entity."""
        return

    def update_record(self, entity_type, index, record):
        """Update an existing record."""
        return

    def delete_record(self, entity_type, index):
        """Delete a record by index."""
        return

    def display_all(self, choice):
        try:
            if choice == '1':
                self.book_repo.show_all()
            elif choice == '2':
                self.author_repo.show_all()
            elif choice == '3':
                self.publisher_repo.show_all()
            elif choice == '4':
                self.genre_repo.show_all()
            else:
                self.reader_repo.show_all()
        except Exception as e:
            logging.error(f"Error displaying: {e}")


def main_menu(library):
    logging.info("Starting main menu")
    while True:
        print("\nLibrary Management System:")
        print("1. Import data")
        print("2. Display All Records")
        print("3. Add Record")
        print("4. Update Record")
        print("5. Delete Record")
        print("6. Search Records")
        print("7. Exit")
        choice = input("Select an option: ").strip()
        logging.debug(f"User selected: {choice}")

        if choice == '1':
            import_data(library)
        elif choice == '2':
            display_records_menu(library)
        elif choice == '3':
            add_record_menu(library)
        elif choice == '4':
            update_record_menu(library)
        elif choice == '5':
            delete_record_menu(library)
        elif choice == '6':
            search_menu(library)
        elif choice == '7':
            logging.info("User chose to exit")
            print("Goodbye!")
            break
        else:
            logging.warning(f"Invalid choice: {choice}")
            print("Invalid choice")


def search_menu(library):
    logging.info("Starting search menu")
    entity_types = {'1': 'book', '2': 'author', '3': 'publisher', '4': 'genre', '5': 'reader'}
    while True:
        print("\nSearch by Entity:")
        print("1. Book")
        print("2. Author")
        print("3. Publisher")
        print("4. Genre")
        print("5. Reader")
        print("0. Back")
        choice = input("Select entity: ").strip()
        logging.debug(f"User selected entity: {choice}")

        if choice == '0':
            logging.info("Returning to main menu")
            break
        elif choice in entity_types:
            entity = entity_types[choice]
            print(f"\nSearch {entity.capitalize()} by:")
            field_options = {
                'book': {'1': 'title', '2': 'genre', '3': 'author', '4': 'year'},
                'author': {'1': 'name', '2': 'birth_year'},
                'publisher': {'1': 'name', '2': 'city'},
                'genre': {'1': 'name'},
                'reader': {'1': 'name', '2': 'email'}
            }
            for k, v in field_options[entity].items():
                print(f"{k}. {v.capitalize()}")
            print("0. Back")
            field_choice = input("Select field: ").strip()

            if field_choice == '0':
                continue
            elif field_choice in field_options[entity]:
                field = field_options[entity][field_choice]
                query = input(f"Enter {field} (e.g., '2000' or '2000-2020' for year): ").strip()
                logging.info(f"Searching {entity} by {field}: {query}")
                results = library.search(query, field, entity)
                print(library.format_results(results))
                logging.info(f"Search results: {len(results)} {entity} records")
            else:
                logging.warning(f"Invalid field choice: {field_choice}")
                print("Invalid field choice")
        else:
            logging.warning(f"Invalid entity choice: {choice}")
            print("Invalid entity choice")


def import_data(library):
    logging.info("Starting data import")
    entity_types = {'1': 'book', '2': 'author', '3': 'publisher', '4': 'genre', '5': 'reader'}
    while True:
        print("\nImport Data for:")
        print("1. Books")
        print("2. Authors")
        print("3. Publishers")
        print("4. Genres")
        print("5. Readers")
        print("0. Back")
        choice = input("Select entity: ").strip()
        logging.debug(f"User selected entity for import: {choice}")

        if choice == '0':
            logging.info("Returning to main menu")
            break
        elif choice in entity_types:
            entity = entity_types[choice]
            path = library.path + input("Enter path to CSV/JSON file: ")
            logging.debug(f"User entered path: {path}")

            if not path:
                logging.warning("Path not provided")
                print("Path not provided")
                continue
            if not os.path.isfile(path):
                logging.error(f"File not found: {path}")
                print(f"File '{path}' not found")
                continue

            data = library.load(path, choice)
            if len(data) != 0:
                setattr(library, entity + 's', data)
                logging.info(f"Successfully imported {len(data)} {entity} records")
                print(f"Imported {len(data)} {entity} records")
                break
            else:
                logging.error("File is empty or contains errors")
                print("File is empty or contains errors")
        else:
            logging.warning(f"Invalid entity choice: {choice}")
            print("Invalid entity choice")


def add_record_menu(library):
    logging.info("Starting add record menu")
    entity_types = {'1': 'book', '2': 'author', '3': 'publisher', '4': 'genre', '5': 'reader'}
    print("\nAdd Record for:")
    for k, v in entity_types.items():
        print(f"{k}. {v.capitalize()}")
    print("0. Back")
    choice = input("Select entity: ").strip()

    if choice == '0':
        return
    if choice not in entity_types:
        logging.warning(f"Invalid entity choice: {choice}")
        print("Invalid entity choice")
        return

    entity = entity_types[choice]
    record = {}
    # fields = {
    #     'book': ['title', 'genre', 'author', 'year'],
    #     'author': ['name', 'birth_year'],
    #     'publisher': ['name', 'city'],
    #     'genre': ['name'],
    #     'reader': ['name', 'email']
    # }
    # for field in fields[entity]:
    #     value = input(f"Enter {field}: ").strip()
    #     record[field] = value
    library.add_record(entity, record)
    print(f"{entity.capitalize()} added successfully")


def update_record_menu(library):
    logging.info("Starting update record menu")
    entity_types = {'1': 'book', '2': 'author', '3': 'publisher', '4': 'genre', '5': 'reader'}
    print("\nUpdate Record for:")
    for k, v in entity_types.items():
        print(f"{k}. {v.capitalize()}")
    print("0. Back")
    choice = input("Select entity: ").strip()

    if choice == '0':
        return
    if choice == '1':
        print("Necessary data: title, author")
    if choice not in entity_types:
        logging.warning(f"Invalid entity choice: {choice}")
        print("Invalid entity choice")
        return

    entity = entity_types[choice]
    data = getattr(library, entity + 's')
    print(library.format_results(data))
    index = input("Enter index of record to update: ").strip()
    if not index.isdigit():
        logging.warning("Invalid index")
        print("Invalid index")
        return
    index = int(index)

    record = {}
    # fields = {
    #     'book': ['title', 'genre', 'author', 'year'],
    #     'author': ['name', 'birth_year'],
    #     'publisher': ['name', 'city'],
    #     'genre': ['name'],
    #     'reader': ['name', 'email']
    # }
    # for field in fields[entity]:
    #     value = input(f"Enter new {field}: ").strip()
    #     record[field] = value
    if library.update_record(entity, index, record):
        print(f"{entity.capitalize()} updated successfully")
    else:
        print("Failed to update record")


def delete_record_menu(library):
    logging.info("Starting delete record menu")
    entity_types = {'1': 'book', '2': 'author', '3': 'publisher', '4': 'genre', '5': 'reader'}
    print("\nDelete Record for:")
    for k, v in entity_types.items():
        print(f"{k}. {v.capitalize()}")
    print("0. Back")
    choice = input("Select entity: ").strip()

    if choice == '0':
        return
    if choice not in entity_types:
        logging.warning(f"Invalid entity choice: {choice}")
        print("Invalid entity choice")
        return

    # entity = entity_types[choice]
    # data = getattr(library, entity + 's')
    # print(library.format_results(data))
    # index = input("Enter index of record to delete: ").strip()
    # if not index.isdigit():
    #     logging.warning("Invalid index")
    #     print("Invalid index")
    #     return
    # index = int(index)
    # if library.delete_record(entity, index):
    #     print(f"{entity.capitalize()} deleted successfully")
    # else:
    #     print("Failed to delete record")


def display_records_menu(library):
    logging.info("Starting display records menu")
    entity_types = {'1': 'book', '2': 'author', '3': 'publisher', '4': 'genre', '5': 'reader'}
    print("\nDisplay Records for:")
    for k, v in entity_types.items():
        print(f"{k}. {v.capitalize()}")
    print("0. Back")
    choice = input("Select entity: ").strip()

    if choice == '0':
        return
    if choice not in entity_types:
        logging.warning(f"Invalid entity choice: {choice}")
        print("Invalid entity choice")
        return

    entity = entity_types[choice]
    library.display_all(choice)
    logging.info(f"Displayed {entity} records")


def main():
    library = Library()
    logging.info("Program started")
    print("Welcome to the Library Management System")
    main_menu(library)


if __name__ == "__main__":
    main()
