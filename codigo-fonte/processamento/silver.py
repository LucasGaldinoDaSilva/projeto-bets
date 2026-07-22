from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, input_file_name, regexp_extract


CAMINHO_CONTAINER = Path("/opt/airflow/data")
CAMINHO_LOCAL = Path(__file__).resolve().parents[2] / "data"

DATA_DIR = (
    CAMINHO_CONTAINER
    if CAMINHO_CONTAINER.exists()
    else CAMINHO_LOCAL
)

BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"


spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("ProcessamentoSilverOdds")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

arquivos_json = [
    str(arquivo)
    for arquivo in BRONZE_DIR.rglob("*.json")
]

if not arquivos_json:
    spark.stop()
    raise FileNotFoundError(
        f"Nenhum arquivo JSON encontrado em {BRONZE_DIR}"
    )

print(f"Diretório de dados: {DATA_DIR}")
print(f"Arquivos Bronze encontrados: {len(arquivos_json)}")

df_bronze = (
    spark.read
    .option("multiline", "true")
    .json(arquivos_json)
    .withColumn("arquivo_origem", input_file_name())
)

df_silver = (
    df_bronze
    .withColumn(
        "sport_key",
        regexp_extract(
            col("arquivo_origem"),
            r"/bronze/([^/]+)/",
            1,
        ),
    )
    .withColumn("bookmaker", explode(col("bookmakers")))
    .withColumn("market", explode(col("bookmaker.markets")))
    .withColumn("outcome_data", explode(col("market.outcomes")))
    .select(
        col("id").alias("game_id"),
        col("sport_key"),
        col("commence_time"),
        col("home_team"),
        col("away_team"),
        col("bookmaker.key").alias("bookmaker_key"),
        col("bookmaker.title").alias("bookmaker_name"),
        col("bookmaker.last_update").alias("bookmaker_last_update"),
        col("market.key").alias("market_key"),
        col("outcome_data.name").alias("outcome"),
        col("outcome_data.price").cast("double").alias("odd"),
        col("arquivo_origem"),
    )
    .dropDuplicates(
        [
            "game_id",
            "sport_key",
            "bookmaker_key",
            "market_key",
            "outcome",
            "bookmaker_last_update",
        ]
    )
)

df_silver.show(20, truncate=False)

(
    df_silver.write
    .mode("overwrite")
    .partitionBy("sport_key")
    .parquet(str(SILVER_DIR))
)

print(f"Silver salva com sucesso em: {SILVER_DIR}")

spark.stop()