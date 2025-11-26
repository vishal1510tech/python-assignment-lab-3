

import json
import logging
from typing import List, Optional
from .book import Book

logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, storage_file: str = "books.json"):
        self.books: List[Book] = []
        self.storage_file = storage_file
        self.load_from_file()

    

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        logger.info(f"Book added: {book}")
        self.save_to_file()

    def search_by_title(self, title_query: str) -> List[Book]:
        title_query = title_query.lower()
        return [b for b in self.books if title_query in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> List[Book]:
        return self.books

    

    def load_from_file(self) -> None:
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book(**item) for item in data]
            logger.info("Books loaded from file successfully.")
        except FileNotFoundError:
            logger.error(f"Storage file '{self.storage_file}' not found. Starting with empty inventory.")
            self.books = []
        except json.JSONDecodeError:
            logger.error(f"Storage file '{self.storage_file}' is corrupted. Starting with empty inventory.")
            self.books = []
        except Exception as e:
            logger.error(f"Unexpected error while loading file: {e}")
            self.books = []

    def save_to_file(self) -> None:
        try:
            data = [book.to_dict() for book in self.books]
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logger.info("Books saved to file successfully.")
        except Exception as e:
            logger.error(f"Error while saving to file: {e}")