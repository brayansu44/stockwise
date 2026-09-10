from abc import ABC, abstractmethod


class TokenService(ABC):

    @abstractmethod
    def create_access_token(self, subject: str) -> str:
        pass

    @abstractmethod
    def decode_access_token(self, token: str) -> str:
        pass