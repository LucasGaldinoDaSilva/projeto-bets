#%%
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col
import pandas as pd


spark = SparkSession.builder\
    .appName("Silver")\
    .getOrCreate()
   
df = (
    spark.read
    .option("multiline", "true")
    .json("data/bronze/soccer_fifa_world_cup/odds_20260616214645.json")
)

df_bookmakers = df.withColumn(
    "bookmakers",
    explode("bookmakers")
)

df_markets = df_bookmakers.withColumn(
    "markets",
    explode("bookmakers.markets")
)

df_outcomes = df_markets.withColumn(
    "outcome",
    explode("markets.outcomes")
)

silver_df = df_outcomes.select(
    col("id").alias("game_id"),
    "sport_key",
    "commence_time",
    "home_team",
    "away_team",

    col("bookmakers.key").alias("bookmaker_key"),
    col("bookmakers.title").alias("bookmaker_name"),

    col("markets.key").alias("market"),
    col("outcome.name").alias("outcome"),
    col("outcome.price").alias("odd"),

    col("bookmakers.last_update").alias("last_update")
)

silver_df.write \
    .mode("append")\
    .partitionBy("sport_key")\
    .parquet("data/silver/soccer_fifa_world_cup")
