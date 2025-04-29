from pydantic import BaseModel, Field
from typing import Optional, List,Literal

# ========== Modelo de Entrada (Request) Producao ==========
class EmbrapaScrapingRequestProducao(BaseModel):
    opcao: Literal["opt_02"] = Field(
        description="Opção fixa para Produção de vinhos, sucos e derivados do Rio Grande do Sul."
    )
    ano: Optional[int] = Field(
        default=None,
        ge=1976,
        le=2023,
        description="Ano desejado (entre 1976 e 2023). Se não informado, traz o mais atual disponível."
    )
    # subopcao: Optional[str] = Field(
    #     default=None,
    #     description="Subopção específica (opcional). Normalmente não utilizada para Produção."
    # )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "opcao": "opt_02",
                    "ano": 2023,
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


# ========== Modelo de Entrada (Request) Processamento ==========
class EmbrapaScrapingRequestProcessamento(BaseModel):
    opcao: Literal["opt_03"] = Field(
        description="Opção fixa para Processamento de uvas viníferas, americanas e híbridas."
    )
    ano: Optional[int] = Field(
        default=None,
        ge=1976,
        le=2023,
        description="Ano desejado (entre 1976 e 2023)."
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
                    "ano": 2023,
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
                    "source_url": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano=2023",
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
