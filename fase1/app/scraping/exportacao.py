from pydantic import BaseModel
from typing import List, Optional


class ExportacaoItem(BaseModel):
    pais: str
    quantidade_kg: Optional[str]
    valor_usd: Optional[str]


class EmbrapaExportacaoResponseData(BaseModel):
    itens: List[ExportacaoItem]
    total_kg: Optional[str]
    total_usd: Optional[str]


class EmbrapaExportacaoResponse(BaseModel):
    source_url: str
    records_count: int
    data: EmbrapaExportacaoResponseData
