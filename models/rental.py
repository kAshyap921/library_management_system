import uuid
from datetime import datetime, timedelta
from data_access.db_config import LOAN_DAYS

# Rental class — ek issue ka poora record
# Encapsulation — saari cheezein private

class Rental:

    def __init__(self, user_id, book_id, issue_date=None,
                 due_date=None, return_date=None, rental_id=None):
        self.__rental_id   = rental_id if rental_id else str(uuid.uuid4())[:8].upper()
        self.__user_id     = user_id
        self.__book_id     = book_id
        self.__issue_date  = issue_date  if issue_date  else datetime.now().strftime("%Y-%m-%d")
        self.__due_date    = due_date    if due_date     else self.__calc_due_date()
        self.__return_date = return_date  # None = abhi return nahi hua

    def __calc_due_date(self):
    
        issue = datetime.strptime(self.__issue_date, "%Y-%m-%d")
        return (issue + timedelta(days=LOAN_DAYS)).strftime("%Y-%m-%d")

    #Getters
    @property
    def rental_id(self):
        return self.__rental_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def book_id(self):
        return self.__book_id

    @property
    def issue_date(self):
        return self.__issue_date

    @property
    def due_date(self):
        return self.__due_date

    @property
    def return_date(self):
        return self.__return_date

    def mark_returned(self):
        self.__return_date = datetime.now().strftime("%Y-%m-%d")

    def is_overdue(self):
        if self.__return_date:
            return False
        today = datetime.now().strftime("%Y-%m-%d")
        return today > self.__due_date

    def days_overdue(self):
        if not self.is_overdue():
            return 0
        today  = datetime.now()
        due    = datetime.strptime(self.__due_date, "%Y-%m-%d")
        return (today - due).days

    def get_display_info(self):
        ret    = self.__return_date if self.__return_date else "Abhi nahi"
        status = "OVERDUE!" if self.is_overdue() else "On time"
        return (
            f"\n  Rental ID   : {self.__rental_id}"
            f"\n  User ID     : {self.__user_id}"
            f"\n  Book ID     : {self.__book_id}"
            f"\n  Issue Date  : {self.__issue_date}"
            f"\n  Due Date    : {self.__due_date}  [{status}]"
            f"\n  Return Date : {ret}"
        )

    def to_dict(self):
        return {
            "rental_id"  : self.__rental_id,
            "user_id"    : self.__user_id,
            "book_id"    : self.__book_id,
            "issue_date" : self.__issue_date,
            "due_date"   : self.__due_date,
            "return_date": self.__return_date if self.__return_date else ""
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id     = data["user_id"],
            book_id     = data["book_id"],
            issue_date  = data["issue_date"],
            due_date    = data["due_date"],
            return_date = data["return_date"] if data["return_date"] else None,
            rental_id   = data["rental_id"]
        )