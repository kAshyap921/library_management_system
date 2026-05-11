import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# SQLite database
DB_PATH = os.path.join(DATA_DIR, "library.db")

# CSV paths (backup)
USERS_CSV   = os.path.join(DATA_DIR, "users.csv")
BOOKS_CSV   = os.path.join(DATA_DIR, "books.csv")
RENTALS_CSV = os.path.join(DATA_DIR, "rentals.csv")

# CSV Field names
USER_FIELDS   = ["user_id", "name", "password", "role", "status"]
BOOK_FIELDS   = ["book_id", "title", "writer", "category", "book_type", "available"]
RENTAL_FIELDS = ["rental_id", "user_id", "book_id", "issue_date", "due_date", "return_date"]

# Constants
STATUS_PENDING  = "pending"
STATUS_VERIFIED = "verified"
STATUS_REJECTED = "rejected"
ROLE_ADMIN      = "admin"
ROLE_MEMBER     = "member"
TYPE_TEXT       = "text"
TYPE_AUDIO      = "audio"
TYPE_VIDEO      = "video"
LOAN_DAYS       = 14