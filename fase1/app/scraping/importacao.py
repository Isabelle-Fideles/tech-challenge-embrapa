from pydantic import BaseModel
from typing import List, Optional


class ImportacaoItem(BaseModel):
    pais: str
    quantidade_kg: Optional[str]
    valor_usd: Optional[str]


class EmbrapaImportacaoResponseData(BaseModel):
    itens: List[ImportacaoItem]
    total_kg: Optional[str]
    total_usd: Optional[str]


class EmbrapaImportacaoResponse(BaseModel):
    source_url: str
    records_count: int
    data: EmbrapaImportacaoResponseData
