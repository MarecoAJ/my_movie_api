from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token

user_router = APIRouter()

class User(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "ejemplo": {
                "id": 1,
                "title": "nombre de la peli",
                "overview": "descripcion de la peli",
                "year": 2023,
                "rating": 6.0,
                "category": "cine"
            }
        }

@user_router.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@mail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return  JSONResponse(status_code=200, content=token)