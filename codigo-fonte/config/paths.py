from pathlib import Path


CONTAINER_DATA_DIR = Path("/opt/airflow/data")

PROJECT_DIR = Path(__file__).resolve().parents[2]
LOCAL_DATA_DIR = PROJECT_DIR / "data"

DATA_DIR = (
    CONTAINER_DATA_DIR
    if CONTAINER_DATA_DIR.exists()
    else LOCAL_DATA_DIR
)

BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"

GOLD_BEST_ODDS_DIR = GOLD_DIR / "melhores_odds"
