from fastapi import FastAPI
from users.host.rest.user_controller import router as user_router
from config.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/users")
