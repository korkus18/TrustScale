from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.helpers.analyzer import Analyzer
from app.helpers.scraper import Scraper
from app.models.result import Result
from app.models.post import Post
from app.constants import INSTAGRAM_APP_ID, INSTAGRAM_APP_SECRET

router = APIRouter(prefix="/analysis", tags=["analysis"])


class AnalysisRequest(BaseModel):
    url: HttpUrl


@router.post("/instagram")
async def analyze_instagram_post(post: Post) -> dict:
    """Analyze Instagram post using Basic Display API

    Args:
        post (Post): Instagram post data

    Returns:
        dict: Analysis results

    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Initialize scraper with access token
        # In production, you should store and manage access tokens securely
        scraper = Scraper(access_token="YOUR_ACCESS_TOKEN")
        
        # Scrape post data
        post_data = scraper.scrape(post.url)
        
        # Return analysis results
        return {
            "status": "success",
            "data": {
                "post": post_data.dict(),
                "analysis": {
                    "engagement_rate": calculate_engagement_rate(post_data),
                    "sentiment": analyze_sentiment(post_data.caption),
                    "hashtag_analysis": analyze_hashtags(post_data.hashtags)
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def calculate_engagement_rate(post: Post) -> float:
    """Calculate engagement rate for a post"""
    # Implement engagement rate calculation
    return 0.0

def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of post caption"""
    # Implement sentiment analysis
    return {"positive": 0.0, "negative": 0.0, "neutral": 1.0}

def analyze_hashtags(hashtags: list) -> dict:
    """Analyze hashtags used in post"""
    # Implement hashtag analysis
    return {"count": len(hashtags), "trending": []}

@router.post("/instagram", response_model=Result)
async def analyze_instagram_post_old(request: AnalysisRequest):
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