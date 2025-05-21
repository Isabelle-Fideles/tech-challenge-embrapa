from sqlalchemy.orm import Session
from app.models.scraping import EmbrapaComercializacao, EmbrapaProducao, EmbrapaProcessamento, EmbrapaImportacao, EmbrapaExportacao
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


# ========== CRUD para Comercializacao ==========
def get_comercializacao(db: Session, ano: int, opcao: str):
    return db.query(EmbrapaComercializacao).filter(
        EmbrapaComercializacao.ano == ano,
        EmbrapaComercializacao.opcao == opcao,
    ).first()

def create_comercializacao(db: Session, ano: int, opcao: str, dados: dict, url: str):
    db_item = EmbrapaComercializacao(
        ano=ano,
        opcao=opcao,
        dados_json=json.dumps(dados),
        source_url=url
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ========== CRUD para Importacao ==========
def get_importacao(db: Session, ano: int, opcao: str,subopcao: str):
    return db.query(EmbrapaImportacao).filter(
        EmbrapaImportacao.ano == ano,
        EmbrapaImportacao.opcao == opcao,
        EmbrapaImportacao.subopcao == subopcao,
    ).first()

def create_importacao(db: Session, ano: int, opcao: str,subopcao: str, dados: dict, url: str):
    db_item = EmbrapaImportacao(
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


# ========== CRUD para Exportacao ==========
def get_exportacao(db: Session, ano: int, opcao: str,subopcao: str):
    return db.query(EmbrapaExportacao).filter(
        EmbrapaExportacao.ano == ano,
        EmbrapaExportacao.opcao == opcao,
        EmbrapaExportacao.subopcao == subopcao,
    ).first()

def create_exportacao(db: Session, ano: int, opcao: str,subopcao: str, dados: dict, url: str):
    db_item = EmbrapaExportacao(
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
