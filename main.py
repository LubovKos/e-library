import logging
import os
import traceback

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
from tables.book_db import BookRepository
from tables.author_db import AuthorRepository
from tables.publisher_db import PublisherRepository
from tables.genre_db import GenreRepository
from tables.reader_db import ReaderRepository
from models.author import Author
from models.book import Book
from models.genre import Genre
from models.publisher import Publisher
from models.reader import Reader
from joiner import Joiner

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
        self.joiner = Joiner()
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

    def filter(self, choice, field, direction):
        try:
            if choice == '1':
                self.book_repo.filter(field, direction)
            elif choice == '2':
                self.author_repo.filter(field, direction)
            elif choice == '3':
                self.publisher_repo.filter(field, direction)
            elif choice == '4':
                self.genre_repo.filter(field, direction)
            elif choice == '5':
                self.publisher_repo.filter(field, direction)
        except Exception as e:
            logging.info(f"Error filtering: {e}")

    def search(self, choice, field, value):
        """Search records by field and entity type."""
        try:
            if choice == '1':
                return self.book_repo.find(field, value)
            elif choice == '2':
                return self.author_repo.find(field, value)
            elif choice == '3':
                return self.publisher_repo.find(field, value)
            elif choice == '4':
                return self.genre_repo.find(field, value)
            else:
                return self.reader_repo.find(field, value)
        except Exception as e:
            logging.error(f"Error searching: {e}")
            return 0

    def add_record(self, choice, record):
        """Add a new record to the specified entity."""
        try:
            if choice == '1':
                book = Book(title=record['title'], author=record['author'],
                            year=int(record['year']), pages=int(record['pages']), description=record['description'],
                            genre=record['genre'], publisher=record['publisher'])
                id = self.book_repo.save(book)
                return id
            elif choice == '2':
                author = Author(full_name=record['full_name'], date_of_birth=record['date_of_birth'],
                                date_of_death=record['date_of_death'], biography=record['biography'])
                id = self.author_repo.save(author)
                return id
            elif choice == '3':
                publisher = Publisher(name=record['name'], address=record['address'],
                                phone=record['phone'], mail=record['mail'])
                id = self.publisher_repo.save(publisher)
                return id
            elif choice == '4':
                genre = Genre(title=record['title'], description=record['description'])
                id = self.genre_repo.save(genre)
                return id
            else:
                reader = Reader(full_name=record['full_name'], phone=record['phone'],
                                mail=record['mail'])
                id = self.reader_repo.save(reader)
                return id
        except Exception as e:
            logging.error(f"Error saving: {e}")
        return -1

    def update_record(self, choice, field, new_val, author="", title=""):
        """Update an existing record."""
        try:
            if choice == '1':
                return self.book_repo.update(field, title, author, new_val)
            elif choice == '2':
                return self.author_repo.update(field, author, new_val)
            elif choice == '3':
                return self.publisher_repo.update(field, title, new_val)
            elif choice == '4':
                return self.genre_repo.update(field, title, new_val)
            elif choice == '5':
                return self.reader_repo.update(field, title, new_val)
            return
        except Exception as e:
            logging.error(f"Error updating db: {e}")
            return e

    def delete_record(self, choice, field, value):
        try:
            if choice == '1':
                return self.book_repo.delete(field, value)
            elif choice == '2':
                return self.author_repo.delete(field, value)
            elif choice == '3':
                return self.publisher_repo.delete(field, value)
            elif choice == '4':
                return self.genre_repo.delete(field, value)
            else:
                return self.author_repo.delete(field, value)
        except Exception as e:
            logging.error(f"Error deleting db: {e}")
            return e

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

    def join(self, choice):
        try:
            if choice == '1':
                self.joiner.join("author")
            elif choice == '2':
                self.joiner.join("publisher")
            elif choice == '3':
                self.joiner.join("genre")
        except Exception as e:
            logging.error(f"Error displaying: {e}")

    def export_data(self, choice, file_choice):
        if choice == '1':
            self.book_repo.export(file_choice)
        elif choice == '2':
            self.author_repo.export(file_choice)
        elif choice == '3':
            self.publisher_repo.export(file_choice)
        elif choice == '4':
            self.genre_repo.export(file_choice)
        else:
            self.reader_repo.export(file_choice)


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
        print("7. Filter Records")
        print("8. Get more information")
        print("9. Export data")
        print("0. Exit")

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
            filtering_menu(library)
        elif choice == '8':
            show_full_info(library)
        elif choice == '9':
            export_data_menu(library)
        elif choice == '0':
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
                'book': {'1': 'title', '2': 'author', '3': 'year', '4': 'genre', '5': 'pages', '6': 'publisher'},
                'author': {'1': 'full_name', '2': 'date_of_birth', '3':'date_of_death', '4': 'biography'},
                'publisher': {'1': 'name', '2': 'address', '3': 'phone', '4':'mail'},
                'genre': {'1': 'title', '2': 'description'},
                'reader': {'1': 'full_name', '2': 'phone', '3': 'mail'}
            }
            for k, v in field_options[entity].items():
                print(f"{k}. {v.capitalize()}")
            print("0. Back")
            field_choice = input("Select field: ").strip()

            if field_choice == '0':
                continue
            elif field_choice in field_options[entity]:
                field = field_options[entity][field_choice]
                query = input(f"Enter {field}: ").strip()
                logging.info(f"Searching {entity} by {field}: {query}")
                res = library.search(choice, field, query)
                if res == 0:
                    print("No results")
                logging.info(f"Found {res} results")
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
    print(f"\nAdding new {entity.capitalize()}")
    field_options = {
        'book': {'title', 'author', 'year', 'genre', 'pages', 'publisher', 'description'},
        'author': {'full_name', 'date_of_birth', 'date_of_death', 'biography'},
        'publisher': {'name', 'address', 'phone', 'mail'},
        'genre': {'title', 'description'},
        'reader': {'full_name', 'phone', 'mail'}
    }
    curr_data = {}
    for v in field_options[entity]:
        print(f"Enter the {v.capitalize()}")
        info = input()
        curr_data[v] = info
    if library.add_record(choice, curr_data) >= 0:
        print(f"{entity.capitalize()} added successfully")
        logging.info(f"{entity.capitalize()} added successfully")
    else:
        logging.info(f"Error with adding")
        print(f"Error with adding the {entity.capitalize()}")
        return


def update_record_menu(library):
    logging.info("Starting update record menu")
    entity_types = {'1': 'book', '2': 'author', '3': 'publisher', '4': 'genre', '5': 'reader'}
    print("\nUpdate Record for:")
    for k, v in entity_types.items():
        print(f"{k}. {v.capitalize()}")
    print("0. Back")
    choice = input("Select entity: ").strip()
    logging.info("Updating " + entity_types[choice])
    if choice == '0':
        return
    elif choice == '1':
        data = list(input("Enter the field that needs updating and the new value for it "
                          "(title, author, year, genre, pages, publisher): ").split())
        try:
            field, new_val = data[0], data[1]
        except Exception as e:
            logging.info(f"Error: {e}")
        author = input("Enter the author of book which you want to update: ")
        title = input("Enter the title of book which you want to update: ")
        result = library.update_record(choice=choice, title=title, author=author, new_val=new_val, field=field)
        if result is True:
            print("Successfully updated!")
            logging.info(f"Successfully updated row: {field} = {new_val}")
        elif result is False:
            print("No records found to update.")
            logging.info(f"No rows found with author = {author} and title = {title}")
        else:
            print("Error with updating")
            logging.info(f"Error with updating")
    elif choice == '2':
        data = list(input("Enter the field that needs updating and the new value for it "
                          "(full_name, date_of_birth, date_of_death, biography): ").split())
        try:
            field, new_val = data[0], data[1]
        except Exception as e:
            logging.info(f"Error: {e}")
        author = input("Enter the author that you want to update: ")
        result = library.update_record(choice=choice, author=author, new_val=new_val, field=field)
        if result is True:
            print("Successfully updated!")
            logging.info(f"Successfully updated row: {field} = {new_val}")
        elif result is False:
            print("No records found to update.")
            logging.info(f"No rows found with author = {author}")
        else:
            print("Error with updating")
            logging.info(f"Error with updating")
    elif choice == '3':
        data = list(input("Enter the field that needs updating and the new value for it "
                          "(name, address, phone, mail): ").split())
        try:
            field, new_val = data[0], data[1]
        except Exception as e:
            logging.info(f"Error: {e}")
        title = input("Enter the title of publisher that you want to update: ")
        result = library.update_record(choice=choice, title=title, new_val=new_val, field=field)
        if result is True:
            print("Successfully updated!")
            logging.info(f"Successfully updated row: {field} = {new_val}")
        elif result is False:
            print("No records found to update.")
            logging.info(f"No rows found with title = {title}")
        else:
            print("Error with updating")
            logging.info(f"Error with updating")
    elif choice == '4':
        data = list(input("Enter the field that needs updating and the new value for it "
                          "(title, description): ").split())
        try:
            field, new_val = data[0], data[1]
        except Exception as e:
            logging.info(f"Error: {e}")
        title = input("Enter the title of genre that you want to update: ")
        result = library.update_record(choice=choice, title=title, new_val=new_val, field=field)
        if result is True:
            print("Successfully updated!")
            logging.info(f"Successfully updated row: {field} = {new_val}")
        elif result is False:
            print("No records found to update.")
            logging.info(f"No rows found with title = {title}")
        else:
            print("Error with updating")
            logging.info(f"Error with updating")
    elif choice == '5':
        data = list(input("Enter the field that needs updating and the new value for it "
                          "(full_name, phone, mail): ").split())
        try:
            field, new_val = data[0], data[1]
        except Exception as e:
            logging.info(f"Error: {e}")
        title = input("Enter the title of publisher that you want to update: ")
        result = library.update_record(choice=choice, title=title, new_val=new_val, field=field)
        if result is True:
            print("Successfully updated!")
            logging.info(f"Successfully updated row: {field} = {new_val}")
        elif result is False:
            print("No records found to update.")
            logging.info(f"No rows found with title = {title}")
        else:
            print("Error with updating")
            logging.info(f"Error with updating")
    else:
        logging.warning(f"Invalid entity choice: {choice}")
        print("Invalid entity choice")
        return


def show_full_info(library):
    logging.info("Starting showing all information about books")
    entity_types = {'1': 'author', '2': 'publisher', '3': 'genre', '0': 'Back'}
    print("\nYou want to know more information about: ")
    for k, v in entity_types.items():
        print(f"{k}. {v.capitalize()}")
    choice = input("Select entity: ").strip()
    logging.info("Joining " + entity_types[choice])
    if choice == '0':
        return
    elif choice in entity_types:
        try:
            library.join(choice)
        except Exception as e:
            logging.info(f"Error: {e}")
    else:
        logging.warning(f"Invalid entity choice: {choice}")
        print("Invalid entity choice")
        return


def delete_record_menu(library):
    logging.info("Starting delete record menu")
    entity_types = {
        '1': ('book', ["title", "author", "year", "genre", "pages", "publisher"]),
        '2': ('author', ["full_name", "date_of_birth", "date_of_death", "biography"]),
        '3': ('publisher', ["name", "address", "phone", "mail"]),
        '4': ('genre', ["title", "description"]),
        '5': ('reader', ["full_name", "phone", "mail"])
    }

    print("\nDelete Record for:")
    for k, v in entity_types.items():
        print(f"{k}. {v[0].capitalize()}")
    print("0. Back")

    choice = input("Select entity: ").strip()
    if choice == '0':
        return

    if choice not in entity_types:
        logging.warning(f"Invalid entity choice: {choice}")
        print("Invalid entity choice")
        return

    entity_name, fields = entity_types[choice]
    print(f"\nDeleting {entity_name} by field")
    print("Available fields:", ", ".join(fields))

    field = input("Enter the field: ").strip()
    if field not in fields:
        print("Invalid field!")
        return

    value = input("Enter the value of this field: ").strip()

    result = library.delete_record(choice, field, value)
    if result is True:
        print("Successfully deleted!")
        logging.info(f"Successfully deleted {entity_name} where {field}={value}")
    elif result is False:
        print("No records found to delete.")
        logging.info(f"No {entity_name} found with {field}={value}")
    else:
        print("Error with deleting")
        logging.info(f"Error with deleting")


def filtering_menu(library):
    logging.info("Start filtering menu")
    entity_types = {'1': 'book', '2': 'author', '3': 'publisher', '4': 'genre', '5': 'reader'}
    while True:
        print("\nFilter by Entity:")
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
            print(f"\nFilter {entity.capitalize()} by:")
            field_options = {
                'book': {'1': 'title', '2': 'author', '3': 'year', '4': 'genre', '5': 'pages', '6': 'publisher'},
                'author': {'1': 'full_name', '2': 'date_of_birth', '3':'date_of_death', '4': 'biography'},
                'publisher': {'1': 'name', '2': 'address', '3': 'phone', '4':'mail'},
                'genre': {'1': 'title', '2': 'description'},
                'reader': {'1': 'full_name', '2': 'phone', '3': 'mail'}
            }
            for k, v in field_options[entity].items():
                print(f"{k}. {v.capitalize()}")
            print("0. Back")
            field_choice = input("Select field: ").strip()

            if field_choice == '0':
                continue
            elif field_choice in field_options[entity]:
                print(f"Choose direction: ")
                print("1. Ascending")
                print("2. Descending")
                dir = input("Select direction: ").strip()
                logging.debug(f"User selected direction: {dir}")
                if dir == "1":
                    library.filter(choice, field_options[entity][field_choice], "up")
                elif dir == "2":
                    library.filter(choice, field_options[entity][field_choice], "down")
                else:
                    logging.warning(f"Invalid direction choice: {dir}")
                    print("Invalid direction choice")
            else:
                logging.warning(f"Invalid field choice: {field_choice}")
                print("Invalid field choice")
        else:
            logging.warning(f"Invalid entity choice: {choice}")
            print("Invalid entity choice")


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


def export_data_menu(library):
    logging.info("Starting exporting data menu")
    entity_types = {'1': 'book', '2': 'author', '3': 'publisher', '4': 'genre', '5': 'reader'}
    print("\nExport data for:")
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
    logging.info(f"Exported data for {entity}")

    logging.info("Choosing extension of file for export")
    entity_file_types = {'1': 'json', '2': 'csv'}
    print("\nFile format:")
    for k, v in entity_file_types.items():
        print(f"{k}. {v.capitalize()}")
    print("0. Back")
    file_choice = input("Select entity: ").strip()
    if file_choice == '0':
        return
    if file_choice not in entity_file_types:
        logging.warning(f"Invalid entity choice: {file_choice}")
        print("Invalid entity choice")
        return

    entity_file = entity_file_types[file_choice]
    library.export_data(choice, entity_file)
    logging.info(f"Exported data in {entity_file}")


def main():
    try:
        library = Library()
        main_menu(library)
        logging.info("Program started")
        print("Welcome to the Library Management System")
    except KeyboardInterrupt:
        print("\nThe program has been terminated at the user's request")
        exit(0)


if __name__ == "__main__":
    main()
