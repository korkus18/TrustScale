from fastapi import FastAPI
from app.routes import test
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(test.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)