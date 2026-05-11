from data_access.csv_handler import CSVHandler
from data_access.db_handler import DBHandler
from data_access.db_config   import USERS_CSV, STATUS_VERIFIED
from models.user             import User
from exceptions.exceptions   import (UserNotFoundError,
                                     InvalidCredentialsError,
                                     UserNotVerifiedError)

# All login operations are handled here
# main.py will call this function to authenticate users

def login(user_id, password):
    # Step 1: Locate user in the data source
    row = CSVHandler.find_one(USERS_CSV, "user_id", user_id.strip().upper())
    row = DBHandler.find_one("users", "user_id", user_id.strip().upper())
    
    if not row:
        raise UserNotFoundError(f"ID '{user_id}' does not match any existing user.")

    if row["password"] != password.strip():
        raise InvalidCredentialsError("Incorrect password.")

    if row["status"] != STATUS_VERIFIED:
        raise UserNotVerifiedError(
            "Your account is not yet verified. "
            "Please wait for administrator approval."
        )

    # Everything is correct — return the User object
    return User.from_dict(row)