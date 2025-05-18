class EmbrapaDataNotFoundException(Exception):
    def __init__(self, message="Nenhuma tabela encontrada para os parâmetros informados."):
        self.message = message
        super().__init__(self.message)

class ExternalServiceUnavailableException(Exception):
    def __init__(self, message="Serviço externo (Embrapa) está indisponível no momento."):
        self.message = message
        super().__init__(self.message)