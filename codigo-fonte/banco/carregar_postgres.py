import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# CONFIGURAÇÕES

load_dotenv()

CAMINHO_GOLD = "data/gold/melhores_odds"
TABELA = "melhores_odds"

usuario = os.getenv("POSTGRES_USER")
senha = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
porta = os.getenv("POSTGRES_PORT")
banco = os.getenv("POSTGRES_DB")

# CONEXÃO

url = (
    f"postgresql+psycopg2://{usuario}:{senha}"
    f"@{host}:{porta}/{banco}"
)

engine = create_engine(url)

# LEITURA DA GOLD

print("Lendo dados da Gold...")

df = pd.read_parquet(CAMINHO_GOLD)

print(f"Total de registros encontrados: {len(df)}")

# AJUSTE DOS TIPOS

df["commence_time"] = pd.to_datetime(
    df["commence_time"],
    errors="coerce",
)

df["coleta_em"] = pd.to_datetime(
    df["coleta_em"],
    errors="coerce",
)

# TABELA TEMPORÁRIA

staging = "staging_melhores_odds"

print("Enviando dados para tabela temporária...")

df.to_sql(
    staging,
    engine,
    if_exists="replace",
    index=False,
)

# CARGA IDEMPOTENTE

print("Inserindo novos registros no PostgreSQL...")

sql = text("""
    INSERT INTO melhores_odds (
        sport_key,
        game_id,
        commence_time,
        coleta_em,
        home_team,
        away_team,
        bookmaker_key,
        bookmaker_name,
        market_key,
        outcome,
        best_odd
    )
    SELECT
        sport_key,
        game_id,
        commence_time,
        coleta_em,
        home_team,
        away_team,
        bookmaker_key,
        bookmaker_name,
        market_key,
        outcome,
        best_odd
    FROM staging_melhores_odds
    ON CONFLICT (
        sport_key,
        game_id,
        commence_time,
        coleta_em,
        bookmaker_key,
        market_key,
        outcome
    )
    DO NOTHING;
""")

with engine.begin() as conn:
    resultado = conn.execute(sql)

print(f"Novos registros inseridos: {resultado.rowcount}")

# REMOVER TABELA TEMPORÁRIA

with engine.begin() as conn:
    conn.execute(
        text(f"DROP TABLE IF EXISTS {staging}")
    )

print("Carga concluída com sucesso!")
