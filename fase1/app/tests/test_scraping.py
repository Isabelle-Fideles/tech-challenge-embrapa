import pytest
import requests
from unittest.mock import patch, Mock
from app.scraping.bs4_scraper import (
    build_embrapa_url,
    fetch_page_content,
    parse_table,
    parse_import_export_table,
    scrape_embrapa
)
from app.core.exceptions import (
    ExternalServiceUnavailableException,
    EmbrapaDataNotFoundException
)


# -----------------------------
# Testes da função build_embrapa_url
# -----------------------------

def test_build_embrapa_url_sem_ano_subopcao():
    url = build_embrapa_url(opcao="opt_02")
    assert url == "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"


def test_build_embrapa_url_completo():
    url = build_embrapa_url(opcao="opt_05", ano=2022, subopcao="subopt_01")
    assert url == "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05&ano=2022&subopcao=subopt_01"


# -----------------------------
# Teste da função fetch_page_content
# -----------------------------

@patch("app.scraping.bs4_scraper.requests.get")
def test_fetch_page_content_sucesso(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"<html>OK</html>"
    mock_get.return_value = mock_response

    url = "http://fakeurl"
    result = fetch_page_content(url)

    assert result == b"<html>OK</html>"
    mock_get.assert_called_once_with(url, timeout=10)


# Teste com múltiplas exceções possíveis de requests
@pytest.mark.parametrize("error", [
    requests.exceptions.RequestException,
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
    requests.exceptions.HTTPError
])
@patch("app.scraping.bs4_scraper.requests.get")
def test_fetch_page_content_falha(mock_get, error):
    mock_get.side_effect = error("Erro simulado")

    with pytest.raises(ExternalServiceUnavailableException):
        fetch_page_content("http://fakeurl")


# -----------------------------
# Testes da função parse_table
# -----------------------------

def test_parse_table_ok():
    with open("app/scraping/mok/opt_02.html", encoding="utf-8") as file:
        html = file.read()

    result = parse_table(html)

    assert "categorias" in result
    assert isinstance(result["categorias"], list)
    assert "total_litros" in result


def test_parse_table_sem_tabela():
    with pytest.raises(ValueError):
        parse_table("<html><body>Sem tabela</body></html>")


# -----------------------------
# Testes da função parse_import_export_table
# -----------------------------

def test_parse_import_export_table_ok():
    with open("app/scraping/mok/opt_05.html", encoding="utf-8") as file:
        html = file.read()

    result = parse_import_export_table(html)

    assert "itens" in result
    assert isinstance(result["itens"], list)
    assert "total_kg" in result
    assert "total_usd" in result


def test_parse_import_export_table_sem_tabela():
    with pytest.raises(ValueError):
        parse_import_export_table("<html><body>Sem tabela</body></html>")


# -----------------------------
# Testes da função scrape_embrapa
# -----------------------------

@patch("app.scraping.bs4_scraper.fetch_page_content")
def test_scrape_embrapa_producao_ok(mock_fetch):
    with open("app/scraping/mok/opt_02.html", encoding="utf-8") as file:
        html = file.read()

    mock_fetch.return_value = html

    result = scrape_embrapa(opcao="opt_02", ano=2022)

    assert "source_url" in result
    assert result["records_count"] > 0
    assert "data" in result
    assert "categorias" in result["data"]


@patch("app.scraping.bs4_scraper.fetch_page_content")
def test_scrape_embrapa_importacao_ok(mock_fetch):
    with open("app/scraping/mok/opt_05.html", encoding="utf-8") as file:
        html = file.read()

    mock_fetch.return_value = html

    result = scrape_embrapa(opcao="opt_05", ano=2022, subopcao="subopt_01")

    assert "source_url" in result
    assert result["records_count"] > 0
    assert "data" in result
    assert "itens" in result["data"]


@patch("app.scraping.bs4_scraper.fetch_page_content")
def test_scrape_embrapa_dados_nao_encontrados(mock_fetch):
    html = """
    <html>
    <body>
        <table class="tb_base tb_dados">
            <tbody></tbody>
        </table>
    </body>
    </html>
    """
    mock_fetch.return_value = html

    with pytest.raises(EmbrapaDataNotFoundException):
        scrape_embrapa(opcao="opt_02")


# -----------------------------
# Teste extra: parsing simples inline (sanidade)
# -----------------------------

def test_parse_import_export_table_dados_corretos():
    html = """
    <table class="tb_base tb_dados">
      <tbody>
        <tr><td>Brasil</td><td>1.000</td><td>2.000</td></tr>
      </tbody>
      <tfoot class="tb_total">
        <tr><td>Total</td><td>1.000</td><td>2.000</td></tr>
      </tfoot>
    </table>
    """
    result = parse_import_export_table(html)
    assert result["itens"][0]["pais"] == "Brasil"
    assert result["itens"][0]["quantidade_kg"] == "1000"
    assert result["itens"][0]["valor_usd"] == "2000"
    assert result["total_kg"] == "1000"
    assert result["total_usd"] == "2000"
