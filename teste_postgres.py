import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

usuario = os.getenv("POSTGRES_USER")
senha = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
porta = os.getenv("POSTGRES_PORT")
banco = os.getenv("POSTGRES_DB")

url = (
    f"postgresql+psycopg2://{usuario}:{senha}"
    f"@{host}:{porta}/{banco}"
)

engine = create_engine(url)

with engine.connect() as conexao:
    print("CONEXAO COM POSTGRESQL OK")