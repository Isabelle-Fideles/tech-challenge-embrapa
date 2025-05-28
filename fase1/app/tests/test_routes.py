import pytest
from fastapi.testclient import TestClient
from base64 import b64encode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.scraping import EmbrapaProducao

# Configuração do banco de testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Substitui o banco de dados na app
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Aponta o get_db usado na app para o banco de teste
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def get_auth_headers():
    user_pass = b"admin:!@#$Fiap2025"
    encoded = b64encode(user_pass).decode("utf-8")
    return {"Authorization": f"Basic {encoded}"}

dadosDB_json = '''
{
  "categorias": [
    {
      "categoria": "VINHO DE MESA",
      "produtos": [
        {
          "produto": "Produto A",
          "quantidade_litros": "100"
        }
      ]
    },
    {
      "categoria": "ESPUMANTE",
      "produtos": [
        {
          "produto": "Produto B",
          "quantidade_litros": "200"
        }
      ]
    }
  ],
  "total_litros": "123456",
  "records_count": 2
}
'''

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Cria o schema e popula dados
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    db.add(EmbrapaProducao(ano=2024, opcao="opt_02", dados_json=dadosDB_json, source_url="http://test.url"))
    db.commit()
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_producao_success():
    headers = get_auth_headers()
    response = client.post("api/v1/embrapa/producao", json={"ano": 2024, "opcao": "opt_02"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


def test_get_producao_no_auth():
    response = client.post("api/v1/embrapa/producao", json={"ano": 2024, "opcao": "opt_02"})
    assert response.status_code == 401


def test_get_producao_not_found():
    headers = get_auth_headers()
    response = client.post(
        "/api/v1/embrapa/producao",
        json={"ano": 2020, "opcao": "opt_02"},
        headers=headers
    )
    assert response.status_code == 503 # Espera 503 pois não há dados para 2020
