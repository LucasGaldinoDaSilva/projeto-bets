from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max as spark_max


CAMINHO_CONTAINER = Path("/opt/airflow/data")
CAMINHO_LOCAL = Path(__file__).resolve().parents[2] / "data"

DATA_DIR = (
    CAMINHO_CONTAINER
    if CAMINHO_CONTAINER.exists()
    else CAMINHO_LOCAL
)

SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold" / "melhores_odds"


spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("ProcessamentoGoldOdds")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

if not SILVER_DIR.exists():
    spark.stop()
    raise FileNotFoundError(
        f"Diretório Silver não encontrado: {SILVER_DIR}"
    )

print(f"Lendo dados Silver de: {SILVER_DIR}")

df_silver = spark.read.parquet(str(SILVER_DIR))

gold_best_odds = (
    df_silver
    .filter(col("odd").isNotNull())
    .groupBy(
        "sport_key",
        "game_id",
        "commence_time",
        "home_team",
        "away_team",
        "market_key",
        "outcome",
    )
    .agg(
        spark_max("odd").alias("best_odd")
    )
)

print("Prévia da camada Gold:")

gold_best_odds.orderBy(
    "sport_key",
    "commence_time",
    "game_id",
).show(30, truncate=False)

(
    gold_best_odds.write
    .mode("overwrite")
    .partitionBy("sport_key")
    .parquet(str(GOLD_DIR))
)

print(f"Gold salva com sucesso em: {GOLD_DIR}")

spark.stop()