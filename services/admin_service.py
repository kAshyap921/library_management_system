from exceptions.exceptions import PermissionDeniedError

# This service is strictly for administrative operations
class AdminService:

    def __init__(self, library_service, rental_service):
        self.__library = library_service
        self.__rentals = rental_service

    def __check_admin(self, user):
        if not user.is_admin():
            raise PermissionDeniedError("Access Denied: Only administrators can view this information.")

    def show_all_books_report(self, admin_user):
        self.__check_admin(admin_user)
        books = self.__library.get_all_books()
        available = [b for b in books if b.available]
        rented    = [b for b in books if not b.available]

        print(f"\n  Inventory Report:")
        print(f"  Total Books      : {len(books)}")
        print(f"  Available        : {len(available)}")
        print(f"  Currently Rented : {len(rented)}")

    def show_overdue_report(self, admin_user):
        self.__check_admin(admin_user)
        overdue = self.__rentals.get_overdue_rentals()

        if not overdue:
            print("\n  No books are currently overdue.")
            return

        print(f"\n  --- {len(overdue)} Overdue Item(s) Found ---")
        for r in overdue:
            # Calculation of fine based on overdue days
            fine = r.days_overdue() * 2
            print(r.get_display_info())
            print(f"  Fine Due         : Rs. {fine}")
            print("  " + "-" * 35)

    def show_active_rentals(self, admin_user):
        self.__check_admin(admin_user)
        active = self.__rentals.get_active_rentals()

        if not active:
            print("\n  There are no active rentals at the moment.")
            return

        print(f"\n  --- {len(active)} Active Rental(s) ---")
        for r in active:
            print(r.get_display_info())
            print("  " + "-" * 35)