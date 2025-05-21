from fastapi import APIRouter, HTTPException
from app.helpers.scraper import Scraper
from app.models.post import Post
from typing import Optional

router = APIRouter()

scraper = Scraper()


last_scraped_post: Optional[Post] = None


@router.post("/scrape", response_model=Post)
def scrape_instagram_post(url: str):
    """
    Spustí scraping a uloží výsledek do paměti.
    """
    global last_scraped_post
    try:
        last_scraped_post = scraper.scrape(url=url)
        return last_scraped_post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/data", response_model=Post)
def get_scraped_data():
    """
    Vrátí poslední uložený post z paměti.
    """
    if last_scraped_post is None:
        raise HTTPException(status_code=404, detail="Žádná data zatím nejsou k dispozici.")
    return last_scraped_post
