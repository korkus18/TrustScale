from pydantic import BaseModel


class Result(BaseModel):
    score: int
    pros: list[str]
    cons: list[str]
    detail: str
