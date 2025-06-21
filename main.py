import streamlit as st
import pandas as pd

# Altere com o título do seu projeto na parte indicada
st.title("Dashboard Final: <Título do seu Projeto>")

# Carrega CSV (assume que já foi gerado via `python scraper.py`)
# Se o seu CSV usar outro separador, ponto e vírgula, por exemplo
# basta alterar o parâmetro sep
df = pd.read_csv("dados/output.csv", sep=",")

# Continue a partir daqui com a implementação do seu Dashboard