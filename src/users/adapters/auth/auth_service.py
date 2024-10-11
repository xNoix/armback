from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from shared.utils import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from users.domain.entities.user import User
from users.domain.services.user_service_impl import UserService
from users.adapters.persistence.user_repository_impl import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_service = UserService(UserRepository())
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_service.user_repository.get_by_username(username)
    if user is None:
        raise credentials_exception
    return User(id=user.id, username=user.username, email=user.email)
