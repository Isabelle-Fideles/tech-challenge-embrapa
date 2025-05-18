from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.scraping import bs4_scraper
from app.schemas.scraping import EmbrapaScrapingRequestComercializacao, EmbrapaScrapingRequestExportacao, EmbrapaScrapingRequestImportacao, EmbrapaScrapingRequestProcessamento, EmbrapaScrapingRequestProducao, EmbrapaScrapingResponse
from app.db.session import SessionLocal
from app.crud import scraping as crud_scraping
import json
from app.api.v1.docs.responses import common_responses
from app.api.v1.docs.embrapa import producao_description, processamento_description, comercializacao_description,importacao_description, exportacao_description
from app.core.exceptions import EmbrapaDataNotFoundException, ExternalServiceUnavailableException
from app.core.security import authenticate_user
from app.scraping.importacao import EmbrapaImportacaoResponse
from app.scraping.exportacao import EmbrapaExportacaoResponse

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
    dependencies=[Depends(authenticate_user)],
    responses={**common_responses}
)
def embrapa_producao(request: EmbrapaScrapingRequestProducao, db: Session = Depends(get_db)):
    try:
        # 1. Primeiro tenta buscar no banco
        cached_data = crud_scraping.get_producao(db, ano=request.ano, opcao=request.opcao)
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
        )

        # 3. Salva o resultado no banco
        crud_scraping.create_producao(db, ano=request.ano, opcao=request.opcao, dados=result["data"], url=result["source_url"])

        return result
    except EmbrapaDataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalServiceUnavailableException as e:
        raise HTTPException(status_code=503, detail=str(e))

# processamento
@router.post(
    "/processamento",
    response_model=EmbrapaScrapingResponse,
    dependencies=[Depends(authenticate_user)],
    responses={ **common_responses}
)
def embrapa_processamento(request: EmbrapaScrapingRequestProcessamento, db: Session = Depends(get_db)):
    
    try:
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
    except EmbrapaDataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalServiceUnavailableException as e:
        raise HTTPException(status_code=503, detail=str(e))

# comercializacao
@router.post(
    "/comercializacao", 
    response_model=EmbrapaScrapingResponse, 
    dependencies=[Depends(authenticate_user)], 
    responses={**common_responses})
def embrapa_comercializacao(request: EmbrapaScrapingRequestComercializacao, db: Session = Depends(get_db)):
    try:
         # 1. Verifica se já existe no banco
        cached = crud_scraping.get_comercializacao(db, ano=request.ano, opcao=request.opcao)
        if cached:
            return EmbrapaScrapingResponse(
                source_url=cached.source_url,
                records_count=len(json.loads(cached.dados_json)["categorias"]),
                data=json.loads(cached.dados_json)
            )
        # 2. Se não achou, faz scraping
        result = bs4_scraper.scrape_embrapa(
            opcao=request.opcao,
            ano=request.ano
        )
        
        # 3. Salva no banco
        crud_scraping.create_comercializacao(db, ano=request.ano, opcao=request.opcao, dados=result["data"], url=result["source_url"])
        return result
    except EmbrapaDataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalServiceUnavailableException as e:
        raise HTTPException(status_code=503, detail=str(e))

# importacao
@router.post(
    "/importacao", 
    response_model=EmbrapaImportacaoResponse, 
    dependencies=[Depends(authenticate_user)], 
    responses={**common_responses})
def embrapa_importacao(request: EmbrapaScrapingRequestImportacao, db: Session = Depends(get_db)):
    try:
         # 1. Verifica se já existe no banco
        cached = crud_scraping.get_importacao(db, ano=request.ano, opcao=request.opcao, subopcao=request.subopcao)
        if cached:
            cached_data = json.loads(cached.dados_json)
            records_count = len(cached_data.get("categorias") or cached_data.get("itens") or [])

            return EmbrapaImportacaoResponse(
                source_url=cached.source_url,
                records_count=records_count,
                data=cached_data
            )
        # 2. Se não achou, faz scraping
        result = bs4_scraper.scrape_embrapa(
            opcao=request.opcao,
            ano=request.ano,
            subopcao=request.subopcao
        )
        
        # 3. Salva no banco
        crud_scraping.create_importacao(db, ano=request.ano, opcao=request.opcao, subopcao=request.subopcao, dados=result["data"], url=result["source_url"])
        return result
    except EmbrapaDataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalServiceUnavailableException as e:
        raise HTTPException(status_code=503, detail=str(e))

# exportacao
@router.post(
    "/exportacao", 
    response_model=EmbrapaExportacaoResponse, 
    dependencies=[Depends(authenticate_user)], 
    responses={**common_responses})
def embrapa_exportacao(request: EmbrapaScrapingRequestExportacao, db: Session = Depends(get_db)):
    try:
         # 1. Verifica se já existe no banco
        cached = crud_scraping.get_exportacao(db, ano=request.ano, opcao=request.opcao, subopcao=request.subopcao)
        if cached:
            cached_data = json.loads(cached.dados_json)
            records_count = len(cached_data.get("categorias") or cached_data.get("itens") or [])

            return EmbrapaExportacaoResponse(
                source_url=cached.source_url,
                records_count=records_count,
                data=cached_data
            )
        # 2. Se não achou, faz scraping
        result = bs4_scraper.scrape_embrapa(
            opcao=request.opcao,
            ano=request.ano,
            subopcao=request.subopcao
        )
        
        # 3. Salva no banco
        crud_scraping.create_exportacao(db, ano=request.ano, opcao=request.opcao, subopcao=request.subopcao, dados=result["data"], url=result["source_url"])
        return result
    except EmbrapaDataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalServiceUnavailableException as e:
        raise HTTPException(status_code=503, detail=str(e))


# Adicionando docstrings aos endpoints
# Essas docstrings serão utilizadas na documentação OpenAPI
embrapa_producao.__doc__ = producao_description
embrapa_processamento.__doc__ = processamento_description
embrapa_comercializacao.__doc__ = comercializacao_description
embrapa_importacao.__doc__ = importacao_description
embrapa_exportacao.__doc__ = exportacao_description