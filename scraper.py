import json
import urllib.request
import os

def coletar_noticias():
    """Coleta as notícias da UFRN com a keyword EAJ e salva no arquivo data/noticias_eaj.txt."""
    url_base = "https://webcache01-producao.info.ufrn.br/admin/portal-ufrn/wp-json/wp/v2/noticias-busca/?tags=EAJ&per_page=100&page="
    noticias = []
    pagina = 1

    print("Iniciando coleta de notícias da UFRN...")

    while True:
        try:
            req = urllib.request.Request(f"{url_base}{pagina}", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                dados = json.loads(resp.read().decode("utf-8"))
                if not dados or not isinstance(dados, list):
                    break
                
                for item in dados:
                    ano = item.get("date", "")[:4] or "N/A"
                    news_id = item.get("id")
                    slug = item.get("slug")
                    url = f"https://www.ufrn.br/imprensa/noticias/{news_id}/{slug}" if news_id and slug else item.get("link", "")
                    
                    if url:
                        noticias.append((ano, url))
                
                print(f"Página {pagina}: {len(dados)} notícias encontradas.")
                pagina += 1
        except Exception:
            break

    # Salva os dados no arquivo .txt
    os.makedirs("data", exist_ok=True)
    filepath = "data/noticias_eaj.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        for ano, url in noticias:
            f.write(f"{ano} | {url}\n")
            
    print(f"Concluído! Total: {len(noticias)} notícias salvas em {filepath}")

if __name__ == "__main__":
    coletar_noticias()
