from pydantic import BaseModel, Field
from typing import Optional, List,Literal

# PRODUCAO
class EmbrapaScrapingRequestProducao(BaseModel):
    opcao: Literal["opt_02"] = Field(
        description="Opção fixa para Produção de vinhos, sucos e derivados do Rio Grande do Sul."
    )
    ano: Optional[int] = Field(
        default=None,
        ge=1970,
        le=2024,
        description="Ano desejado (entre 1970 e 2024). Se não informado, traz o mais atual disponível."
    )
   

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "opcao": "opt_02",
                    "ano": 2024,
                    "subopcao": None
                },
                {
                    "opcao": "opt_02",
                    "ano": None,
                    "subopcao": None
                }
            ]
        }
    }


# PROCESSAMENTO
class EmbrapaScrapingRequestProcessamento(BaseModel):
    opcao: Literal["opt_03"] = Field(
        description="Opção fixa para Processamento de uvas viníferas, americanas e híbridas."
    )
    ano:int = Field(
        default=None,
        ge=1970,
        le=2024,
        description="Ano desejado (entre 1970 e 2024)."
    )
    subopcao: Optional[Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04"]] = Field(
        default="subopt_01",
        description="Subopção específica (Viníferas, Americanas e Híbridas, Uvas de Mesa, Sem classificação)."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "opcao": "opt_03",
                    "ano": 2024,
                    "subopcao": "subopt_01"
                }
            ]
        }
    }


# COMERCIALIZAÇÃO
class EmbrapaScrapingRequestComercializacao(BaseModel):
    opcao: Literal["opt_04"] = Field(
        description="Opção fixa para Comercialização de vinhos e derivados."
    )
    ano: Optional[int] = Field(
        default=None, ge=1970, le=2024,
        description="Ano desejado (entre 1970 e 2024). Se não informado, traz o mais atual."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "opcao": "opt_04", 
                    "ano": 2024,
                    "subopcao": None
                }
            ]
        }
    }

# IMPORTAÇÃO
class EmbrapaScrapingRequestImportacao(BaseModel):
    opcao: Literal["opt_05"] = Field(description="Opção fixa para Importação.")
    ano: int = Field(ge=1970, le=2024)
    subopcao: Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04", "subopt_05"]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "opcao": "opt_05", 
                    "ano": 2024,
                    "subopcao": "subopt_01"
                }
            ]
        }
    }

# EXPORTAÇÃO
class EmbrapaScrapingRequestExportacao(BaseModel):
    opcao: Literal["opt_06"] = Field(description="Opção fixa para Exportação.")
    ano: int = Field(ge=1970, le=2024)
    subopcao: Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04"]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "opcao": "opt_06", 
                    "ano": 2024,
                    "subopcao": "subopt_01"
                }
            ]
        }
    }
    
# ========== Modelos de Saída (Response) ==========
class ProdutoItem(BaseModel):
    produto: str
    quantidade_litros: str

class CategoriaItem(BaseModel):
    categoria: str
    produtos: List[ProdutoItem]

class EmbrapaScrapingResponseData(BaseModel):
    categorias: List[CategoriaItem]
    total_litros: Optional[str]

class EmbrapaScrapingResponse(BaseModel):
    source_url: str
    records_count: int
    data: EmbrapaScrapingResponseData
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "source_url": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano=2024",
                    "records_count": 3,
                    "data": {
                        "categorias": [
                            {
                                "categoria": "VINHO DE MESA",
                                "produtos": [
                                    {
                                        "produto": "Tinto",
                                        "quantidade_litros": "139.320.884"
                                    },
                                    {
                                        "produto": "Branco",
                                        "quantidade_litros": "27.910.299"
                                    }
                                ]
                            }
                        ],
                        "total_litros": "457.792.870"
                    }
                }
            ]
        }
    }
