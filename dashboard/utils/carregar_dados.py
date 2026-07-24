from pathlib import Path

import pandas as pd
import streamlit as st


CAMINHO_PROJETO = Path(__file__).resolve().parents[2]

GOLD_DIR = (
    CAMINHO_PROJETO
    / "data"
    / "gold"
    / "melhores_odds"
)

GOLD_HISTORICO_DIR = (
    CAMINHO_PROJETO
    / "data"
    / "gold"
    / "historico_odds"
)


@st.cache_data
def carregar_dados_gold():
    if not GOLD_DIR.exists():
        return pd.DataFrame()

    try:
        return pd.read_parquet(GOLD_DIR)

    except Exception as erro:
        st.error(
            f"Erro ao carregar a Gold: {erro}"
        )
        return pd.DataFrame()


@st.cache_data
def carregar_dados_historico():
    if not GOLD_HISTORICO_DIR.exists():
        return pd.DataFrame()

    try:
        return pd.read_parquet(GOLD_HISTORICO_DIR)

    except Exception as erro:
        st.error(
            f"Erro ao carregar a Gold histórica: {erro}"
        )
        return pd.DataFrame()