"""Application configuration - root APIRouter.

Defines all FastAPI application endpoints.
"""

from fastapi import APIRouter

from app.controllers.v1 import llm, studio, video

root_api_router = APIRouter()
# v1
root_api_router.include_router(video.router)
root_api_router.include_router(llm.router)
root_api_router.include_router(studio.router)
