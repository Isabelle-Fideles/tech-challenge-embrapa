from fastapi import APIRouter
from app.api.v1.endpoints import scraping

api_router = APIRouter()

# Scraping Embrapa
scraping_router = APIRouter(
    prefix="/embrapa",
    tags=["Embrapa"],
    responses={
        404: {"description": "Dados não encontrados para os parâmetros fornecidos."},
        500: {"description": "Erro interno inesperado na aplicação."},
        503: {"description": "Serviço externo (Embrapa) está indisponível no momento."}
    }
)

scraping_router.include_router(scraping.router)

api_router.include_router(scraping_router)
