from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import router
from app.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)