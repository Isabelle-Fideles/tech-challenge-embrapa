from fastapi import HTTPException

class EmbrapaDataNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail={
                "error_code": "DATA_NOT_FOUND",
                "error_message": "Nenhuma tabela encontrada para o ano e opção informados."
            }
        )
