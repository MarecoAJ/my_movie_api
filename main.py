from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List
from starlette.requests import Request
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "mi app fastAPI"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@mail.com":
            raise HTTPException(status_code=403, detail="credenciales no validas")
    
class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15)
    overview: str = Field(min_length=15)
    year: int =Field(le=2023)
    rating: float
    category: str

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

@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer)])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse( status_code=200, content=item)
    return JSONResponse(status_code=404, content=[])

@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(status_code=200, content= data)

@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie:Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"mensaje": "se agrego la peli"})

@app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
    return JSONResponse(status_code=200, content={"mensaje": "se modifico la peli"})

@app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return JSONResponse(status_code=200, content={"mensaje": "se elimino la peli"})