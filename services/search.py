from exceptions.exceptions import BookNotFoundError

# check fist avalable book then check rented book & (unavailable)

class SearchService:

    def __init__(self, library_service):
        #"need a reference to LibraryService to borrow books"
        self.__library = library_service

    def search_by_writer(self, writer_name):
        all_books = self.__library.get_all_books()
        results   = [
            b for b in all_books
            if writer_name.lower() in b.writer.lower()
        ]
        return self.__split_available(results)

    def search_by_category(self, category):
        all_books = self.__library.get_all_books()
        results   = [
            b for b in all_books
            if category.lower() in b.category.lower()
        ]
        return self.__split_available(results)

    def search_by_type(self, book_type):
        all_books = self.__library.get_all_books()
        results   = [
            b for b in all_books
            if b.book_type.lower() == book_type.lower()
        ]
        return self.__split_available(results)

    def search_by_title(self, title):
        all_books = self.__library.get_all_books()
        results   = [
            b for b in all_books
            if title.lower() in b.title.lower()
        ]
        return self.__split_available(results)

    def __split_available(self, books):
        available = [b for b in books if b.available]
        rented    = [b for b in books if not b.available]
        return available, rented

    def get_all_categories(self):
        all_books = self.__library.get_all_books()
        categories = sorted(set(b.category for b in all_books))
        return categories

    def show_by_category_grouped(self):
        all_books = self.__library.get_all_books()
        grouped   = {}
        for book in all_books:
            cat = book.category
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(book)
        return grouped