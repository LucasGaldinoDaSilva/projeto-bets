# ⚽ Projeto Bets — Pipeline de Engenharia de Dados

Pipeline de Engenharia de Dados desenvolvido para coleta, processamento, armazenamento e disponibilização de dados de odds esportivas.

O projeto foi desenvolvido com foco em aplicar conceitos de **Data Engineering**, construindo um fluxo automatizado desde a ingestão dos dados de uma API até sua disponibilização para análise.

---

## 🏗️ Arquitetura

```text
                 ┌─────────────────┐
                 │  The Odds API   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     Bronze      │
                 │ Dados brutos    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     Silver      │
                 │    PySpark      │
                 │ Transformações  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │      Gold       │
                 │ Dados analíticos│
                 └────────┬────────┘
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
        ┌─────────────────┐ ┌───────────────┐
        │   PostgreSQL    │ │   Streamlit   │
        │ Armazenamento   │ │   Dashboard   │
        └─────────────────┘ └───────────────┘

                 ▲
                 │
        ┌─────────────────┐
        │ Apache Airflow  │
        │ Orquestração    │
        └─────────────────┘
```

---

## 🎯 Objetivo

O objetivo do projeto é construir um pipeline capaz de coletar dados de odds esportivas de diferentes competições, processá-los e disponibilizá-los de forma estruturada para análise.

Além da construção do dashboard, o projeto busca demonstrar na prática conceitos fundamentais de Engenharia de Dados, como:

* ingestão de dados através de APIs;
* processamento distribuído;
* arquitetura em camadas;
* transformação de dados;
* orquestração de pipelines;
* armazenamento em banco de dados;
* automação;
* consumo de dados para análise.

---

## 🔄 Pipeline de dados

### 1. Ingestão — Bronze

Os dados são coletados através da **The Odds API**.

As informações são armazenadas inicialmente em sua forma bruta, preservando os dados recebidos da fonte.

Competições utilizadas no projeto:

* Campeonato Brasileiro;
* Copa Libertadores;
* Copa Sul-Americana.

---

### 2. Processamento — Silver

Os dados da camada Bronze são processados utilizando **Apache Spark / PySpark**.

Nesta etapa são realizadas transformações como:

* normalização dos dados;
* expansão das estruturas de odds;
* organização dos eventos;
* tratamento dos registros;
* seleção das informações necessárias para as próximas etapas.

---

### 3. Camada analítica — Gold

Na camada Gold são gerados datasets preparados para consumo analítico.

Entre as informações disponibilizadas estão:

* partidas;
* times;
* casas de apostas;
* mercados;
* resultados;
* odds;
* horários das partidas;
* melhores odds encontradas.

Os dados são armazenados em formato **Parquet**.

---

## ⚙️ Orquestração

O **Apache Airflow** é utilizado para automatizar e orquestrar a execução do pipeline.

Fluxo principal:

```text
Ingestão
   ↓
Bronze
   ↓
Silver
   ↓
Gold
```

O pipeline é executado através de uma DAG responsável por controlar a sequência das etapas.

---

## 🗄️ Banco de dados

Os dados processados também são disponibilizados no **PostgreSQL**.

O banco é utilizado como camada de armazenamento para permitir que aplicações de consumo consultem os dados estruturados.

---

## 📊 Dashboard

O projeto possui um dashboard desenvolvido com **Streamlit** para visualização dos dados processados.

O dashboard apresenta informações como:

* campeonatos;
* partidas;
* casas de apostas;
* melhores odds;
* histórico das odds;
* probabilidade implícita das odds.

### Tecnologias utilizadas no dashboard

* Streamlit
* Pandas
* Plotly
* PostgreSQL

---

## 🛠️ Tecnologias

| Tecnologia     | Utilização                          |
| -------------- | ----------------------------------- |
| Python         | Desenvolvimento do pipeline         |
| PySpark        | Processamento e transformação       |
| Apache Spark   | Processamento de dados              |
| Apache Airflow | Orquestração                        |
| PostgreSQL     | Armazenamento                       |
| Docker         | Ambiente dos serviços               |
| Streamlit      | Dashboard                           |
| Pandas         | Manipulação de dados                |
| Plotly         | Visualização                        |
| The Odds API   | Fonte de dados                      |
| Parquet        | Armazenamento dos dados processados |
| Git/GitHub     | Versionamento                       |

---

## 📁 Estrutura do projeto

```text
projeto-bets/
│
├── airflow/
│   ├── dags/
│   │   └── pipeline_bets.py
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── codigo-fonte/
│   ├── config/
│   ├── ingestao/
│   │   └── coletar_odds.py
│   ├── processamento/
│   │   ├── silver.py
│   │   └── gold.py
│   └── utils/
│
├── dashboard/
│   ├── app.py
│   └── utils/
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── .gitignore
├── README.md
└── requirements.txt
```

> Os diretórios de dados gerados, ambientes virtuais, logs e arquivos contendo credenciais não são versionados no Git.

---

## 🔐 Variáveis de ambiente

As credenciais e configurações sensíveis são armazenadas através de variáveis de ambiente.

Exemplo:

```env
ODDS_API_KEY=sua_chave_aqui

POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=projeto_bets
```

O arquivo `.env` não deve ser enviado para o GitHub.

---

## 🚀 Como executar

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd projeto-bets
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv bets
source bets/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` com as configurações necessárias.

### 5. Executar o Airflow

Entre no diretório:

```bash
cd airflow
```

Execute:

```bash
docker compose up -d
```

O Airflow estará disponível localmente através da porta configurada no `docker-compose.yml`.

### 6. Executar o dashboard

Na pasta `dashboard`:

```bash
streamlit run app.py
```

---

## 📚 Conceitos praticados

Este projeto permitiu aplicar conceitos de:

* Engenharia de Dados;
* ETL;
* ELT;
* Data Lake;
* processamento distribuído;
* Apache Spark;
* PySpark;
* Apache Airflow;
* pipelines automatizados;
* APIs REST;
* armazenamento em Parquet;
* bancos relacionais;
* PostgreSQL;
* Docker;
* versionamento com Git;
* visualização de dados.

---

## 🚧 Próximos passos

Algumas possibilidades de evolução do projeto:

* implementação de testes automatizados;
* melhoria do monitoramento do pipeline;
* criação de alertas para falhas;
* expansão das fontes de dados;
* evolução da infraestrutura para cloud;
* implementação de CI/CD;
* utilização de uma plataforma de dados em nuvem.

---

## 👨‍💻 Autor

**Lucas Galdino da Silva**

Estudante de Análise e Desenvolvimento de Sistemas com foco em **Engenharia de Dados**.

### Tecnologias de interesse

Python • SQL • PySpark • Apache Airflow • PostgreSQL • Docker • Data Engineering

---

## 📌 Observação

Este projeto possui finalidade educacional e de portfólio, sendo utilizado para estudos e aplicação prática de conceitos de Engenharia de Dados.
