from sqlalchemy.orm import Session
from app.models.scraping import EmbrapaProducao, EmbrapaProcessamento
import json
# ========== CRUD para Produção ==========
def get_producao(db: Session, ano: int, opcao: str):
    return db.query(EmbrapaProducao).filter(
        EmbrapaProducao.ano == ano,
        EmbrapaProducao.opcao == opcao
    ).first()

def create_producao(db: Session, ano: int, opcao: str, dados: dict, url: str):
    db_item = EmbrapaProducao(
        ano=ano,
        opcao=opcao,
        dados_json=json.dumps(dados),
        source_url=url
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ========== CRUD para Processamento ==========
def get_processamento(db: Session, ano: int, opcao: str, subopcao: str):
    return db.query(EmbrapaProcessamento).filter(
        EmbrapaProcessamento.ano == ano,
        EmbrapaProcessamento.opcao == opcao,
        EmbrapaProcessamento.subopcao == subopcao
    ).first()

def create_processamento(db: Session, ano: int, opcao: str, subopcao: str, dados: dict, url: str):
    db_item = EmbrapaProcessamento(
        ano=ano,
        opcao=opcao,
        subopcao=subopcao,
        dados_json=json.dumps(dados),
        source_url=url
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item