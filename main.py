from fastapi import  FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "mi app fastAPI"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind = engine)

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