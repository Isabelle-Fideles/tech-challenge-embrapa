```mermaid
flowchart LR
    E[Cliente Externo / Sistema Integrado] <--> |REST API| B
    A[Embrapa Fonte de Dados] <--> |Web Scraping| B[API Embrapa]
    B <--> |Fallback/Cache| C[(Banco de Dados / CSV)]
    B <--> |Aplicações| D[Dashboards/ ML]
```