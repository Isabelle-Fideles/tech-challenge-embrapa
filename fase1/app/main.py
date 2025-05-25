from fastapi import FastAPI,Request, Response
from app.api.v1.api import api_router
import sys
import os
from dotenv import load_dotenv
# from app.core.middleware.docs_auth import DocsAuthMiddleware


# Carrega variáveis do .env
load_dotenv()

# Lista de variáveis obrigatórias do projeto:
REQUIRED_ENV_VARS = [
    "EMBRAPA_BASE_URL",
    "DATABASE_URL",
    "DOCS_USER",
    "DOCS_PASSWORD",
]

missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

if missing_vars:
    print("\n❌ ERRO DE CONFIGURAÇÃO:\n")
    print(f"As seguintes variáveis obrigatórias não foram definidas no ambiente ou no arquivo .env: {', '.join(missing_vars)}")
    print("Por favor, configure todas as variáveis obrigatórias antes de iniciar a aplicação.\n")
    sys.exit(1)
    

app = FastAPI(
    title="API Embrapa - POS Tech MLE - Fase 1",
    description="""
**A API Embrapa Vitibrasil** disponibiliza dados públicos sobre a cadeia produtiva da vitivinicultura no Brasil, com foco especial no Estado do Rio Grande do Sul — responsável por mais de 90% da produção nacional.

Através desta API, é possível acessar informações sobre:
- Quantidade de uvas processadas
- Produção e comercialização de vinhos, sucos e derivados
- Importação e exportação de produtos vitivinícolas

As informações são extraídas diretamente do site oficial da Embrapa Uva e Vinho, sendo organizadas por ano, tipo de produto e natureza da operação (produção, comercialização, importação ou exportação).
    """,
    version="0.1.0"
)


# app.add_middleware(DocsAuthMiddleware)

# Roteador principal
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "API POS Tech MLE - Online"}


#Melhorar o logging (para saber se veio do scraping ou do cache)

#Criar error handler global para pegar qualquer erro inesperado e transformar em JSON bonito

#Criar métricas básicas (número de cache hits, número de scraping feitos)