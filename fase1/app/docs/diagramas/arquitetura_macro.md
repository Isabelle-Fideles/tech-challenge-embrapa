```mermaid
flowchart LR
    A[Embrapa Fonte de Dados] -->|Web Scraping| B[API Embrapa FastAPI]
    B -->|Fallback/Cache| C[(Banco de Dados / CSV)]
    B --> D[Dashboards / Aplicações / ML]
```