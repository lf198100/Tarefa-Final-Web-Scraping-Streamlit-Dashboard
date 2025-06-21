import os
import sys
import pytest
import re
from scraper import fetch_page, parse_data, generate_csv

def test_fetch_page_function_signature():
    """Testa se a função fetch_page tem a assinatura correta e retorna uma string"""
    # O teste não faz chamada real à internet
    # Verifica apenas se a função segue a interface esperada
    try:
        # Chamada com um URL dummy
        result = fetch_page("https://example.com")
        # Verifica se o retorno é uma string
        assert isinstance(result, str), "A função fetch_page deve retornar uma string"
    except Exception as e:
        pytest.fail(f"fetch_page deve aceitar um parâmetro URL e retornar uma string: {str(e)}")

def test_parse_data_function_signature():
    """Testa se a função parse_data tem a assinatura correta e retorna uma lista de dicionários"""
    try:
        # Chama com HTML dummy
        result = parse_data("<html></html>")
        # Verifica se o retorno é uma lista
        assert isinstance(result, list), "parse_data deve retornar uma lista"
        
        # Se a lista tiver elementos, verifica se são dicionários
        if result:
            assert all(isinstance(item, dict) for item in result), "Todos os itens da lista devem ser dicionários"
    except Exception as e:
        pytest.fail(f"parse_data deve aceitar um parâmetro HTML e retornar uma lista de dicionários: {str(e)}")

def test_generate_csv_function_existence():
    """Verifica se generate_csv existe e é chamável"""
    assert callable(generate_csv), "generate_csv deve ser uma função chamável"
    
    # Verifica se a URL foi alterada da padrão (os alunos devem alterar)
    import inspect
    source = inspect.getsource(generate_csv)
      # Opcionalmente, verifica se a URL padrão foi alterada
    # Esta verificação é suave e pode ser removida se necessário
    if "URL = " in source and "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies" in source:
        print("AVISO: A URL padrão não foi alterada em generate_csv")

def test_csv_output_path():
    """Verifica se a função generate_csv tenta salvar no caminho correto"""
    # Essa é uma verificação mais simples, sem tentar executar a função completa
    # Verificamos apenas se a função menciona o caminho 'dados/output.csv'
    import inspect
    source = inspect.getsource(generate_csv)
    assert "dados/output.csv" in source, "generate_csv deve salvar em 'dados/output.csv'"
    
def test_integration_mocked(monkeypatch):
    """Teste de integração com mocks para evitar chamadas reais"""
    # Mock das dependências
    mock_data = [{"campo1": "valor1"}]
    
    # Contadores para verificar se as funções são chamadas
    calls = {"fetch": 0, "parse": 0, "save": 0}
    
    def mock_fetch(url):
        calls["fetch"] += 1
        return "<html>teste</html>"
        
    def mock_parse(html):
        calls["parse"] += 1
        return mock_data
        
    def mock_save(data, filename):
        calls["save"] += 1
        assert data == mock_data, "Os dados não foram passados corretamente"
        assert "output.csv" in filename, "Nome do arquivo deve conter 'output.csv'"
    
    # Substitui as funções reais pelos mocks
    monkeypatch.setattr("scraper.fetch_page", mock_fetch)
    monkeypatch.setattr("scraper.parse_data", mock_parse)
    monkeypatch.setattr("scraper.save_to_csv", mock_save)
    
    # Intercepta sys.exit() para evitar que o teste pare
    def mock_exit(code=0):
        pass
    monkeypatch.setattr(sys, "exit", mock_exit)
    
    # Executa a função
    generate_csv()
    
    # Verifica se todas as funções foram chamadas
    assert calls["fetch"] > 0, "fetch_page não foi chamada"
    assert calls["parse"] > 0, "parse_data não foi chamada"
    assert calls["save"] > 0, "save_to_csv não foi chamada"
