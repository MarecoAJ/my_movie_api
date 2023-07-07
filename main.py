from fastapi import FastAPI, Body
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

@app.get("/movies", tags=["movies"])
def get_movies():
    return movies

@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return []

@app.get("/movies/", tags=["movies"])
def get_movies_by_category(category: str):
    return list(filter(lambda item: item['category'] == category , movies))

@app.post("/movies", tags=["movies"])
def create_movie(id: int =Body(), title: str =Body(), overview: str =Body(), year: int =Body(), rating:float =Body(), category:str =Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies