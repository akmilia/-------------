from logging import getLogger

from fastapi import FastAPI

from database import lifespan
from middlewares import register_middlewares

from .config import settings
from .exceptions import register_exceptions
from .router import v1_router

from fastapi.middleware.cors import CORSMiddleware 

logger = getLogger(__name__)

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    openapi_url='/openapi.json' if settings.DEBUG else None,
    docs_url='/docs' if settings.DEBUG else None,
    redoc_url='/redoc' if settings.DEBUG else None,
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",  # URL вашего React приложения
    "http://127.0.0.1:5173",
    "https://localhost", 
    "http://localhost",
    "http://127.0.0.1",
] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

app = register_middlewares(app)
app = register_exceptions(app)
app.include_router(v1_router)
