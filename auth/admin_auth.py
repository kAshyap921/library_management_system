from data_access.csv_handler import CSVHandler
from data_access.db_handler  import DBHandler
from data_access.db_config   import (USERS_CSV, USER_FIELDS,
                                     STATUS_PENDING, STATUS_VERIFIED, STATUS_REJECTED)
from exceptions.exceptions   import UserNotFoundError, PermissionDeniedError

# All administrative user management functions are handled here

def get_pending_users():
    rows = CSVHandler.load(USERS_CSV)
    rows = DBHandler.load("users")
    return [r for r in rows if r["status"] == STATUS_PENDING]

def approve_user(admin_user, user_id):
    if not admin_user.is_admin():
        raise PermissionDeniedError("Only administrators can perform this action.")

    row = CSVHandler.find_one(USERS_CSV, "user_id", user_id.strip().upper())
    if not row:
        raise UserNotFoundError(f"User ID '{user_id}' not found.")

    DBHandler.update("users", "user_id", user_id.strip().upper(),
                 {"status": STATUS_VERIFIED})
    CSVHandler.update_row(
        USERS_CSV,
        key          = "user_id",
        value        = user_id.strip().upper(),
        updated_data = {"status": STATUS_VERIFIED},
        fieldnames   = USER_FIELDS
    )
    print(f"  User '{row['name']}' has been approved.")

def reject_user(admin_user, user_id):
    if not admin_user.is_admin():
        raise PermissionDeniedError("Only administrators can perform this action.")

    row = CSVHandler.find_one(USERS_CSV, "user_id", user_id.strip().upper())
    if not row:
        raise UserNotFoundError(f"User ID '{user_id}' not found.")
    
    DBHandler.update("users", "user_id", user_id.strip().upper(),
                 {"status": STATUS_REJECTED})
    CSVHandler.update_row(
        USERS_CSV,
        key          = "user_id",
        value        = user_id.strip().upper(),
        updated_data = {"status": STATUS_REJECTED},
        fieldnames   = USER_FIELDS
    )
    print(f"  User '{row['name']}' has been rejected.")

def get_all_users(admin_user):
    if not admin_user.is_admin():
        raise PermissionDeniedError("Only administrators have access to view all users.")
    # Returning DB load as primary data source
    return DBHandler.load("users")