import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

URL = (
    f"https://api.the-odds-api.com/v4/sports/"
    f"soccer_brazil_campeonato/odds/"
    f"?apiKey={API_KEY}"
    f"&regions=eu"
    f"&markets=h2h"
)

def coletar_odds():
    response = requests.get(URL)

    if response.status_code != 200:
        print(f"Erro: {response.status_code}")
        print(response.text)
        return
    
    dados = response.json()

    data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    caminho_arquivo = (
        f"data/bronze/odds_{data_coleta}.json"

    )

    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )
    print(f"Arquvos salvo em: {caminho_arquivo}")
    print(f"Quantidade de jogos: {len(dados)}")

if __name__ == "__main__":
    coletar_odds()