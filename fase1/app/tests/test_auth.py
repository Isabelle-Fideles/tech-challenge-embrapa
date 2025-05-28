import pytest
from fastapi.testclient import TestClient
from base64 import b64encode
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core.security import authenticate_user
from app.main import app

app = FastAPI()

# Criamos uma rota fictícia protegida para testar o middleware
@app.get("/protected")
def protected_route(username: str = Depends(authenticate_user)):
    return {"message": f"Hello, {username}"}


client = TestClient(app)

def get_basic_auth_header(username: str, password: str) -> dict:
    credentials = f"{username}:{password}"
    encoded = b64encode(credentials.encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {encoded}"}


def test_auth_success():
    headers = get_basic_auth_header("admin", "!@#$Fiap2025")
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, admin"}


def test_auth_wrong_username():
    headers = get_basic_auth_header("wronguser", "!@#$Fiap2025")
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas."


def test_auth_wrong_password():
    headers = get_basic_auth_header("admin", "wrongpass")
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas."


def test_auth_missing_header():
    response = client.get("/protected")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers
