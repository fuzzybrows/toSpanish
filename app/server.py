import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import router
from app.settings import settings

logger = logging.getLogger(__name__)
format_str = "{levelname}:  {asctime} | {name} | {message}"
logging.basicConfig(level=logging.INFO, style="{", format=format_str)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)