import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


def criar_conexao():
    usuario = os.getenv("POSTGRES_USER")
    senha = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    porta = os.getenv("POSTGRES_PORT")
    banco = os.getenv("POSTGRES_DB")

    url = (
        f"postgresql+psycopg2://{usuario}:{senha}"
        f"@{host}:{porta}/{banco}"
    )

    return create_engine(url)


@st.cache_data(ttl=60)
def carregar_dados_gold():
    """
    Carrega somente a coleta mais recente de cada
    jogo, resultado e campeonato.
    """

    try:
        engine = criar_conexao()

        query = text("""
            WITH dados_recentes AS (
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
                    best_odd,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            sport_key,
                            game_id,
                            market_key,
                            outcome
                        ORDER BY coleta_em DESC
                    ) AS rn
                FROM melhores_odds
                WHERE market_key = 'h2h'
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
            FROM dados_recentes
            WHERE rn = 1
        """)

        with engine.connect() as conexao:
            df = pd.read_sql(query, conexao)

        return df

    except Exception as erro:
        st.error(
            f"Erro ao carregar dados do PostgreSQL: {erro}"
        )
        return pd.DataFrame()


@st.cache_data(ttl=60)
def carregar_dados_historico():
    """
    Carrega o histórico de odds do PostgreSQL.
    """

    try:
        engine = criar_conexao()

        query = text("""
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
                best_odd AS odd
            FROM melhores_odds
            WHERE market_key = 'h2h'
            ORDER BY coleta_em
        """)

        with engine.connect() as conexao:
            df = pd.read_sql(query, conexao)

        return df

    except Exception as erro:
        st.error(
            f"Erro ao carregar histórico do PostgreSQL: {erro}"
        )
        return pd.DataFrame()
