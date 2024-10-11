from fastapi import APIRouter, Depends, HTTPException, status
from users.domain.entities.user import User, UserCreate
from users.domain.services.user_service_impl import UserService
from users.adapters.persistence.user_repository_impl import UserRepository
from users.adapters.auth.auth_service import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from shared.utils import create_access_token

router = APIRouter()
user_service = UserService(UserRepository())

@router.post("/register", response_model=User)
def register(user: UserCreate):
    existing_user = user_service.user_repository.get_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return user_service.create_user(user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
