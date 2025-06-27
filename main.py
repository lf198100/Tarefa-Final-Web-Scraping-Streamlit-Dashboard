import streamlit as st
import pandas as pd

# Altere com o título do seu projeto na parte indicada
st.title("Dashboard Final: Lista de países por População")

# Carrega CSV (assume que já foi gerado via `python scraper.py`)
# Se o seu CSV usar outro separador, ponto e vírgula, por exemplo
# basta alterar o parâmetro sep
df = pd.read_csv("dados/output.csv", sep=",")

# Renomeia a coluna para facilitar o uso no código
df.rename(columns={'Estimativa da ONU': 'População'}, inplace=True)

# Continue a partir daqui com a implementação do seu Dashboard

# Exibe dados brutos
st.subheader("📊 Dados Originais")
st.dataframe(df)

# Limpeza: remove pontos, vírgulas, espaços e converte colunas para número se possível
for col in df.columns:
    df[col] = df[col].astype(str)\
                     .str.replace(".", "", regex=False)\
                     .str.replace(",", "", regex=False)\
                     .str.replace(" ", "", regex=False)
    df[col] = pd.to_numeric(df[col], errors='ignore')


# FILTROS NA SIDEBAR 

st.sidebar.header("Filtros")

# 1. text_input para buscar país por nome parcial
filtro_texto = st.sidebar.text_input("Buscar país (parte do nome):")

# 2. checkbox para filtrar só países com população > 100 milhões
filtro_pop_100mi = st.sidebar.checkbox("Mostrar só países com população > 100 milhões")

# 3. slider para filtrar intervalo de população
min_pop = int(df['População'].min())
max_pop = int(df['População'].max())
filtro_pop_slider = st.sidebar.slider(
    "Intervalo de população:",
    min_value=min_pop,
    max_value=max_pop,
    value=(min_pop, max_pop)
)

# Aplicar filtros
df_filtrado = df.copy()

if filtro_texto:
    df_filtrado = df_filtrado[df_filtrado['País (ou território dependente)'].str.contains(filtro_texto, case=False, na=False)]

if filtro_pop_100mi:
    df_filtrado = df_filtrado[df_filtrado['População'] > 100_000_000]

df_filtrado = df_filtrado[
    (df_filtrado['População'] >= filtro_pop_slider[0]) &
    (df_filtrado['População'] <= filtro_pop_slider[1])
]

# Exibe dados filtrados
st.subheader(f"📊 Dados Filtrados ({len(df_filtrado)} países)")
st.dataframe(df_filtrado)

# Estatísticas
st.subheader("📈 Estatísticas")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Países", len(df_filtrado))
with col2:
    if 'População' in df_filtrado.columns:
        st.metric("População Total", f"{df_filtrado['População'].sum():,.0f}".replace(",", "."))
with col3:
    if 'População' in df_filtrado.columns:
        st.metric("População Média", f"{df_filtrado['População'].mean():,.0f}".replace(",", "."))

# Gráfico de barras com os 10 mais populosos do filtro
if 'População' in df_filtrado.columns and 'País (ou território dependente)' in df_filtrado.columns:
    df_top = df_filtrado.sort_values(by="População", ascending=False).head(10)
    st.subheader("🔝 Top 10 Países por População (Filtrado)")
    st.bar_chart(df_top.set_index("País (ou território dependente)")["População"])
else:
    st.write("Nenhum país encontrado com os filtros aplicados.")
if 'População' in df_filtrado.columns and 'País (ou território dependente)' in df_filtrado.columns:
    df_menores = df_filtrado.sort_values(by="População", ascending=True).head(5)
    st.subheader("🔽 5 Países Menos Populosos (Filtrado)")
    st.bar_chart(df_menores.set_index("País (ou território dependente)")["População"])
    # Gráfico de barras com os 5 menos populosos

