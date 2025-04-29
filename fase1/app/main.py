from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(
    title="API Embrapa - POS Tech MLE - Fase 1",
    description="""
        Esta API coleta dados públicos da Embrapa Uva e Vinho,
        organizando informações de produção, processamento, comercialização, importação e exportação de uvas, vinhos e derivados.
    """,
    version="1.0.0"
)

# Roteador principal
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "API POS Tech MLE - Online"}


# 📈 Melhorar o logging (para saber se veio do scraping ou do cache)

# 🛡️ Criar error handler global para pegar qualquer erro inesperado e transformar em JSON bonito

# 📊 Criar métricas básicas (número de cache hits, número de scraping feitos)