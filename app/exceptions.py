class UserValidationError(Exception):
    """Raised when user input fails validation checks."""
    pass

class AuthenticationError(Exception):
    """Raised when authentication (login) fails."""
    pass

class NotFoundError(Exception):
    """Raised when a requested resource is not found in the database."""
    pass

class PermissionError(Exception):
    """Raised when authorization fails."""
    pass