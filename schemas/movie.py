from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15)
    overview: str = Field(min_length=15)
    year: int =Field(le=2023)
    rating: float
    category: str
