from abc import ABC, abstractmethod
from users.domain.entities.user import UserInDB

class UserRepositoryInterface(ABC):

    @abstractmethod
    def get_by_username(self, username: str) -> UserInDB:
        pass

    @abstractmethod
    def create(self, user: UserInDB) -> UserInDB:
        pass
