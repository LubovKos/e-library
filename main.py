import csv
import json
import logging
import os
import sqlite3

from data_import.csv.book_importer import CSVBookReader
from databases.book_db import BookRepository


repo = BookRepository()
importer = CSVBookReader("data/csv/test_books.csv", repo)

# Импорт
importer.load_from_csv()
repo.show_all()

