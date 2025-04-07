from fastapi import APIRouter, HTTPException
from app.helpers.scraper import Scraper
from app.models.post import Post

router = APIRouter()

scraper = Scraper()


@router.get("/test", response_model=Post)
def scrape_instagram_post(url: str):
    """
    Scrapes Instagram post data and returns it as a structured Post model.
    """
    try:
        return scraper.scrape(shortcode="DIGYx2ZMwFv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
