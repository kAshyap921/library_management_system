from data_access.csv_handler import CSVHandler
from data_access.db_handler  import DBHandler
from data_access.db_config   import USERS_CSV, USER_FIELDS, STATUS_PENDING, ROLE_MEMBER
from models.user             import User
from exceptions.exceptions   import UserAlreadyExistsError

#naya user register karna


def register(name, password):
    if not name.strip() or not password.strip():
        raise ValueError("Both name and password are required.")

    # Load existing users to check for duplicates
    existing_users = DBHandler.load("users")
    existing_users = CSVHandler.load(USERS_CSV)
    
    for row in existing_users:
        if row["name"].lower() == name.strip().lower():
            raise UserAlreadyExistsError(
                f"An account with the name '{name}' already exists."
            )

    # Initialize new user with default member role and pending status
    new_user = User(
        name     = name,
        password = password,
        role     = ROLE_MEMBER,
        status   = STATUS_PENDING
    )

    # Save user data to both database and CSV storage
    DBHandler.insert("users", new_user.to_dict())
    CSVHandler.append_row(USERS_CSV, new_user.to_dict(), USER_FIELDS)

    return new_user