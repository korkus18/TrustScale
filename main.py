from fastapi import FastAPI
from app.routes import test

app = FastAPI()

app.include_router(test.router)
