```mermaid
flowchart TD
    subgraph API Rotas
        Cliente -->|POST /producao| Producao
        Producao -->|Consulta/Salva| DB
        Producao -->|Executa scraping| Scraping

        Cliente -->|POST /processamento| Processamento
        Processamento -->|Consulta/Salva| DB
        Processamento -->|Executa scraping| Scraping

        Cliente -->|POST /comercializacao| Comercializacao
        Comercializacao -->|Consulta/Salva| DB
        Comercializacao -->|Executa scraping| Scraping

        Cliente -->|POST /importacao| Importacao
        Importacao -->|Consulta/Salva| DB
        Importacao -->|Executa scraping| Scraping

        Cliente -->|POST /exportacao| Exportacao
        Exportacao -->|Consulta/Salva| DB
        Exportacao -->|Executa scraping| Scraping

        Scraping -->|Retorna dados| DB

    
        Producao
        Processamento
        Comercializacao
        Importacao
        Exportacao
    end

    

```
