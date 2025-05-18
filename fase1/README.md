# Projeto: API Embrapa Uva e Vinho - POS Tech MLE

## 📝 Descrição
API para coleta estruturada de dados públicos da Embrapa, focando nas abas de:
- Produção
- Processamento
- Comercialização
- Importação
- Exportação

Esses dados servirão de base para análise e construção de modelos de **Machine Learning** no futuro.

---

## 🛠️ Tecnologias
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite (para a FASE 1)
- Alembic
- BeautifulSoup4

---

## 🗂️ Estrutura do Projeto

Estrutura modular baseada em boas práticas de FastAPI e princípios de Clean Architecture:

- Separação clara por camadas (`api/`, `core/`, `models/`, `schemas/`, `crud/`)
- Roteamento versionado (`/api/v1/...`)

```
📦 API Embrapa - POS Tech MLE
├── 📁 app
│   ├── 📁 alembic                  # Migrations do banco de dados
│   │   └── __init__.py
│   ├── 📁 api                      # Camada de API
│   │   └── 📁 v1                   # Versão da API
│   │       ├── api.py             # Roteador principal
│   │       ├── 📁 docs            # Documentação e responses
│   │       │   ├── embrapa.py
│   │       │   └── responses.py
│   │       ├── 📁 endpoints       # Endpoints da API
│   │       │   ├── __init__.py
│   │       │   └── scraping.py
│   │       └── __init__.py
│   ├── 📁 core                     # Configurações e segurança
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   ├── 📁 middleware
│   │   │   └── docs_auth.py       # Proteção da doc Swagger
│   │   └── security.py            # JWT, OAuth2, HTTPBasic, etc.
│   ├── 📁 crud                     # Camada de persistência
│   │   ├── __init__.py
│   │   └── scraping.py
│   ├── 📁 db                       # Sessão e base SQLAlchemy
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── session.py
│   ├── 📁 models                   # Modelos ORM
│   │   ├── __init__.py
│   │   └── scraping.py
│   ├── 📁 schemas                  # Modelos Pydantic
│   │   ├── __init__.py
│   │   └── scraping.py
│   ├── 📁 scraping                 # Módulos de scraping
│   │   ├── bs4_scraper.py         # Serviço genérico
│   │   ├── exportacao.py          # Customizações específicas
│   │   ├── importacao.py
│   │   ├── __init__.py
│   │   └── 📁 mok                  # Mocks HTML locais
│   │       ├── opt_02.html
│   │       ├── opt_03.html
│   │       ├── opt_04.html
│   │       ├── opt_05.html
│   │       └── opt_06.html
│   └── 📁 tests                    # Testes automatizados
│       └── __init__.py
├── 🚀 main.py                      # Ponto de entrada da aplicação
├── ⚙️ create_db.py                 # Script para criação inicial do banco
├── 🗃️ embrapa.db                   # Banco SQLite
├── 📄 poetry.lock                  # Lockfile de dependências
├── 📄 pyproject.toml               # Configuração do projeto (Poetry)
├── 📄 requirements.txt            # Alternativa ao Poetry
├── 📄 README.md                    # Documentação do projeto
```
---

## ⚙️ Instalação e Execução
```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
poetry install
poetry shell
uvicorn app.main:app --reload
```
---

## 🔐 Autenticação
Autenticação via **HTTPBasic** foi implementada (FASE 1) como proteção opcional da documentação (Swagger):
- Middleware: app/core/middleware/docs_auth.py (**DESABILITADO**)
- Rota protegida: /docs (**HABILITADO**)
---


## 🌍 Variáveis de Ambiente (.env)
```bash 
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=supersecret
```
---

## 🧪 Testes
```bash 
WP pytest
```
---

## 🔁 Fluxo de Funcionamento
1. Usuário envia uma requisição POST para /api/v1/embrapa/*
2. A rota é tratada por um endpoint na API
3. Um scraper realiza a busca dos dados na Embrapa via BeautifulSoup
4. Os dados são parseados e cacheados em banco local (SQLite)
5. A resposta é formatada em JSON conforme Schema Pydantic

---

## 🗺️ Fluxo Detalhado da API

| Etapa | Descrição                                        | Arquivo                            |
| :---- | :----------------------------------------------- | :--------------------------------- |
| 1     | API recebe requisição                            | `app/main.py`                      |
| 2     | Requisição roteada pela API v1                   | `app/api/v1/api.py`                |
| 3     | Endpoint `embrapa_producao()` ou outro é chamado | `app/api/v1/endpoints/scraping.py` |
| 4     | Serviço de scraping é ativado                    | `app/scraping/bs4_scraper.py`      |
| 5     | Parser executado com BeautifulSoup               | `app/scraping/bs4_scraper.py`      |
| 6     | Verifica se dados existem no banco               | `app/crud/scraping.py`             |
| 7     | Se não existir, salva dados no banco             | `app/crud/scraping.py`             |
| 8     | Formata dados com Pydantic                       | `app/schemas/scraping.py`          |
| 9     | Resposta JSON enviada ao cliente                 | FastAPI                            |


---


## 🗺️ Arquitetura da API Embrapa (Fluxo Completo)

```text
+---------------------------+
|  Usuário / Client (POST)  |
+------------+--------------+
             |
             v
+------------------------------+
| API: /api/v1/embrapa/*       |  <-- Etapa 1
+-------------+----------------+
              |
              v
+------------------------------+
| Roteador API v1              |  <-- Etapa 2
| (app/api/v1/api.py)          |
+-------------+----------------+
              |
              v
+------------------------------------------+
| Endpoint específico                      |  <-- Etapa 3
| (e.g. embrapa_producao())                |
| (app/api/v1/endpoints/scraping.py)       |
+---------------------+--------------------+
                      |
                      v
+-------------------------------------------+
| Serviço de Scraping                       |  <-- Etapa 4
| (bs4_scraper.scrape_embrapa)              |
| (app/scraping/bs4_scraper.py)             |
+---------------------+---------------------+
                      |
                      v
+----------------------------------------------------+
| Requisição HTTP à Embrapa + Parser (BS4)          |  <-- Etapa 5
| parse_table / parse_import_export_table           |
| (app/scraping/bs4_scraper.py)                     |
+---------------------+-----------------------------+
                      |
                      v
      +---------------+------------------+
      |                                  |
      v                                  v
+---------------------+       +-------------------------+
| Verifica se existe  |       | Faz scraping e salva    |  <-- Etapas 6 e 7
| no banco (GET)      |       | no banco (CREATE)       |
| (crud/scraping.py)  |       | (crud/scraping.py)      |
+---------------------+       +-------------------------+
              \                      /
               \                    /
                \                  /
                 v                v
          +-----------------------------+
          | Dados formatados no Schema  |  <-- Etapa 8
          | (Pydantic -                 |
          | schemas/scraping.py)        |
          +-----------------------------+
                       |
                       v
         +-------------------------------+
         |  Resposta JSON                |  <-- Etapa 9
         +-------------------------------+
```

---

## 📊 Cenário de Aplicação em Machine Learning
Os dados coletados poderão ser utilizados para:
- **Predição de produção de uvas por estado**
- **Classificação de tipos de vinho por perfil de exportação**
- **Análise de tendências na comercialização e importação**


---

## 🚀 Plano de Deploy (MVP)

O projeto pode ser facilmente publicado em:

- Railway (deploy contínuo via Git)
- Render.com
- **Docker + Uvicorn em VPS (Ex: EC2)**

---
## 🔗 Rotas disponíveis

- /api/v1/embrapa/producao
- /api/v1/embrapa/processamento
- /api/v1/embrapa/comercializacao
- /api/v1/embrapa/importacao
- /api/v1/embrapa/exportacao

## 📄 Licença
MIT License.
