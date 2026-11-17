from abc import ABC, abstractmethod
from app.schemas import PlatformResult


class BasePlatform(ABC):
    """
    Every platform class must inherit from this base class
    and implement the post() method.
    """

    platform_name: str = "Unknown"

    @abstractmethod
    def post(self, message: str) -> PlatformResult:
        """
        Post the message to the platform.
        Must return a PlatformResult object.
        """
        pass