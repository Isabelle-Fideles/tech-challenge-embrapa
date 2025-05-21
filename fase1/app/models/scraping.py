from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class EmbrapaProducao(Base):
    __tablename__ = "embrapa_producao"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    opcao = Column(String(10), index=True)
    dados_json = Column(Text)  # Aqui armazenamos a resposta parseada em JSON
    source_url = Column(String(255))


# Tabela de Processamento
class EmbrapaProcessamento(Base):
    __tablename__ = "embrapa_processamento"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    opcao = Column(String(10), index=True)
    subopcao = Column(String(20), index=True)  # Subopcao usada para filtrar no scraping
    dados_json = Column(Text)  # Dados extraídos da Embrapa, armazenados em formato JSON
    source_url = Column(String(255))  # URL de origem do scraping
    
    
    
# Tabela de Comercializacao
class EmbrapaComercializacao(Base):
    __tablename__ = "embrapa_comercializacao"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    opcao = Column(String(10), index=True)
    dados_json = Column(Text)  # Dados extraídos da Embrapa, armazenados em formato JSON
    source_url = Column(String(255))  # URL de origem do scraping


    
# Tabela de Importacao
class EmbrapaImportacao(Base):
    __tablename__ = "embrapa_importacao"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    opcao = Column(String(10), index=True)
    subopcao = Column(String(20), index=True)  # Subopcao usada para filtrar no scraping
    dados_json = Column(Text)  # Dados extraídos da Embrapa, armazenados em formato JSON
    source_url = Column(String(255))  # URL de origem do scraping


# Tabela de Exportacao
class EmbrapaExportacao(Base):
    __tablename__ = "embrapa_exportacao"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    opcao = Column(String(10), index=True)
    subopcao = Column(String(20), index=True)  # Subopcao usada para filtrar no scraping
    dados_json = Column(Text)  # Dados extraídos da Embrapa, armazenados em formato JSON
    source_url = Column(String(255))  # URL de origem do scraping