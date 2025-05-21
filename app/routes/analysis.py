from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.helpers.analyzer import Analyzer
from app.helpers.scraper import Scraper
from app.models.result import Result

router = APIRouter(prefix="/analysis", tags=["analysis"])


class AnalysisRequest(BaseModel):
    url: HttpUrl


@router.post("/instagram", response_model=Result)
async def analyze_instagram_post(request: AnalysisRequest):
    """
    Analyze an Instagram post and provide detailed insights.
    
    Args:
        request (AnalysisRequest): The request containing the Instagram post URL
        
    Returns:
        Result: Detailed analysis of the Instagram post
        
    Raises:
        HTTPException: If there's an error during scraping or analysis
    """
    try:
        # Initialize scraper and analyzer
        scraper = Scraper()
        analyzer = Analyzer()
        
        # Scrape the post data
        post = scraper.scrape(str(request.url))
        
        # Analyze the post
        result = await analyzer.run(post)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}") 