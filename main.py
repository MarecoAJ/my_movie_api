from fastapi import  FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router

app = FastAPI()
app.title = "mi app fastAPI"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)
app.include_router(movie_router)

Base.metadata.create_all(bind = engine)

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
 
movies = [
    {
        "id": 1,
        "title": "avatar",
        "overview": "",
        "year": "2009",
        "rating": 7.8,
        "category": "accion"
    },
    {
        "id": 2,
        "title": "avatar",
        "overview": "",
        "year": "2009",
        "rating": 7.8,
        "category": "accion"
    }
]

@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>hola</h1>")

@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@mail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return  JSONResponse(status_code=200, content=token)