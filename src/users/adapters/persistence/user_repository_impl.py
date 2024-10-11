from users.domain.ports.output.user_repository import UserRepositoryInterface
from users.domain.entities.user import UserInDB
from sqlalchemy.orm import Session
from config.database import SessionLocal, Base
from users.adapters.persistence.models import UserModel

class UserRepository(UserRepositoryInterface):
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_by_username(self, username: str) -> UserInDB:
        user = self.db.query(UserModel).filter(UserModel.username == username).first()
        if user:
            return UserInDB(
                id=user.id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password
            )
        return None

    def create(self, user: UserInDB) -> UserInDB:
        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        user.id = db_user.id
        return user
