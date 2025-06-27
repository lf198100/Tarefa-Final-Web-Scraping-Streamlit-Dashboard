import os
import sys
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import subprocess
import sys


def generate_user_agent():
    """
    Essa função cria um dicionário com informações que "fingem" ser um navegador web,
    para o site achar que o pedido vem de uma pessoa usando um navegador normal,
    e não de um programa automático.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    return headers

def fetch_page(url):
    """
    Aqui a gente tenta baixar a página da internet usando o endereço que passamos.
    Usa o 'user agent' para se passar por navegador e pega o conteúdo HTML.
    Se der algum erro, mostra a mensagem e para o programa.
    """
    headers = generate_user_agent()
    try:
        response = requests.get(url, headers=headers)  # Pede a página com os cabeçalhos
        response.raise_for_status()  # Verifica se deu tudo certo, senão gera erro
        return response.text  # Retorna o código HTML da página
    except requests.RequestException as e:
        print(f"Erro ao buscar a página: {e}")
        sys.exit(1)  # Sai do programa se falhar

def parse_data(html):
    """
    Recebe o código HTML da página, usa o BeautifulSoup para entender a estrutura,
    procura a tabela com a classe "wikitable" (onde estão os dados que queremos).
    Depois, lê os títulos das colunas e pega as linhas da tabela,
    descartando as duas primeiras colunas que não interessam.
    Cada linha vira um dicionário com título: valor, e tudo vai para uma lista.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "wikitable"})  # Procura a tabela certa

    lista = []
    if not table:
        print("Tabela não encontrada.")
        return lista  # Se não achar tabela, devolve lista vazia

    headers = [th.text.strip() for th in table.find("tr").find_all("th")]  # Pega títulos da tabela

    # Remove as duas primeiras colunas dos títulos, pois não queremos esses dados
    headers = headers[2:]

    # Para cada linha da tabela, começando depois do cabeçalho
    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td", "th"])  # Pega as colunas da linha
        if len(cols) < len(headers) + 2:
            continue  # Pula linhas que não têm colunas suficientes
        # Ignora as duas primeiras colunas da linha, igual aos títulos
        cols = cols[2:]
        if len(cols) != len(headers):
            continue  # Pula linhas que não batem com o número de títulos
        # Monta um dicionário combinando título com conteúdo da célula
        item = {headers[i]: cols[i].text.strip() for i in range(len(headers))}
        lista.append(item)  # Adiciona esse dicionário na lista
    return lista


def save_to_csv(data, filename):
    """
    Recebe a lista de dicionários (os dados) e salva tudo em um arquivo CSV,
    que pode ser aberto em Excel ou outros programas.
    Se a lista estiver vazia, avisa e para o programa.
    """
    if not data:
        print("Nenhum registro para salvar.")
        sys.exit(1)
    # Garante que a pasta onde o arquivo vai ficar existe (se não existir, cria)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))  # Usa os títulos do primeiro item
        writer.writeheader()  # Escreve a primeira linha com os títulos
        writer.writerows(data)  # Escreve as linhas com os dados

def generate_csv():
    """
    Função principal que junta tudo: baixa a página, pega os dados e salva no CSV.
    Você pode mudar a URL para outra página que tenha uma tabela parecida.
    """
    URL = "https://pt.wikipedia.org/wiki/Lista_de_pa%C3%ADses_por_popula%C3%A7%C3%A3o"
    html = fetch_page(URL)  # Baixa a página
    data = parse_data(html)  # Pega só os dados que queremos
    save_to_csv(data, "dados/output.csv")  # Salva num arquivo na pasta "dados"

if __name__ == "__main__":
    generate_csv()  # Quando rodar o script, já faz tudo automaticamente

    
