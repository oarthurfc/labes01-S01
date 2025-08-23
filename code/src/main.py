import os
import time
from dotenv import load_dotenv
import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from requests.exceptions import HTTPError, RequestException

# Config
MAX_REPOS = 1000       # total repositórios
PAGE_SIZE = 25        # 25 por chamada
MAX_RETRIES = 4       # tentativas por página
RETRY_BASE = 1.5      # fator para retentativas

# Carregar token do .env
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise SystemExit("Erro: GITHUB_TOKEN não encontrado no .env")

# Configurar transporte GraphQL
transport = RequestsHTTPTransport(
    url="https://api.github.com/graphql",
    headers={"Authorization": f"bearer {GITHUB_TOKEN}"},
    use_json=True,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# Ler a query do arquivo
QUERY_PATH = os.path.join(os.path.dirname(__file__), "query.graphql")
with open(QUERY_PATH, "r", encoding="utf-8") as f:
    QUERY = f.read()

def fetch_page(cursor=None):
    """Busca uma página (25 itens) com retry"""
    variables = {"cursor": cursor}
    attempt = 0
    while True:
        try:
            return client.execute(gql(QUERY), variable_values=variables)
        except (HTTPError, RequestException, Exception) as e:
            attempt += 1
            if attempt > MAX_RETRIES:
                raise
            sleep_s = RETRY_BASE ** attempt
            print(f"Falha na página (tentativa {attempt}/{MAX_RETRIES}): {e}. "
                  f"Repetindo em {sleep_s:.1f}s…")
            time.sleep(sleep_s)

def collect_top_repos():
    """Paginação até juntar MAX_REPOS, tendo os repositórios ordenados por estrelas em ordem decrescente."""
    all_edges = []
    cursor = None
    has_next = True
    page_count = 1

    while has_next and len(all_edges) < MAX_REPOS:
        print(f"Buscando {PAGE_SIZE} repositórios para página {page_count}")
        data = fetch_page(cursor)
        search = data["search"]
        edges = search.get("edges", [])
        all_edges.extend(edges)
        page_info = search.get("pageInfo") or {}
        has_next = page_info.get("hasNextPage", False)
        cursor = page_info.get("endCursor")
        page_count += 1

    return all_edges[:MAX_REPOS]

def _pick_language(repo):
    pl = repo.get("primaryLanguage")
    if pl and pl.get("name"):
        return pl["name"]

    langs = (repo.get("languages") or {}).get("edges") or []
    if langs:
        return langs[0]["node"]["name"]

    return "Unknown"

def save_to_csv(edges):
    rows = []
    for edge in edges:
        repo = edge["node"]
        rows.append({
            "name": repo["name"],
            "owner": repo["owner"]["login"],
            "stars": repo["stargazerCount"],
            "createdAt": repo["createdAt"],
            "updatedAt": repo["pushedAt"],
            "primaryLanguage": _pick_language(repo),
            "pullRequests": repo["pullRequests"]["totalCount"],
            "releases": repo["releases"]["totalCount"],
            "issues": repo["issues"]["totalCount"],
            "closedIssues": repo["closed"]["totalCount"],
        })
    df = pd.DataFrame(rows)
    df.to_csv("repositories.csv", index=False)
    print(f"Arquivo repositories.csv salvo com {len(rows)} registros.")

if __name__ == "__main__":
    try:
        edges = collect_top_repos()
        save_to_csv(edges)
    except Exception as e:
        print("Erro ao coletar repositórios:", e)
