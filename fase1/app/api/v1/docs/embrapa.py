producao_description = """
    Consulta a produção de vinhos, sucos e derivados do Rio Grande do Sul no banco de dados da Embrapa.

    Este endpoint realiza scraping direto no site oficial da Embrapa Uva e Vinho, ou retorna dados em cache local persistido em banco de dados.

    ### Parâmetros esperados no corpo da requisição (JSON):

    - **opcao** (`str`, obrigatório):  
    Valor fixo `"opt_02"`, que identifica a seção de **Produção** no site da Embrapa.

    - **ano** (`int`, obrigatório):  
    Ano da consulta. Aceita valores entre `1970` e `2024`.  
    Se não informado, o sistema tentará trazer o dado mais recente disponível.

    ### Exemplo de requisição:

    ```json
    {
    "opcao": "opt_02",
    "ano": 2024
    }
    ```
    Caso o dado já esteja disponível no cache/banco local, ele será retornado diretamente.
    Se não estiver, o sistema fará scraping em tempo real e salvará o resultado.
    """

processamento_description = """
    Consulta os dados de processamento de uvas no estado do Rio Grande do Sul, conforme publicado pela Embrapa Uva e Vinho.

    Este endpoint realiza scraping direto no site oficial da Embrapa ou retorna os dados previamente armazenados no banco local (cache).

    ### Parâmetros esperados no corpo da requisição (JSON):

    - **opcao** (`str`, obrigatório):  
    Valor fixo `"opt_03"`, correspondente à seção de **Processamento** da Embrapa.

    - **ano** (`int`, obrigatório):  
    Ano de referência da consulta. Deve estar entre `1970` e `2024`.

    - **subopcao** (`str`, opcional):  
    Tipo de uva processada. Os valores aceitos são:
    - `"subopt_01"` → Viníferas (padrão)
    - `"subopt_02"` → Americanas e híbridas
    - `"subopt_03"` → Uvas de mesa
    - `"subopt_04"` → Sem classificação

    Se não informado, será utilizado `"subopt_01"` como padrão.

    ### Exemplo de requisição:

    ```json
    {
    "opcao": "opt_03",
    "ano": 2024,
    "subopcao": "subopt_01"
    }
    ```
    Se os dados estiverem disponíveis no banco local, serão retornados imediatamente.
    Caso contrário, será realizado o scraping em tempo real e o resultado será armazenado para uso futuro.
    """
    
comercializacao_description = """
Consulta dados de comercialização de vinhos e derivados do RS, conforme informações da Embrapa.

Este endpoint realiza scraping direto no site oficial da Embrapa Uva e Vinho, ou retorna dados em cache local persistido em banco de dados.

### Parâmetros esperados no corpo da requisição (JSON):

- **opcao** (`str`, obrigatório):  
Valor fixo `"opt_04"`, que identifica a seção de **Comercialização** no site da Embrapa.

- **ano** (`int`, obrigatório):  
Ano da consulta. Aceita valores entre `1970` e `2024`.  
Se não informado, o sistema tentará trazer o dado mais recente disponível.

### Exemplo de requisição:

```json
{
"opcao": "opt_04",
"ano": 2024
}
```
"""

importacao_description = """
    Consulta os dados de importação de uvas no estado do Rio Grande do Sul, conforme publicado pela Embrapa Uva e Vinho.

    Este endpoint realiza scraping direto no site oficial da Embrapa ou retorna os dados previamente armazenados no banco local (cache).

    ### Parâmetros esperados no corpo da requisição (JSON):

    - **opcao** (`str`, obrigatório):  
    Valor fixo `"opt_05"`, correspondente à seção de **Importação** da Embrapa.

    - **ano** (`int`, obrigatório):  
    Ano de referência da consulta. Deve estar entre `1970` e `2024`.

    - **subopcao** (`str`, opcional):  
    Tipo de uva processada. Os valores aceitos são:
    - `"subopt_01"` → Vinhos de mesa
    - `"subopt_02"` → Espumantes
    - `"subopt_03"` → Uvas frescas
    - `"subopt_04"` → Uvas passas
    - `"subopt_05"` → Suco de uva

    Se não informado, será utilizado `"subopt_01"` como padrão.

    ### Exemplo de requisição:

    ```json
    {
    "opcao": "opt_05",
    "ano": 2024,
    "subopcao": "subopt_01"
    }
    ```
    Se os dados estiverem disponíveis no banco local, serão retornados imediatamente.
    Caso contrário, será realizado o scraping em tempo real e o resultado será armazenado para uso futuro.
    """


exportacao_description = """
    Consulta os dados de exportação de uvas no estado do Rio Grande do Sul, conforme publicado pela Embrapa Uva e Vinho.

    Este endpoint realiza scraping direto no site oficial da Embrapa ou retorna os dados previamente armazenados no banco local (cache).

    ### Parâmetros esperados no corpo da requisição (JSON):

    - **opcao** (`str`, obrigatório):  
    Valor fixo `"opt_06"`, correspondente à seção de **Exportação** da Embrapa.

    - **ano** (`int`, obrigatório):  
    Ano de referência da consulta. Deve estar entre `1970` e `2024`.

    - **subopcao** (`str`, opcional):  
    Tipo de uva processada. Os valores aceitos são:
    - `"subopt_01"` → Vinhos de mesa
    - `"subopt_02"` → Espumantes
    - `"subopt_03"` → Uvas frescas
    - `"subopt_04"` → Suco de uva

    Se não informado, será utilizado `"subopt_01"` como padrão.

    ### Exemplo de requisição:

    ```json
    {
    "opcao": "opt_06",
    "ano": 2024,
    "subopcao": "subopt_01"
    }
    ```
    Se os dados estiverem disponíveis no banco local, serão retornados imediatamente.
    Caso contrário, será realizado o scraping em tempo real e o resultado será armazenado para uso futuro.
    """