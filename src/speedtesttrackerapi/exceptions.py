"""Exception classes for the SpeedtestTrackerAPI Package"""

from typing import Optional


class ApiError(Exception):
    """Base Exception for the SpeedtestTrackerAPI Package"""

    pass


class AuthenticationError(ApiError):
    """Exception raised for errors in authentication due to wrong api keys or login credentials"""

    pass


class ResourceNotFoundError(ApiError):
    """Exception raised if a resource could not be found"""

    pass


class ForbiddenError(Exception):
    """Forbidden error response when user lacks permission"""

    message: Optional[str]


class NotAcceptableError(Exception):
    """Error response when the Accept header is missing or invalid"""

    message: Optional[str]
    error: Optional[str]


class NotFoundError(Exception):
    """Error when a requested result is not found"""

    message: Optional[str]


class UnauthenticatedError(Exception):
    """Error when User is not authenticated"""

    message: Optional[str]


class ValidationError(Exception):
    """Validation failed due to invalid server_id input"""

    message: Optional[str]
