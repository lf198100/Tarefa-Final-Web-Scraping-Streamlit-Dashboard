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
    Monta um dicionário de headers para simular o requests feito pelo browser
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    return headers

def fetch_page(url):
    """
    Faz GET em `url` e retorna HTML como string.
    """
    headers = generate_user_agent()
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao buscar a página: {e}")
        sys.exit(1)

def parse_data(html):
    """
    Recebe HTML e retorna uma lista de dicionários dos dados capturados.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "wikitable"})

    lista = []
    if not table:
        print("Tabela não encontrada.")
        return lista

    headers = [th.text.strip() for th in table.find("tr").find_all("th")]

    # Remove as duas primeiras colunas dos headers também
    headers = headers[2:]

    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td", "th"])
        if len(cols) < len(headers) + 2:
            continue
        # Ignora as duas primeiras células da linha
        cols = cols[2:]
        if len(cols) != len(headers):
            # Linha com número de colunas diferente, ignora
            continue
        item = {headers[i]: cols[i].text.strip() for i in range(len(headers))}
        lista.append(item)
    return lista


def save_to_csv(data, filename):
    """
    Salva list[dict] em CSV em `filename`. Sai se data==[].
    """
    if not data:
        print("Nenhum registro para salvar.")
        sys.exit(1)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

def generate_csv():
    """
    Helper CLI: baixa a página, parseia e salva 'dados/output.csv'.
    """
    # Altere com a url do seu projeto"
    URL = "https://pt.wikipedia.org/wiki/Lista_de_pa%C3%ADses_por_popula%C3%A7%C3%A3o"
    html = fetch_page(URL)
    data = parse_data(html)
    save_to_csv(data, "dados/output.csv")

if __name__ == "__main__":
    generate_csv()
    
