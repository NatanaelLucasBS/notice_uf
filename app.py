import os
import pandas as pd
import streamlit as st
from scraper import coletar_noticias

# Título da Aplicação
st.title("📊 Notícias UFRN (Keyword: EAJ)")
st.write("Gráfico demonstrando a quantidade de notícias publicadas sobre a EAJ por ano.")

# Garante que o arquivo de dados exista
filepath = "data/noticias_eaj.txt"
if not os.path.exists(filepath):
    st.info("Coletando dados da UFRN pela primeira vez...")
    coletar_noticias()

# Leitura simples do arquivo .txt
df = pd.read_csv(filepath, sep="|", names=["Ano", "URL"], engine="python")
df["Ano"] = df["Ano"].astype(str).str.strip()
df["URL"] = df["URL"].str.strip()

# Agrupa as notícias por ano
contagem = df.groupby("Ano").size().reset_index(name="Quantidade de Notícias")

# Requisito 2: Gráfico no Streamlit usando st.bar_chart
st.subheader("Quantidade de Notícias por Ano")
st.bar_chart(contagem.set_index("Ano"))

# Tabela com as URLs coletadas
st.subheader("Links das Notícias Coletadas")
st.dataframe(df, use_container_width=True)
