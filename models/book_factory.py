from data_access.db_config import TYPE_TEXT, TYPE_AUDIO, TYPE_VIDEO

# Factory Pattern implementation for Book creation

class BookFactory:

    @staticmethod
    def create(title, writer, category, book_type=TYPE_TEXT):
        from models.book import TextBook, AudioBook, VideoBook

        book_type = book_type.lower().strip()

        if book_type == TYPE_AUDIO:
            return AudioBook(title, writer, category, book_type)
        elif book_type == TYPE_VIDEO:
            return VideoBook(title, writer, category, book_type)
        else:
            return TextBook(title, writer, category, TYPE_TEXT)

    @staticmethod
    def from_dict(data):
        from models.book import TextBook, AudioBook, VideoBook

        book_type = data.get("book_type", TYPE_TEXT).lower()
        available = data.get("available", "True")

        args = {
            "title"    : data["title"],
            "writer"   : data["writer"],
            "category" : data["category"],
            "book_type": book_type,
            "available": available,
            "book_id"  : data["book_id"]
        }

        if book_type == TYPE_AUDIO:
            return AudioBook(**args)
        elif book_type == TYPE_VIDEO:
            return VideoBook(**args)
        else:
            return TextBook(**args)

    @staticmethod
    def get_type_menu():
        print("  Select Book Type:")
        print("  1. Text  (Standard Edition)")
        print("  2. Audio (Audiobook Format)")
        print("  3. Video (Video Lesson/Media)")

    @staticmethod
    def type_from_choice(choice):
        mapping = {"1": TYPE_TEXT, "2": TYPE_AUDIO, "3": TYPE_VIDEO}
        return mapping.get(choice, TYPE_TEXT)