from abc import ABC, abstractmethod
from users.domain.entities.user import User, UserCreate

class UserServiceInterface(ABC):

    @abstractmethod
    def create_user(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    def authenticate_user(self, username: str, password: str) -> User:
        pass
