import requests
from bs4 import BeautifulSoup
from typing import Any, Optional, List, Dict
from functools import lru_cache
from app.core.exceptions import EmbrapaDataNotFoundException

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"

def build_embrapa_url(opcao: str, ano: Optional[int] = None, subopcao: Optional[str] = None) -> str:
    params = f"?opcao={opcao}"
    if ano:
        params += f"&ano={ano}"
    if subopcao:
        params += f"&subopcao={subopcao}"
    return BASE_URL + params

def fetch_page_content(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        raise RuntimeError(f"Erro ao acessar {url}: {str(e)}") from e

def parse_table(html_content: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        raise ValueError("Tabela de dados não encontrada na página.")

    grouped_data = []
    current_category = None
    tbody = table.find("tbody")

    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) != 2:
            continue

        produto_cell, quantidade_cell = cells
        produto_text = produto_cell.text.strip()
        quantidade_text = quantidade_cell.text.strip()

        if 'tb_item' in produto_cell.get('class', []):
            current_category = {
                "categoria": produto_text,
                "produtos": []
            }
            grouped_data.append(current_category)
        elif 'tb_subitem' in produto_cell.get('class', []) and current_category:
            current_category["produtos"].append({
                "produto": produto_text,
                "quantidade_litros": quantidade_text
            })

    tfoot = table.find("tfoot", class_="tb_total")
    total_geral = None
    if tfoot:
        total_row = tfoot.find("tr")
        if total_row:
            total_cells = total_row.find_all("td")
            if len(total_cells) == 2:
                total_geral = total_cells[1].text.strip()

    return {
        "categorias": grouped_data,
        "total_litros": total_geral
    }

def parse_import_export_table(html_content: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        raise ValueError("Tabela de dados não encontrada na página.")

    data = []
    tbody = table.find("tbody")

    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 3:
            pais = cells[0].text.strip()
            quantidade = cells[1].text.strip()
            valor = cells[2].text.strip()

            data.append({
                "pais": pais,
                "quantidade_kg": quantidade,
                "valor_usd": valor
            })

    # Total
    tfoot = table.find("tfoot", class_="tb_total")
    total_kg = total_usd = None
    if tfoot:
        total_row = tfoot.find("tr")
        if total_row:
            total_cells = total_row.find_all("td")
            if len(total_cells) == 3:
                total_kg = total_cells[1].text.strip()
                total_usd = total_cells[2].text.strip()

    return {
        "itens": data,
        "total_kg": total_kg,
        "total_usd": total_usd
    }

@lru_cache(maxsize=1000)
def scrape_embrapa(opcao: str, ano: Optional[int] = None, subopcao: Optional[str] = None) -> Dict:
    url = build_embrapa_url(opcao=opcao, ano=ano, subopcao=subopcao)
    html_content = fetch_page_content(url)
    
    if opcao in ["opt_05", "opt_06"]:
        parsed_data = parse_import_export_table(html_content)
    else:
        parsed_data = parse_table(html_content)
    
    if not parsed_data.get("categorias") and not parsed_data.get("itens"):
        raise EmbrapaDataNotFoundException()

    return {
        "source_url": url,
        "records_count": len(parsed_data.get("categorias", parsed_data.get("itens", []))),
        "data": parsed_data
    }
