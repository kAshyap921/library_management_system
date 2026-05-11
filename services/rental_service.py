from data_access.csv_handler import CSVHandler
from data_access.db_handler  import DBHandler
from data_access.db_config   import RENTALS_CSV, RENTAL_FIELDS
from models.rental           import Rental
from exceptions.exceptions   import (BookNotAvailableError,
                                     AlreadyIssuedError,
                                     BookNotFoundError)

# Handles book issuance and returns

class RentalService:

    def __init__(self, library_service):
        self.__library = library_service
        self.__rentals = []
        self.__load_rentals()

    def __load_rentals(self):
        # Load rental history from both CSV and Database sources
        rows = CSVHandler.load(RENTALS_CSV)
        rows = DBHandler.load("rentals")
        for row in rows:
            self.__rentals.append(Rental.from_dict(row))

    def __save_rentals(self):
        # Persist current rental states to storage
        data = [r.to_dict() for r in self.__rentals]
        DBHandler.save("rentals", data)
        CSVHandler.save(RENTALS_CSV, data, RENTAL_FIELDS)

    def issue_book(self, user, book_id):
        # Step 1: Check if the user already has an active issue
        for rental in self.__rentals:
            if rental.user_id == user.user_id and rental.return_date is None:
                raise AlreadyIssuedError(
                    f"A book with ID '{rental.book_id}' is already issued to you. "
                    f"Please return it before issuing another."
                )

        # Step 2: Verify if the book exists
        book = self.__library.get_book(book_id)

        # Step 3: Check if the book is currently available
        if not book.available:
            raise BookNotAvailableError(
                f"'{book.title}' is currently unavailable — it has been issued to someone else."
            )

        # Everything is valid — proceed with issuance
        rental = Rental(user_id=user.user_id, book_id=book_id)
        self.__rentals.append(rental)

        # Mark book as unavailable in the library system
        self.__library.update_availability(book_id, False)

        self.__save_rentals()
        return rental

    def return_book(self, user, book_id):
        # Verify if this specific book is issued to the user
        active = None
        for rental in self.__rentals:
            if (rental.user_id == user.user_id and
                rental.book_id == book_id.strip().upper() and
                rental.return_date is None):
                active = rental
                break

        if not active:
            raise BookNotFoundError(
                f"No active record found for book ID '{book_id}' under your account."
            )

        # Mark as returned
        active.mark_returned()

        # Update book status to available
        self.__library.update_availability(book_id, True)

        self.__save_rentals()

        # Notify if the return is overdue
        if active.days_overdue() > 0:
            fine = active.days_overdue() * 2
            print(f"\n  *** OVERDUE ALERT ***")
            print(f"  {active.days_overdue()} days late — Fine applied: Rs. {fine}")

        return active

    def get_user_rentals(self, user_id):
        # Retrieve complete rental history for a specific user
        return [r for r in self.__rentals if r.user_id == user_id]

    def get_active_rentals(self):
        # Retrieve all books currently out on rent
        return [r for r in self.__rentals if r.return_date is None]

    def get_overdue_rentals(self):
        # Retrieve books that have passed the due date and are not yet returned
        return [r for r in self.__rentals if r.is_overdue()]