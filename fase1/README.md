# Projeto: API Embrapa Uva e Vinho - POS Tech MLE

## Descrição
API para coleta estruturada de dados públicos da Embrapa, focando em produção, processamento, comercialização, importação e exportação de uvas e vinhos.

## Tecnologias
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite (inicialmente)
- Alembic
- BeautifulSoup4

## Estrutura do Projeto - Um misto pragmático entre:
- **Clean Architecture** → separação de camadas lógicas (api/, core/, models/, schemas/, crud/)
- **Best Practices de FastAPI** → organizada por "domínios" e com separação por versão de API.

```
├📦 app
├── 📂 alembic
├── 📂 api
│   └── 📂 v1
│       ├── 📄 api.py
│       ├── 📂 endpoints
│       │   ├── 📄 __init__.py
│       │   └── 📄 scraping.py
│       └── 📄 __init__.py
├── 📂 core
│   └── 📄 exceptions.py
├── 📂 crud
│   └── 📄 scraping.py
├── 📂 db
│   ├── 📄 base.py
│   └── 📄 session.py
├── 📄 main.py
├── 📂 models
│   └── 📄 scraping.py
├── 📂 schemas
│   └── 📄 scraping.py
├── 📂 scraping
│   └── 📄 bs4_scraper.py
└── 📂 tests
📄 create_db.py
📄 embrapa.db
📄 README.md
📄 requirements.txt
```
---

## Instalação WP
```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
poetry install
poetry shell
```
---

## Variáveis de Ambiente (.env) WP
```bash 
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=supersecret
```
---

## Atualização do DB SQLite Sempre que Necessário
```bash 
poetry run python create_db.py
```
---
## Rodando o Projeto
```bash 
uvicorn app.main:app --reload
```
---

## Testes WP
```bash 
pytest 
```
---

## Observações Técnicas
1. Toda entrada (requests) e saída (responses) são validadas **por Schemas Pydantic**
2. Persistência usa **SQLAlchemy ORM** para garantir compatibilidade com múltiplos bancos de dados.
3. Scraping é feito usando **requests** para download de HTML e **BeautifulSoup4** para parsing dos dados.
4. **Caching inteligente** é utilizado via `lru_cache (Least Recently Used)` para otimizar scraping repetitivo.
5. O projeto foi modularizado em camadas para garantir `manutenção`, `escalabilidade` e `boas práticas de desenvolvimento`.

---

## Arquitetura de Fluxo de Chamadas

Esta seção descreve o fluxo de funcionamento da API de Scraping da Embrapa.

O ciclo de uma requisição é composto por:

1. **Recepção da requisição HTTP** (FastAPI)
2. **Chamadas de Endpoint** (`app/api/v1/endpoints/`)
3. **Lógica de Scraping** (`app/scraping/bs4_scraper.py`)
4. **Validação e formatação de dados** (Pydantic Schemas)
5. **Persistência no Banco de Dados** (SQLAlchemy ORM)

---

## Fluxo detalhado passo a passo

| Etapa | Descrição | Arquivo |
|:------|:----------|:--------|
| 1 | FastAPI recebe a requisição POST em `/api/v1/embrapa/producao` ou `/api/v1/embrapa/processamento` | `app/main.py` |
| 2 | A requisição é roteada para o módulo correto de API (versão e prefixo) | `app/api/v1/api.py` |
| 3 | O endpoint específico é chamado: função `embrapa_producao()` ou `embrapa_processamento()` | `app/api/v1/endpoints/scraping.py` |
| 4 | O serviço de scraping é ativado para buscar os dados da Embrapa | `app/scraping/bs4_scraper.py` |
| 5 | O HTML da página é baixado (requests) e parseado (BeautifulSoup) usando `parse_table` ou `parse_import_export_table` | `app/scraping/bs4_scraper.py` |
| 6 | Se os dados já existirem no banco, são carregados via `get_producao()` ou `get_processamento()` | `app/crud/scraping.py` |
| 7 | Se os dados não existirem, o scraping é salvo no banco com `create_producao()` ou `create_processamento()` | `app/crud/scraping.py` |
| 8 | A resposta é formatada para JSON conforme o schema Pydantic | `app/schemas/scraping.py` |
| 9 | A resposta formatada é devolvida ao usuário pela API | (Resposta HTTP) |

---


## Licença
MIT License.
