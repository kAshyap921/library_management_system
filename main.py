from auth.login              import login
from auth.register           import register
from auth.admin_auth         import (get_pending_users, approve_user,
                                     reject_user, get_all_users)
from services.library        import LibraryService
from services.search         import SearchService
from services.rental_service import RentalService
from services.admin_service  import AdminService
from models.book_factory     import BookFactory
from exceptions.exceptions   import *
from data_access.db_config   import (USERS_CSV, USER_FIELDS,
                                     ROLE_ADMIN, STATUS_VERIFIED)
from data_access.csv_handler import CSVHandler
from data_access.db_handler  import DBHandler


def sep():
    print("-" * 54)

def header(text):
    print("\n" + "=" * 45)
    print(f"  {text}")
    print("=" * 45)

def setup_admin_if_needed():
    rows = DBHandler.load("users")
    rows = CSVHandler.load(USERS_CSV)
    admins = [r for r in rows if r.get("role") == ROLE_ADMIN]
    if not admins:
        default_admin = {
            "user_id" : "ADMIN001",
            "name"    : "Admin",
            "password": "admin123",
            "role"    : ROLE_ADMIN,
            "status"  : STATUS_VERIFIED
        }
        DBHandler.insert("users", default_admin)
        CSVHandler.append_row(USERS_CSV, default_admin, USER_FIELDS)
        print("  Default admin created — ID: ADMIN001, Pass: admin123")

# Search menu logic

def search_menu(search_service):
    while True:
        header("Search Books")
        print("  1. Search by Author")
        print("  2. Search by Category")
        print("  3. Search by Title")
        print("  4. Search by Type (text/audio/video)")
        print("  5. View all categories")
        print("  0. Go Back")
        sep()
        choice = input("  Select Option: ").strip()

        if choice == "1":
            writer = input("  Enter Author Name: ")
            avail, rented = search_service.search_by_writer(writer)
            __show_search_results(avail, rented)

        elif choice == "2":
            cat = input("  Enter Category: ")
            avail, rented = search_service.search_by_category(cat)
            __show_search_results(avail, rented)

        elif choice == "3":
            title = input("  Enter Title: ")
            avail, rented = search_service.search_by_title(title)
            __show_search_results(avail, rented)

        elif choice == "4":
            print("  Type: 1.Text  2.Audio  3.Video")
            t = input("  Choose Type: ").strip()
            type_map = {"1": "text", "2": "audio", "3": "video"}
            book_type = type_map.get(t, "text")
            avail, rented = search_service.search_by_type(book_type)
            __show_search_results(avail, rented)

        elif choice == "5":
            cats = search_service.get_all_categories()
            print("\n  Available Categories:")
            for c in cats:
                print(f"    - {c}")

        elif choice == "0":
            break

def __show_search_results(available, rented):
    sep()
    if not available and not rented:
        print("  No books found.")
        return
    if available:
        print(f"  [{len(available)} Available]")
        for b in available:
            print(b.get_display_info())
            sep()
    if rented:
        print(f"\n  [{len(rented)} Not Available — Currently on Rent]")
        for b in rented:
            print(b.get_display_info())
            sep()

# Member menu logic

def member_menu(user, library_svc, search_svc, rental_svc):
    while True:
        header(f"Welcome {user.name} | Member Menu")

        # After login — show books grouped by category
        grouped = search_svc.show_by_category_grouped()
        print("\n  Available categories in Library:")
        for cat in grouped:
            avail = sum(1 for b in grouped[cat] if b.available)
            total = len(grouped[cat])
            print(f"    [{cat}]  {avail}/{total} available")

        print("\n  1. Search Books")
        print("  2. Issue a Book")
        print("  3. Return a Book")
        print("  4. View My Rentals")
        print("  0. Logout")
        sep()
        choice = input("  Select Option: ").strip()

        if choice == "1":
            search_menu(search_svc)

        elif choice == "2":
            book_id = input("  Enter Book ID: ").strip().upper()
            try:
                rental = rental_svc.issue_book(user, book_id)
                print("\n  Book issued successfully!")
                print(rental.get_display_info())
            except (AlreadyIssuedError, BookNotAvailableError,
                    BookNotFoundError) as e:
                print(f"\n  Error: {e}")

        elif choice == "3":
            book_id = input("  Enter Book ID: ").strip().upper()
            try:
                rental = rental_svc.return_book(user, book_id)
                print("\n  Book returned successfully!")
                print(rental.get_display_info())
            except (BookNotFoundError, LibraryError) as e:
                print(f"\n  Error: {e}")

        elif choice == "4":
            rentals = rental_svc.get_user_rentals(user.user_id)
            if not rentals:
                print("\n  You haven't issued any books yet.")
            else:
                for r in rentals:
                    print(r.get_display_info())
                    sep()

        elif choice == "0":
            print(f"\n  Goodbye {user.name}!")
            break

# Admin menu logic

def admin_menu(user, library_svc, search_svc, rental_svc):
    admin_svc = AdminService(library_svc, rental_svc)

    while True:
        header(f"Admin Panel — {user.name}")
        print("  --- User Management ---")
        print("  1. View pending users (Approve/Reject)")
        print("  2. View all users")
        print("\n  --- Book Management ---")
        print("  3. Add new book")
        print("  4. Update book details")
        print("  5. Delete a book")
        print("  6. Search books")
        print("\n  --- Reports ---")
        print("  7. View inventory report")
        print("  8. View active rentals")
        print("  9. View overdue books")
        print("\n  0. Logout")
        sep()
        choice = input("  Select Option: ").strip()

        # User management
        if choice == "1":
            pending = get_pending_users()
            if not pending:
                print("\n  No pending users found.")
            else:
                print(f"\n  {len(pending)} pending user(s):")
                for p in pending:
                    print(f"    ID: {p['user_id']} | Name: {p['name']}")
                sep()
                uid    = input("  Enter User ID (to Approve/Reject): ").strip()
                action = input("  1. Approve  2. Reject: ").strip()
                try:
                    if action == "1":
                        approve_user(user, uid)
                        print("\n  User approved successfully.")
                    elif action == "2":
                        reject_user(user, uid)
                        print("\n  User request rejected.")
                except (UserNotFoundError, PermissionDeniedError) as e:
                    print(f"\n  Error: {e}")

        elif choice == "2":
            try:
                users = get_all_users(user)
                print(f"\n  Total {len(users)} users:")
                for u in users:
                    print(f"    {u['user_id']} | {u['name']} | {u['role']} | {u['status']}")
            except PermissionDeniedError as e:
                print(f"\n  Error: {e}")

        # Book management
        elif choice == "3":
            title    = input("  Title: ")
            writer   = input("  Author: ")
            category = input("  Category: ")
            BookFactory.get_type_menu()
            t_choice  = input("  Select Type (1/2/3): ").strip()
            book_type = BookFactory.type_from_choice(t_choice)
            try:
                book = library_svc.add_book(user, title, writer, category, book_type)
                print(f"\n  Book added successfully! ID: {book.book_id}")
            except (BookAlreadyExistsError, PermissionDeniedError) as e:
                print(f"\n  Error: {e}")

        elif choice == "4":
            book_id  = input("  Book ID: ").strip()
            title    = input("  New title (Press Enter to skip): ")
            writer   = input("  New author (Press Enter to skip): ")
            category = input("  New category (Press Enter to skip): ")
            try:
                book = library_svc.update_book(
                    user, book_id,
                    title    = title    or None,
                    writer   = writer   or None,
                    category = category or None
                )
                print("\n  Update successful:")
                print(book.get_display_info())
            except (BookNotFoundError, PermissionDeniedError) as e:
                print(f"\n  Error: {e}")

        elif choice == "5":
            book_id = input("  Enter Book ID: ").strip()
            try:
                library_svc.delete_book(user, book_id)
                print("\n  Book deleted successfully.")
            except (BookNotFoundError, PermissionDeniedError, Exception) as e:
                print(f"\n  Error: {e}")

        elif choice == "6":
            search_menu(search_svc)

        # Reports
        elif choice == "7":
            admin_svc.show_all_books_report(user)

        elif choice == "8":
            admin_svc.show_active_rentals(user)

        elif choice == "9":
            admin_svc.show_overdue_report(user)

        elif choice == "0":
            print(f"\n  Admin logged out.")
            break

# Main entry point 

def main():
    # Initialize services — shared across the application
    DBHandler.setup_tables()
    library_svc = LibraryService()
    search_svc  = SearchService(library_svc)
    rental_svc  = RentalService(library_svc)

    # If first run, set up the default administrator
    setup_admin_if_needed()
    
    while True:
        header("LIBRARY MANAGEMENT SYSTEM")
        print("  1. Login")
        print("  2. Create New Account")
        print("  0. Exit")
        sep()
        choice = input("  Select Option: ").strip()

        if choice == "1":
            user_id  = input("  User ID: ").strip()
            password = input("  Password: ").strip()
            try:
                user = login(user_id, password)
                print(f"\n  Login successful! Welcome {user.name}")
                
                if user.is_admin():
                    admin_menu(user, library_svc, search_svc, rental_svc)
                else:
                    member_menu(user, library_svc, search_svc, rental_svc)

            except (UserNotFoundError, InvalidCredentialsError,
                    UserNotVerifiedError) as e:
                print(f"\n  Login failed: {e}")

        elif choice == "2":
            name     = input("  Enter your name: ")
            password = input("  Choose a password: ")
            try:
                new_user = register(name, password)
                print(f"\n  Account created! Your ID is: {new_user.user_id}")
                print("  Please wait for admin approval before you can log in.")
            except (UserAlreadyExistsError, ValueError) as e:
                print(f"\n  Error: {e}")

        elif choice == "0":
            print("\n  Shutting down Library Management System. See you soon!")
            break

        else:
            print("\n  Invalid option — Please enter 0, 1, or 2.")


if __name__ == "__main__":
    main()