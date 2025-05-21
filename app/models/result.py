from pydantic import BaseModel
from typing import List, Dict


class Commentary(BaseModel):
    positive: str
    neutral: str
    negative: str


class CategoryAnalysis(BaseModel):
    score: int
    commentary: Commentary
    pros: List[str]
    cons: List[str]
    tips: List[str]


class Result(BaseModel):
    engagement: CategoryAnalysis
    quality: CategoryAnalysis
    relevance: CategoryAnalysis
    audience_behavior: CategoryAnalysis
    average_score: int
    overall_pros: List[str]
    overall_cons: List[str]
    detail: str
