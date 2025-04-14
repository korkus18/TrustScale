from fastapi import APIRouter, HTTPException
from helpers.scraper import Scraper
from models.post import Post

router = APIRouter()

scraper = Scraper()


last_scraped_post: Post | None = None


@router.post("/scrape", response_model=Post)
async def scrape_instagram_post(url: str):
    """
    Spustí scraping a uloží výsledek do paměti.
    """
    global last_scraped_post
    try:
        last_scraped_post = await scraper.fetch_instagram_data(url=url)
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
