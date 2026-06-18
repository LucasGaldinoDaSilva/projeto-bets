from pyspark.sql import SparkSession
from pyspark.sql.functions import max

spark = SparkSession.builder\
    .appName("ProcessamentoGold")\
    .getOrCreate()

df = spark.read.parquet("data/silver/soccer_fifa_world_cup/sport_key=soccer_fifa_world_cup/")

# Melhores ODDS 

gold_best_odds = (
    df.groupBy(
        "game_id",
        "home_team",
        "away_team",
        "outcome",
        "bookmaker_name"
    )
    .agg(
        max("odd").alias("best_odds")
    )
)

gold_best_odds.write \
    .mode("overwrite")\
    .parquet("data/gold/Melhor_odds")