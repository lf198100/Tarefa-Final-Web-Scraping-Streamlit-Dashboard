import streamlit as st 
import pandas as pd

# Define o título que aparece no topo do painel
st.title("Dashboard Final: Lista de países por População")

# Carrega o arquivo CSV com os dados da população
# Se o CSV usar outro separador, é só mudar o parâmetro sep
df = pd.read_csv("dados/output.csv", sep=",")

# Renomeia a coluna "Estimativa da ONU" para "População" para facilitar o uso
df.rename(columns={'Estimativa da ONU': 'População'}, inplace=True)

# Mostra o título para a tabela dos dados originais
st.subheader("📊 Dados Originais")
# Exibe os dados carregados em uma tabela interativa
st.dataframe(df)

# Limpa os dados para garantir que números estejam no formato correto
# Remove pontos, vírgulas, espaços e tenta transformar em números
for col in df.columns:
    df[col] = df[col].astype(str)\
                     .str.replace(".", "", regex=False)\
                     .str.replace(",", "", regex=False)\
                     .str.replace(" ", "", regex=False)
    df[col] = pd.to_numeric(df[col], errors='ignore')

# Cria um cabeçalho na barra lateral para os filtros
st.sidebar.header("Filtros")

# Filtro 1: Caixa de texto para buscar país pelo nome (ou parte do nome)
filtro_texto = st.sidebar.text_input("Buscar país (parte do nome):")

# Filtro 2: Caixa para selecionar somente países com população maior que 100 milhões
filtro_pop_100mi = st.sidebar.checkbox("Mostrar só países com população > 100 milhões")

# Filtro 3: Controle deslizante para escolher um intervalo mínimo e máximo de população
min_pop = int(df['População'].min())
max_pop = int(df['População'].max())
filtro_pop_slider = st.sidebar.slider(
    "Intervalo de população:",
    min_value=min_pop,
    max_value=max_pop,
    value=(min_pop, max_pop)
)

# Aplica os filtros na cópia dos dados
df_filtrado = df.copy()

# Se o filtro de texto tiver algo escrito, filtra pelos países que contém o texto (sem diferenciar maiúsculas/minúsculas)
if filtro_texto:
    df_filtrado = df_filtrado[df_filtrado['País (ou território dependente)'].str.contains(filtro_texto, case=False, na=False)]

# Se o filtro do checkbox estiver marcado, mostra só países com população maior que 100 milhões
if filtro_pop_100mi:
    df_filtrado = df_filtrado[df_filtrado['População'] > 100_000_000]

# Aplica filtro pelo intervalo de população selecionado no slider
df_filtrado = df_filtrado[
    (df_filtrado['População'] >= filtro_pop_slider[0]) &
    (df_filtrado['População'] <= filtro_pop_slider[1])
]

# Mostra quantos países foram filtrados e a tabela com esses dados filtrados
st.subheader(f"📊 Dados Filtrados ({len(df_filtrado)} países)")
st.dataframe(df_filtrado)

# Exibe algumas estatísticas básicas sobre os países filtrados
st.subheader("📈 Estatísticas")
col1, col2, col3 = st.columns(3)  # Divide a área em 3 colunas

with col1:
    st.metric("Total de Países", len(df_filtrado))  # Quantidade total de países no filtro

with col2:
    # Soma total da população dos países filtrados
    if 'População' in df_filtrado.columns:
        st.metric("População Total", f"{df_filtrado['População'].sum():,.0f}".replace(",", "."))

with col3:
    # Média da população entre os países filtrados
    if 'População' in df_filtrado.columns:
        st.metric("População Média", f"{df_filtrado['População'].mean():,.0f}".replace(",", "."))

# Gráfico dos 10 países mais populosos entre os filtrados
if 'População' in df_filtrado.columns and 'País (ou território dependente)' in df_filtrado.columns:
    df_top = df_filtrado.sort_values(by="População", ascending=False).head(10)
    st.subheader("🔝 Top 10 Países por População (Filtrado)")
    st.bar_chart(df_top.set_index("País (ou território dependente)")["População"])
else:
    st.write("Nenhum país encontrado com os filtros aplicados.")

# Gráfico dos 5 países menos populosos entre os filtrados
if 'População' in df_filtrado.columns and 'País (ou território dependente)' in df_filtrado.columns:
    df_menores = df_filtrado.sort_values(by="População", ascending=True).head(5)
    st.subheader("🔽 5 Países Menos Populosos (Filtrado)")
    st.bar_chart(df_menores.set_index("País (ou território dependente)")["População"])
