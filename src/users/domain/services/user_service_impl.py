from users.domain.ports.input.user_service import UserServiceInterface
from users.domain.ports.output.user_repository import UserRepositoryInterface
from users.domain.entities.user import User, UserCreate, UserInDB
from shared.utils import get_password_hash, verify_password

class UserService(UserServiceInterface):
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def create_user(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        user_in_db = UserInDB(
            id=None,
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        created_user = self.user_repository.create(user_in_db)
        return User(id=created_user.id, username=created_user.username, email=created_user.email)

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.user_repository.get_by_username(username)
        if user and verify_password(password, user.hashed_password):
            return User(id=user.id, username=user.username, email=user.email)
        return None
