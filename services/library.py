from data_access.csv_handler import CSVHandler
from data_access.db_config   import BOOKS_CSV, BOOK_FIELDS
from data_access.db_handler  import DBHandler
from models.book             import Book
from models.book_factory     import BookFactory
from exceptions.exceptions   import (BookNotFoundError, BookAlreadyExistsError,
                                     PermissionDeniedError)

# Core CRUD operations for Books - Restricted to Administrators

class LibraryService:

    def __init__(self):
        self.__books = {}
        self.__load_books()

    def __load_books(self):
        # Load books from CSV storage into memory at startup
        # rows = DBHandler.load("books")
        rows = CSVHandler.load(BOOKS_CSV)
        for row in rows:
            book = BookFactory.from_dict(row)
            self.__books[book.book_id] = book

    def __save_books(self):
        # Synchronize in-memory changes back to persistent storage
        data = [b.to_dict() for b in self.__books.values()]
        # DBHandler.save("books", data)
        CSVHandler.save(BOOKS_CSV, data, BOOK_FIELDS)

    def add_book(self, admin_user, title, writer, category, book_type):
        if not admin_user.is_admin():
            raise PermissionDeniedError("Only administrators are authorized to add books.")

        # Check for duplicate entries (Title + Author)
        for book in self.__books.values():
            if (book.title.lower()  == title.lower() and
                book.writer.lower() == writer.lower()):
                raise BookAlreadyExistsError(
                    f"'{title}' by {writer} already exists in the library inventory."
                )

        new_book = BookFactory.create(title, writer, category, book_type)
        self.__books[new_book.book_id] = new_book
        self.__save_books()
        return new_book

    def update_book(self, admin_user, book_id, title=None, writer=None, category=None):
        if not admin_user.is_admin():
            raise PermissionDeniedError("Only administrators are authorized to update book details.")

        book = self.get_book(book_id)
        if title:
            book.title = title
        if writer:
            book.writer = writer
        if category:
            book.category = category
            
        self.__save_books()
        return book

    def delete_book(self, admin_user, book_id):
        if not admin_user.is_admin():
            raise PermissionDeniedError("Only administrators are authorized to delete books.")

        book = self.get_book(book_id)
        if not book.available:
            raise Exception("Cannot delete a book that is currently rented. Please return it first.")

        del self.__books[book_id]
        self.__save_books()

    def get_book(self, book_id):
        book = self.__books.get(book_id.strip().upper())
        if not book:
            raise BookNotFoundError(f"Book with ID '{book_id}' was not found.")
        return book

    def get_all_books(self):
        return list(self.__books.values())

    def update_availability(self, book_id, status):
        # This method is intended for use by the Rental Service specifically
        book = self.get_book(book_id)
        book._set_availability(status)
        self.__save_books()