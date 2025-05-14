# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path
from tabulate import tabulate


class Joiner:
    def __init__(self, db_path: str = "C:/Users/student/PycharmProjects/booksdb/data/library.db"):
        self.db_path = Path(db_path)

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def join(self, table_title) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if table_title == "author":
                query = """SELECT book.title, book.year, book.genre, book.pages, book.publisher, 
                author.full_name, author.date_of_birth, author.date_of_death  
                FROM book JOIN author 
                ON book.author = author.full_name"""
                headers = ["Название", "Год", "Жанр", "Страниц", "Издательство", "Автор", "Дата рождения", "Дата смерти"]
            elif table_title == "publisher":
                query = """SELECT book.title, book.author, book.year, book.genre, book.pages, 
                publisher.name, publisher.address, publisher.phone, publisher.mail  
                FROM book JOIN publisher 
                ON book.publisher = publisher.name"""
                headers = ["Название", "Автор", "Год", "Жанр", "Страниц", "Издательство", "Адрес", "Телефон", "Почта"]
            else:
                query = """SELECT book.title, book.author, book.year, book.pages, book.publisher, 
                genre.title, genre.description
                FROM book JOIN genre 
                ON book.genre = genre.title"""
                headers = ["Название", "Автор", "Год", "Страниц", "Издательство", "Жанр", "Описание жанра"]
            cursor.execute(query)
            res = cursor.fetchall()
            table_data = []
            for row in res:
                row_data = []
                for elem in row:
                    row_data.append(elem)
                table_data.append(row_data)

            print("\n" + "=" * 100)
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
            print("=" * 100 + "\n")
            return len(table_data)
