# Características de repositórios populares do GitHub

## Sobre o Projeto

Este projeto coleta e analisa dados dos repositórios mais populares (por número de estrelas) do GitHub, utilizando a API GraphQL oficial. O objetivo é extrair insights sobre tendências de desenvolvimento, linguagens de programação mais utilizadas, e padrões de contribuição na comunidade open-source.

## Como Executar

### Pré-requisitos
- Python 3.13.6
- Token de acesso pessoal do GitHub

## Estrutura do Projeto

```
├── code/
│   ├── src/
│   ├── main.py          # Script principal de coleta
│   └── query.graphql    # Query GraphQL para API GitHub
├── .env                 # Token de acesso GitHub (não versionado)
├── requirements.txt     # Dependências Python
└── repositories.csv     # Resultado da análise (gerado)
```

### Configuração do Ambiente

1. **Instale o Python 3.13.6**

2. **Crie o ambiente virtual**
```bash
python -m venv .venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
source .venv/Scripts/activate

# Linux/macOS
source .venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Configure o token do GitHub**
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione seu token: `GITHUB_TOKEN=seu_token_aqui`

### Executando o Projeto

1. **Navegue até o diretório do código**
```bash
cd code
```

2. **Execute o script principal**
```bash
python src/main.py
```

O arquivo `repositories.csv` será gerado com os dados coletados.

---


## Relatório de Análise

### 1. Introdução

A plataforma GitHub se tornou o epicentro do desenvolvimento colaborativo de software, hospedando milhões de repositórios que representam projetos de todos os tipos e escalas. Este estudo analisa os 100 repositórios mais populares (medidos por estrelas) para identificar tendências, padrões e características que definem os projetos de maior impacto na comunidade de desenvolvedores.

O número de estrelas em um repositório GitHub serve como indicador de popularidade e relevância na comunidade, refletindo tanto a utilidade quanto o interesse dos desenvolvedores. Ao examinar os repositórios mais estrelados, podemos obter insights valiosos sobre:
- Tecnologias e linguagens em ascensão
- Tipos de projetos que geram maior engajamento
- Padrões de manutenção e contribuição
- Evolução temporal do ecossistema open-source

### 2. Metodologia

#### 2.1 Coleta de Dados

A coleta foi realizada através da API GraphQL v4 do GitHub, que oferece maior eficiência e flexibilidade comparada à REST API. Os dados foram obtidos através de:

**Ferramenta:** Python com biblioteca `gql` para consultas GraphQL
**Período:** Agosto de 2025
**Amostra:** Top 100 repositórios ordenados por número de estrelas
**Estratégia de coleta:** Paginação com 25 repositórios por página, sistema de retry para robustez

#### 2.2 Parâmetros Coletados

Para cada repositório, foram extraídas as seguintes métricas:
- **Identificação:** Nome, proprietário
- **Popularidade:** Número de estrelas
- **Temporalidade:** Data de criação, última atualização
- **Tecnologia:** Linguagem principal e secundárias
- **Atividade:** Pull requests mergeados, releases, issues totais e fechadas

#### 2.3 Tratamento de Dados

- **Linguagens:** Priorização da linguagem principal; fallback para a linguagem com maior uso em bytes
- **Dados ausentes:** Classificação como "Unknown" quando não disponível
- **Robustez:** Sistema de retry com backoff exponencial para lidar com limitações de API

#### 2.4 Hipóteses Informais

Antes da coleta de dados, elaboramos algumas hipóteses iniciais sobre as características esperadas dos repositórios mais populares no GitHub:

- **Hipótese 1 — Maturidade e Atualizações Frequentes**  
  Projetos populares tendem a ser relativamente antigos (criados há mais de 5 anos), mas ainda recebem atualizações constantes, pois são mantidos por grandes comunidades.

- **Hipótese 2 — Contribuições Externas e Gestão de Issues**  
   Repositórios populares (mais de 50 mil estrelas) tendem a acumular ao menos 5.000 pull requests mergeadas ao longo do tempo e manter uma taxa de fechamento de issues superior a 80%.

- **Hipótese 3 — Linguagens Consolidadas**  
  A maioria dos repositórios populares é escrita em linguagens amplamente difundidas e consolidadas (JavaScript, Python, Java), em vez de linguagens de nicho ou recentes.

### 3. Resultados Obtidos

#### 3.1 Repositórios Mais Populares

Os 5 repositórios com maior número de estrelas:

1. **freeCodeCamp** (425.544 estrelas) - Plataforma educacional em TypeScript
2. **build-your-own-x** (409.134 estrelas) - Tutoriais de construção em Markdown
3. **awesome** (390.806 estrelas) - Lista curada de recursos
4. **free-programming-books** (364.851 estrelas) - Coleção de livros gratuitos em Python
5. **public-apis** (360.748 estrelas) - Catálogo de APIs públicas em Python

#### 3.2 Distribuição por Linguagem de Programação

Análise da linguagem principal dos top 100:

- **JavaScript:** 15 repositórios (15%) - Dominância do desenvolvimento web
- **Python:** 14 repositórios (14%) - Versatilidade em data science e automação
- **TypeScript:** 13 repositórios (13%) - Crescimento do JavaScript tipado
- **Unknown/Markdown:** 12 repositórios (12%) - Projetos de documentação
- **C++:** 6 repositórios (6%) - Sistemas de alta performance
- **Outras linguagens:** 40 repositórios (40%) - Java, Go, Rust, C#, etc.

#### 3.3 Categorias de Projetos

**Educacionais (25%):** freeCodeCamp, build-your-own-x, free-programming-books, coding-interview-university, system-design-primer

**Frameworks/Bibliotecas (23%):** React, Vue, TensorFlow, Bootstrap, Flutter, Next.js

**Ferramentas de Desenvolvimento (18%):** VS Code, Git, Docker, Kubernetes, Terminal

**Listas Curatoriais (12%):** awesome, public-apis, awesome-python, papers-we-love

**Sistemas/Infraestrutura (22%):** Linux, AutoGPT, Ollama, Supabase, Electron

#### 3.4 Padrões Temporais

**Projetos Veteranos (2010-2014):** 25 repositórios
- Incluem Linux (2011), React (2013), Bootstrap (2011)
- Demonstram longevidade e maturidade

**Era de Crescimento (2015-2019):** 45 repositórios
- Período de expansão do ecossistema JavaScript/TypeScript
- Emergência de ferramentas modernas de desenvolvimento

**Projetos Recentes (2020-2025):** 30 repositórios
- Foco em IA/ML (AutoGPT, DeepSeek, Whisper)
- Ferramentas de produtividade moderna

#### 3.5 Métricas de Atividade

**Repositórios com Alta Atividade de Contribuição:**
- **Kubernetes:** 62.213 pull requests, 47.617 issues
- **TensorFlow:** 35.596 pull requests, 40.708 issues
- **VS Code:** 35.922 pull requests, 204.094 issues

**Taxa Média de Resolução de Issues:** ~87% dos repositórios mantêm taxas de resolução acima de 80%

### 4. Hipóteses e Insights

#### 4.1 Hipótese: "Projetos Educacionais Dominam a Popularidade"
**Confirmada:** 25% dos top repositórios são educacionais, sugerindo que a comunidade valoriza altamente recursos de aprendizado.

**Implicação:** O GitHub não é apenas um repositório de código, mas uma plataforma de conhecimento.

#### 4.2 Hipótese: "JavaScript e Python Lideram o Ecossistema"
**Confirmada:** Juntos representam 29% dos repositórios, refletindo:
- **JavaScript:** Dominância do desenvolvimento web full-stack
- **Python:** Versatilidade em automação, data science e IA

#### 4.3 Hipótese: "Projetos de IA/ML Estão em Ascensão"
**Confirmada:** 15 repositórios relacionados a IA/ML nos últimos 5 anos:
- AutoGPT, Stable Diffusion, Ollama, Whisper, LangChain, DeepSeek
- Indica transformação tecnológica em direção à inteligência artificial

#### 4.4 Hipótese: "Ferramentas de Produtividade Geram Alto Engajamento"
**Confirmada:** VS Code (175k estrelas), Terminal do Windows (99k estrelas), PowerToys (122k estrelas)
- Desenvolvedores priorizam ferramentas que melhoram workflow

#### 4.5 Hipótese: "Projetos com Documentação Extensa São Mais Populares"
**Suportada:** Repositórios "awesome-*", documentações técnicas e livros gratuitos têm alta popularidade
- Sugere que organização e acessibilidade do conhecimento são valorizadas

### 5. Tendências Identificadas

#### 5.1 Tecnológicas
- **TypeScript em Crescimento:** 13% dos projetos, indicando maturação do ecossistema JavaScript
- **Rust Emergente:** Projetos como RustDesk e Tauri mostram adoção crescente
- **IA/ML Mainstream:** De nicho para categoria principal em 5 anos

#### 5.2 Organizacionais
- **Empresas Lideram:** Microsoft (4 repositórios), Facebook/Meta (3), Google (indireto)
- **Comunidade Forte:** Projetos mantidos por organizações independentes têm grande sucesso

#### 5.3 Evolutivas
- **Longevidade:** Projetos iniciais (2010-2014) mantêm relevância
- **Adaptabilidade:** Repositórios que evoluem com tendências permanecem populares

### 6. Conclusões

A análise dos top 100 repositórios GitHub revela um ecossistema diversificado mas com padrões claros:

1. **Educação como Motor:** Plataformas educacionais dominam, evidenciando o papel do GitHub como facilitador de aprendizado

2. **JavaScript/TypeScript e Python:** Consolidação como linguagens fundamentais do desenvolvimento moderno

3. **IA como Nova Fronteira:** Crescimento exponencial de projetos relacionados à inteligência artificial

4. **Valor da Curadoria:** Listas organizadas e documentação estruturada geram alto engajamento

5. **Sustentabilidade:** Projetos com comunidades ativas e manutenção consistente mantêm relevância ao longo do tempo

Esta análise fornece uma fotografia valiosa do estado atual do desenvolvimento open-source e sugere direções futuras para tecnologias e práticas de desenvolvimento de software.

---
