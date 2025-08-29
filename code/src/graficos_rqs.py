import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

ARQ_CSV = "repositories.csv"
PASTA_SAIDA = "graficos"
sns.set(style="whitegrid")

def salvar_grafico(nome_arquivo):
    """Salva o gráfico atual em PNG na pasta 'graficos'."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    caminho = os.path.join(PASTA_SAIDA, f"{nome_arquivo}.png")
    plt.savefig(caminho)
    plt.close()
    print(f"Gráfico salvo em: {caminho}")

def preparar_df(df):
    """Cria colunas auxiliares usadas nas RQs."""
    df = df.copy()
    # Datas -> datetime
    df["createdAt"] = pd.to_datetime(df["createdAt"], utc=True, errors="coerce")
    df["updatedAt"] = pd.to_datetime(df["updatedAt"], utc=True, errors="coerce")
    now = pd.Timestamp.utcnow()
    # Idade (anos) e tempo desde última atualização (dias)
    df["age_years"] = (now - df["createdAt"]).dt.days / 365
    df["days_since_update"] = (now - df["updatedAt"]).dt.days
    # Linguagem
    df["primaryLanguage"] = df["primaryLanguage"].fillna("Unknown")
    top_langs = df["primaryLanguage"].value_counts().head(8).index.tolist()
    df["lang_top8"] = df["primaryLanguage"].where(df["primaryLanguage"].isin(top_langs), "Unknown")
    # Faixas de estrelas (para barras empilhadas e heatmap)
    star_bins = [0, 1000, 5000, 10000, 25000, 50000, 100000, np.inf]
    star_labels = ["<1k", "1k–5k", "5k–10k", "10k–25k", "25k–50k", "50k–100k", "100k+"]
    df["star_bucket"] = pd.cut(df["stars"], bins=star_bins, labels=star_labels, include_lowest=True)
    # Taxa de fechamento de issues
    df["percent_issues_closed"] = np.where(df["issues"] > 0, df["closedIssues"]/df["issues"], np.nan)
    return df

# =========================
# RQ01 – Maturidade (idade)
# =========================

def rq01(df):
    # Histograma da idade
    plt.figure(figsize=(8, 5))
    sns.histplot(df["age_years"], bins=30)
    plt.title("RQ01 – Distribuição da idade (anos) dos repositórios")
    plt.xlabel("Idade (anos)")
    salvar_grafico("RQ01_hist_idade")

    # Boxplot da idade
    plt.figure(figsize=(6, 4))
    sns.boxplot(y=df["age_years"])
    plt.title("RQ01 – Boxplot da idade")
    plt.ylabel("Idade (anos)")
    salvar_grafico("RQ01_box_idade")

    # Linha: repositórios por ano de criação
    por_ano = df["createdAt"].dt.year.value_counts().sort_index()
    plt.figure(figsize=(9, 4))
    sns.lineplot(x=por_ano.index, y=por_ano.values, marker="o")
    plt.title("RQ01 – Repositórios por ano de criação")
    plt.xlabel("Ano"); plt.ylabel("Qtde repositórios")
    salvar_grafico("RQ01_linha_criacao_por_ano")

# =========================================
# RQ02 – Contribuição externa (pull requests)
# =========================================

def rq02(df):

    # Dispersão: Stars x PRs
    plt.figure(figsize=(7, 5))
    sns.scatterplot(x="stars", y="pullRequests", data=df, alpha=0.6)
    plt.title("RQ02 – Stars vs Pull Requests")
    salvar_grafico("RQ02_disp_stars_vs_prs")

    # Boxplot de PRs por Linguagem (top8)
    df_lang = df[df["lang_top8"] != "Unknown"]
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="lang_top8", y="pullRequests", data=df_lang, showfliers=False)
    plt.title("RQ02 – PRs por linguagem (boxplot)")
    plt.xlabel("Linguagem (top8)"); plt.ylabel("Pull Requests")
    plt.xticks(rotation=30, ha="right")
    salvar_grafico("RQ02_box_prs_por_linguagem")

# =========================
# RQ03 – Releases
# =========================

def rq03(df):
    # Histograma de releases
    plt.figure(figsize=(8, 5))
    sns.histplot(df["releases"], bins=40, kde=False)
    plt.title("RQ03 – Distribuição de Releases")
    plt.xlabel("Releases")
    salvar_grafico("RQ03_hist_releases")

    # Dispersão: Stars x Releases
    plt.figure(figsize=(7, 5))
    sns.scatterplot(x="stars", y="releases", data=df, alpha=0.6)
    plt.title("RQ03 – Stars vs Releases")
    salvar_grafico("RQ03_disp_stars_vs_releases")

    # Boxplot de releases por linguagem
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="lang_top8", y="releases", data=df.query("lang_top8 != 'Unknown'"), showfliers=False)
    plt.title("RQ03 – Releases por linguagem")
    plt.xlabel("Linguagem (top8)")
    plt.ylabel("Releases")
    plt.xticks(rotation=30, ha="right")
    salvar_grafico("RQ03_box_releases_por_linguagem")

# ====================================================
# RQ04 – Atualização (dias desde a última atualização)
# ====================================================

def rq04(df):
    # Linha: Há quantos dias os repositórios estão sem atualização por cada ano de 'updatedAt'
    mediana_por_ano = df.groupby(df["updatedAt"].dt.year)["days_since_update"].median()
    plt.figure(figsize=(9, 4))
    sns.lineplot(x=mediana_por_ano.index, y=mediana_por_ano.values, marker="o")
    plt.title("RQ04 – Há quantos dias os repositórios estão sem atualização por cada ano")
    plt.xlabel("Ano da última atualização"); plt.ylabel("Mediana (dias)")
    salvar_grafico("RQ04_linha_mediana_days_since_update_por_ano")

    # Repositórios por linguagem: há quanto tempo estão sem atualização? (Violin)
    plt.figure(figsize=(10, 5))
    sns.violinplot(x="lang_top8", y="days_since_update", data=df[df["lang_top8"]!="Unknown"], cut=0, inner=None)
    plt.title("RQ04 – Repositórios por linguagem: há quanto tempo estão sem atualização? (Violin)")
    plt.xlabel("Linguagem (top8)"); plt.ylabel("Dias desde atualização")
    plt.xticks(rotation=30, ha="right")
    salvar_grafico("RQ04_violin_days_since_update_por_linguagem")

# =========================================
# RQ05 – Linguagens populares e popularidade
# =========================================

def rq05(df):
    # Barras: Top 15 linguagens entre os 1000 repositórios mais estrelados
    top15 = (
        df.loc[df["primaryLanguage"] != "Unknown", "primaryLanguage"]
        .value_counts()
        .head(15)
    )
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top15.index, y=top15.values, estimator=sum, errorbar=None)
    plt.title("RQ05 – Top 15 linguagens entre os 1000 repositórios mais estrelados")
    plt.xlabel("Linguagem")
    plt.ylabel("Qtd repositórios")
    plt.xticks(rotation=45, ha="right")
    salvar_grafico("RQ05_barras_top15_linguagens")

    # Barras empilhadas: Linguagem (top8) x faixa de estrelas
    ct = pd.crosstab(df["lang_top8"], df["star_bucket"])
    ct = ct.drop(index="Unknown", errors="ignore")
    ct.plot(kind="bar", stacked=True, figsize=(10, 6))
    plt.title("RQ05 – Linguagem × faixa de estrelas")
    plt.xlabel("Linguagem (top8)")
    plt.ylabel("Qtd repositórios")
    plt.xticks(rotation=30, ha="right")
    salvar_grafico("RQ05_empilhadas_linguagem_por_star_bucket")

    # Heatmap: mesma matriz de contagem
    plt.figure(figsize=(8, 6))
    sns.heatmap(ct, annot=True, fmt="d", cbar=True)
    plt.title("RQ05 – Heatmap: linguagem × faixa de estrelas")
    plt.xlabel("Faixa de estrelas"); plt.ylabel("Linguagem")
    salvar_grafico("RQ05_heatmap_lang_star_bucket")

# =========================================
# RQ06 – % de issues fechadas
# =========================================

def rq06(df):
    """Histograma de % de issues fechadas"""

    # repositórios com issues > 0
    mask = df["issues"] > 0

    pct = (df.loc[mask, "closedIssues"] / df.loc[mask, "issues"]) * 100
    plt.figure(figsize=(8, 5))
    sns.histplot(pct, bins=20, kde=False)
    plt.title("RQ06 – Distribuição: % de issues fechadas")
    plt.xlabel("% de issues fechadas")
    salvar_grafico("RQ06_hist_closed_issues_pct")

    print(f"RQ06: n={pct.size}, média={pct.mean():.2f}%, mediana={pct.median():.2f}%")


# =========================================
# RQ07 – BÔNUS (medianas por linguagem)
# =========================================

def rq07(df):
    df_plot = df[df["lang_top8"] != "Unknown"].copy()

    agg = (
        df_plot.groupby("lang_top8", as_index=False)
        .agg(
            median_prs=("pullRequests", "median"),
            median_releases=("releases", "median"),
            median_days_since_update=("days_since_update", "median"),
        )
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(x="lang_top8", y="median_prs", data=agg, errorbar=None)
    plt.title("RQ07 – Mediana de PRs por linguagem")
    plt.xlabel("Linguagem"); plt.ylabel("Mediana de PRs")
    plt.xticks(rotation=30, ha="right")
    salvar_grafico("RQ07_barras_mediana_prs_por_linguagem")

    plt.figure(figsize=(10, 6))
    sns.barplot(x="lang_top8", y="median_releases", data=agg, errorbar=None)
    plt.title("RQ07 – Mediana de releases por linguagem")
    plt.xlabel("Linguagem"); plt.ylabel("Mediana de releases")
    plt.xticks(rotation=30, ha="right")
    salvar_grafico("RQ07_barras_mediana_releases_por_linguagem")

    plt.figure(figsize=(10, 6))
    sns.barplot(x="lang_top8", y="median_days_since_update", data=agg, errorbar=None)
    plt.title("RQ07 – Comparativo entre linguagens: dias sem atualização")
    plt.xlabel("Linguagem"); plt.ylabel("Dias")
    plt.xticks(rotation=30, ha="right")
    salvar_grafico("RQ07_barras_mediana_days_since_update_por_linguagem")


def main():
    df = pd.read_csv(ARQ_CSV)
    df = preparar_df(df)

    rq01(df)
    rq02(df)
    rq03(df)
    rq04(df)
    rq05(df)
    rq06(df)
    rq07(df)

if __name__ == "__main__":
    main()
