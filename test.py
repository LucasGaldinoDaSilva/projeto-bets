from pathlib import Path

import pandas as pd


CAMINHO_GOLD = (
	Path(__file__).resolve().parent
	/ "data"
	/ "gold"
	/ "melhores_odds"
)

df = pd.read_parquet(CAMINHO_GOLD)
print(df.head())
print(f"Registros carregados: {len(df)}")
