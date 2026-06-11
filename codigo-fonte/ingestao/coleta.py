#%%
import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


API_KEY = os.getenv("ODDS_API_KEY")

response = requests.get(
    f"https://api.the-odds-api.com/v4/sports/?apiKey={API_KEY}"
)

df = pd.DataFrame(response.json())
df