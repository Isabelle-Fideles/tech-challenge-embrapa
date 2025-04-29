from fastapi import APIRouter
from app.api.v1.endpoints import scraping

api_router = APIRouter()

# Scraping Embrapa
scraping_router = APIRouter(
    prefix="/embrapa",
    tags=["Embrapa"],
    responses={
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro interno no servidor"}
    }
)

scraping_router.include_router(scraping.router)

api_router.include_router(scraping_router)
