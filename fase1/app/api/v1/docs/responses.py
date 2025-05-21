common_responses = {
    500: {
        "description": "Erro interno",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Erro interno inesperado na aplicação."
                }
            }
        }
    },
    503: {
        "description": "Serviço da Embrapa fora do ar.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Serviço externo (Embrapa) está indisponível no momento."
                }
            }
        }
    },
    404: {
        "description": "Nenhuma tabela encontrada com os parâmetros informados.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Nenhuma tabela encontrada para os parâmetros informados."
                }
            }
        }
    }
}

