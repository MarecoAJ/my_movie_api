from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "mi app fastAPI"
app.version = "0.0.1"

movies = [
    {
        "id": 1,
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

@app.get("/movies", tags=["movies"])
def get_movies():
    return movies