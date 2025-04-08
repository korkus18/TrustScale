from pydantic import BaseModel
from typing import Optional


class Author(BaseModel):
    username: str
    full_name: str
    id: str


class Location(BaseModel):
    name: Optional[str]
    lat: Optional[float]
    lng: Optional[float]


class CarouselItem(BaseModel):
    media_url: str
    is_video: bool
    accessibility_caption: Optional[str]


class Post(BaseModel):
    author: Author
    caption: str
    hashtags: list[str]
    media_url: str
    is_video: bool
    timestamp: int
    like_count: int
    comment_count: Optional[int]
    accessibility_caption: Optional[str]
    location: Location
    tagged_users: Optional[list[str]]  # Or replace str with a model if you know the structure
    carousel: Optional[list[CarouselItem]]
