import os
from dotenv import load_dotenv
import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


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
with open(os.path.join(os.path.dirname(__file__), "query.graphql"), "r", encoding="utf-8") as f:
    QUERY = f.read()

# Executar a query
def fetch_repos():
    try:
        result = client.execute(gql(QUERY))
        return result
    except Exception as e:
        print("Erro ao executar a query:", e)
        return None

# Salvar em CSV
def save_to_csv(data):
    rows = []
    for edge in data["search"]["edges"]:
        repo = edge["node"]
        rows.append({
            "name": repo["name"],
            "owner": repo["owner"]["login"],
            "stars": repo["stargazerCount"],
            "createdAt": repo["createdAt"],
            "updatedAt": repo["pushedAt"],
            "primaryLanguage": repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else None,
            "pullRequests": repo["pullRequests"]["totalCount"],
            "releases": repo["releases"]["totalCount"],
            "issues": repo["issues"]["totalCount"],
            "closedIssues": repo["closed"]["totalCount"],
        })
    df = pd.DataFrame(rows)
    df.to_csv("repositories.csv", index=False)
    print(f"Arquivo repos.csv salvo com {len(rows)} registros.")

if __name__ == "__main__":
    data = fetch_repos()
    if data:
        save_to_csv(data)
