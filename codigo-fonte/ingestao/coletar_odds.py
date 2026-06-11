import os
import json
import requests

from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

sport = [
    "soccer_brazil_campeonato",
    "soccer_conmebol_copa_libertadores",
    "soccer_conmebol_copa_sudamericana",
    "soccer_fifa_world_cup"

]



def coletar_odds(sport_key):
    URL = (
    f"https://api.the-odds-api.com/v4/sports/"
    f"{sport_key}/odds/"
    f"?apiKey={API_KEY}"
    f"&regions=eu"
    f"&markets=h2h"
)
    response = requests.get(URL)

    if response.status_code != 200:
        print(f"Erro: {response.status_code}")
        print(response.text)
        return
    
    dados = response.json()

    pasta = Path(f"data/bronze/{sport_key}")
    pasta.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    arquivo = pasta / f"odds_{timestamp}.json"

    

    with open(arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )
    print(f"{sport_key}: {len(dados)} jogos salvos")

if __name__ == "__main__":
    for sport_key in sport:
        coletar_odds(sport_key)

