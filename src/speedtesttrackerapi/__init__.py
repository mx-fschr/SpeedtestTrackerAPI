"""Intialization of the SpeedtestTrackerAPI Package"""

from .client import ApiClient
from .exceptions import ApiError, AuthenticationError, ResourceNotFoundError

__all__ = ["ApiClient", "ApiError", "AuthenticationError", "ResourceNotFoundError"]


def hello() -> str:
    return "Hello from speedtesttrackerapi!"
