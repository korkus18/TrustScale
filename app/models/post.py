from pydantic import BaseModel


class Comment(BaseModel):
    comment: str


class Post(BaseModel):
    shortcode: str
    dimensions: str
    src: str
    srcAttached: List[str]
    hasAudio: bool
    videoUrl: str
    views: int
    plays: int
    likes: int
    location: str
    takenAt: datetime
    related: List[str]
    type: str
    videoDuration: float
    music: str
    isVideo: bool
    taggedUsers: List[str]
    captions: List[str]
    relatedProfiles: List[str]
    commentsCount: int
    commentsDisabled: bool
    commentsNextPage: str
    comments: List[Comment]
