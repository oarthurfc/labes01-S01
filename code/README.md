# Como criar ambiente virtual

1. Instale o Python 3.13.6

2. Crie o ambiente virtual 
```bash
python -m venv .venv
```
3. Ative o ambiente virtual
```bash
source .venv/Scripts/activate
```
4. Instale as dependências do projeto
```bash
pip install -r requirements.txt
```

# Para gerar o relatório com os dados coletados do GitHub

Com o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando:

1. Navegue até o diretório do projeto
```bash
cd/code
```

2. Execute o script
```bash
python src/main.py
```
Será gerado um arquivo `repositories.csv` com o resultado do processamento.

# Para gerar os gráficos a partir do arquivo CSV gerado

Com o ambiente virtual ativado e as dependências instaladas, além de o arquivo CSV já gerado, execute o seguinte comando:

1. Navegue até o diretório /code
```bash
cd/code
```

2. Execute o script
```bash
python src/graficos_rqs.py
```

3. Serão gerados os gráficos de análise na pasta code/graficos

# Dependências do projeto
load_dotenv - módulo para carregar variáveis de ambiente
os - módulo para obtenção de dados do sistema operacional (ex: navegação em diretórios, manipulação de arquivos)
time - módulo para manipulação de tempo
requests - módulo para trabalhar com requisições e exceções
gql - módulo para trabalhar com GraphQL
Client - módulo para criar um cliente GraphQL autenticado via token e realizar requisições
pandas, seaborn, matplotlib - módulos para análise e visualização de dados gráficos



