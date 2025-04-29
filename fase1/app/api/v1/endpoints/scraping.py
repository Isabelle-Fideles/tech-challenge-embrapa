from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.scraping import bs4_scraper
from app.schemas.scraping import EmbrapaScrapingRequestProcessamento, EmbrapaScrapingRequestProducao, EmbrapaScrapingResponse
from app.db.session import SessionLocal
from app.crud import scraping as crud_scraping
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# producao
@router.post(
    "/producao",
    response_model=EmbrapaScrapingResponse,
    responses={
        404: {
            "description": "Nenhuma tabela encontrada para o ano e opção informados.",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "DATA_NOT_FOUND",
                        "error_message": "Nenhuma tabela encontrada para o ano e opção informados."
                    }
                }
            }
        }
    }
)
def embrapa_producao(request: EmbrapaScrapingRequestProducao, db: Session = Depends(get_db)):
    """
    Banco de dados de uva, vinho e derivados.
    """
    # 1. Primeiro tenta buscar no banco
    cached_data = crud_scraping.get_producao(db, ano=request.ano, opcao=request.opcao)
    if cached_data:
        return EmbrapaScrapingResponse(
            source_url=cached_data.source_url,
            records_count=len(json.loads(cached_data.dados_json)["categorias"]),
            data=json.loads(cached_data.dados_json)
        )

    # 2. Se não achou, faz scraping
    result = bs4_scraper.embrapa(
        opcao=request.opcao,
        ano=request.ano,
    )

    # 3. Salva o resultado no banco
    crud_scraping.create_producao(db, ano=request.ano, opcao=request.opcao, dados=result["data"], url=result["source_url"])

    return result

# processamento
@router.post(
    "/processamento",
    response_model=EmbrapaScrapingResponse,
    responses={
        404: {
            "description": "Nenhuma tabela encontrada para o ano, opção ou subopção informados.",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "DATA_NOT_FOUND",
                        "error_message": "Nenhuma tabela encontrada para o ano e opção informados."
                    }
                }
            }
        }
    }
)
def embrapa_processamento(request: EmbrapaScrapingRequestProcessamento, db: Session = Depends(get_db)):
    """
    Banco de dados de uva, vinho e derivados - Processamento.
    """
    # 1. Verifica se já existe no banco
    cached_data = crud_scraping.get_processamento(db, ano=request.ano, opcao=request.opcao, subopcao=request.subopcao)
    if cached_data:
        return EmbrapaScrapingResponse(
            source_url=cached_data.source_url,
            records_count=len(json.loads(cached_data.dados_json)["categorias"]),
            data=json.loads(cached_data.dados_json)
        )

    # 2. Se não achou, faz scraping
    result = bs4_scraper.scrape_embrapa(
        opcao=request.opcao,
        ano=request.ano,
        subopcao=request.subopcao
    )

    # 3. Salva no banco
    crud_scraping.create_processamento(db, ano=request.ano, opcao=request.opcao, subopcao=request.subopcao, dados=result["data"], url=result["source_url"])

    return result