# 📰 Notícias UFRN - Keyword EAJ

Trabalho prático para coleta de notícias do portal da UFRN filtradas pela palavra-chave **EAJ** e visualização em gráfico usando **Streamlit**.

---

## 📁 Estrutura de Pastas

```text
noticeuf/
├── data/
│   └── noticias_eaj.txt      # Arquivo salvo com: ANO | URL
├── scraper.py                 # Script de raspagem de dados
├── app.py                     # Aplicação Streamlit com o gráfico (st.bar_chart)
├── requirements.txt           # Lista de dependências
├── .gitignore
└── README.md
```

---

## 🚀 Como Executar

### 1. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 2. Rodar a raspagem (gera o arquivo `data/noticias_eaj.txt`)
```bash
python scraper.py
```

### 3. Visualizar o gráfico no Streamlit
```bash
python -m streamlit run app.py
```
Acesse `http://localhost:8501` no seu navegador.

---

## ☁️ Como Rodar no Google Colab

Caso deseje rodar a raspagem e ver o gráfico no **Google Colab**, basta colar o seguinte código em uma célula do Colab:

```python
import json, urllib.request, os
import pandas as pd
import matplotlib.pyplot as plt

# 1. Coleta das Notícias
url_base = "https://webcache01-producao.info.ufrn.br/admin/portal-ufrn/wp-json/wp/v2/noticias-busca/?tags=EAJ&per_page=100&page="
noticias, pagina = [], 1

while True:
    try:
        req = urllib.request.Request(f"{url_base}{pagina}", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
            if not dados or not isinstance(dados, list): break
            for item in dados:
                ano = item.get("date", "")[:4] or "N/A"
                news_id, slug = item.get("id"), item.get("slug")
                url = f"https://www.ufrn.br/imprensa/noticias/{news_id}/{slug}" if news_id and slug else item.get("link", "")
                if url: noticias.append((ano, url))
            pagina += 1
    except Exception: break

# 2. Salvar no arquivo noticias_eaj.txt
os.makedirs("data", exist_ok=True)
with open("data/noticias_eaj.txt", "w", encoding="utf-8") as f:
    for ano, url in noticias:
        f.write(f"{ano} | {url}\n")

print(f"Total de noticias salvas: {len(noticias)}")

# 3. Gráfico de Barras
df = pd.read_csv("data/noticias_eaj.txt", sep="|", names=["Ano", "URL"], engine="python")
df["Ano"] = df["Ano"].str.strip()
contagem = df.groupby("Ano").size()

contagem.plot(kind="bar", color="#2563EB")
plt.title("Quantidade de Notícias por Ano (EAJ)")
plt.xlabel("Ano")
plt.ylabel("Notícias")
plt.show()
```
