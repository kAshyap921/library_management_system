# All custom exceptions for the system are defined here.
# Using specific exceptions is more descriptive than using a generic Exception class.

class LibraryError(Exception):
    """Base class for all library-related exceptions."""
    pass

class UserNotFoundError(LibraryError):
    """Raised when a user is not found during login or look-up."""
    pass

class InvalidCredentialsError(LibraryError):
    """Raised when the provided ID or password is incorrect."""
    pass

class UserNotVerifiedError(LibraryError):
    """Raised when the user exists but hasn't been approved by an admin yet."""
    pass

class UserAlreadyExistsError(LibraryError):
    """Raised when attempting to register with an ID that is already in use."""
    pass

class BookNotFoundError(LibraryError):
    """Raised when the requested book does not exist in the library records."""
    pass

class BookNotAvailableError(LibraryError):
    """Raised when a book is already rented out to someone else."""
    pass

class AlreadyIssuedError(LibraryError):
    """Raised if the user already has an active book issue under their name."""
    pass

class BookAlreadyExistsError(LibraryError):
    """Raised when attempting to add a book that already exists in the system."""
    pass

class PermissionDeniedError(LibraryError):
    """Raised when a regular member attempts to perform administrative tasks."""
    pass