import uuid
from data_access.db_config import TYPE_TEXT

# Book base class — demonstrating Encapsulation
# PhysicalBook, AudioBook, and VideoBook inherit from this — demonstrating Inheritance + Polymorphism

class Book:

    def __init__(self, title, writer, category, book_type=TYPE_TEXT,
                 available=True, book_id=None):
        self.__book_id   = book_id if book_id else str(uuid.uuid4())[:8].upper()
        self.__title     = title.strip()
        self.__writer    = writer.strip()
        self.__category  = category.strip()
        self.__book_type = book_type
        self.__available = True if available in [True, "True", "true"] else False

    # --- Getters ---
    @property
    def book_id(self):
        return self.__book_id

    @property
    def title(self):
        return self.__title

    @property
    def writer(self):
        return self.__writer

    @property
    def category(self):
        return self.__category

    @property
    def book_type(self):
        return self.__book_type

    @property
    def available(self):
        return self.__available

    # --- Setters ---
    @title.setter
    def title(self, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        self.__title = value.strip()

    @writer.setter
    def writer(self, value):
        if not value.strip():
            raise ValueError("Author name is required")
        self.__writer = value.strip()

    @category.setter
    def category(self, value):
        if not value.strip():
            raise ValueError("Category cannot be empty")
        self.__category = value.strip()

    # Intended for use by internal services only
    def _set_availability(self, status):
        self.__available = status

    def get_display_info(self):
        status = "Available" if self.__available else "Rented Out"
        return (
            f"\n  Book ID  : {self.__book_id}"
            f"\n  Title    : {self.__title}"
            f"\n  Writer   : {self.__writer}"
            f"\n  Category : {self.__category}"
            f"\n  Type     : {self.__book_type.upper()}"
            f"\n  Status   : {status}"
        )

    def to_dict(self):
        return {
            "book_id"  : self.__book_id,
            "title"    : self.__title,
            "writer"   : self.__writer,
            "category" : self.__category,
            "book_type": self.__book_type,
            "available": str(self.__available)
        }

    @classmethod
    def from_dict(cls, data):
        # Factory method to instantiate the correct subclass
        from models.book_factory import BookFactory
        return BookFactory.from_dict(data)

    def __str__(self):
        status = "Available" if self.__available else "Rented Out"
        return (f"[{self.__book_id}] {self.__title} | "
                f"By: {self.__writer} | Cat: {self.__category} | "
                f"Type: {self.__book_type.upper()} | {status}")


# Subclasses — Demonstrating INHERITANCE + POLYMORPHISM

class TextBook(Book):

    def get_display_info(self):
        return "[TEXT BOOK]" + super().get_display_info()

    def __str__(self):
        return "[TEXT] " + super().__str__()


class AudioBook(Book):
    
    def get_display_info(self):
        return "[AUDIO BOOK]" + super().get_display_info()

    def __str__(self):
        return "[AUDIO] " + super().__str__()

class VideoBook(Book):
   
    def get_display_info(self):
        return "[VIDEO BOOK]" + super().get_display_info()

    def __str__(self):
        return "[VIDEO] " + super().__str__()