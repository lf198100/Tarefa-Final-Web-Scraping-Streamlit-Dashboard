import os
import sys
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

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
        
    return ""

def parse_data(html):
    """
    Recebe HTML e retorna uma lista de dicionarios dos dados capturados
    """
    lista = []

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
    URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = fetch_page(URL)
    data = parse_data(html)
    save_to_csv(data, "dados/output.csv")

if __name__ == "__main__":
    generate_csv()
