from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from datetime import datetime

from src.extract import extract_spotify_daily
from src.transform import transform_spotify_daily, save_silver
from src.load import (
    gold_consistent_songs,
    gold_streams_by_country,
    gold_daily_trends,
    save_gold,
)
from src.config import SILVER_DIR


def task_extract():
    df = extract_spotify_daily("spotify_daily.csv")
    df.write_parquet(SILVER_DIR / "bronze_snapshot.parquet")


def task_transform():
    import polars as pl
    from src.config import BRONZE_DIR

    df_raw = pl.read_parquet(SILVER_DIR / "bronze_snapshot.parquet")
    df_silver = transform_spotify_daily(df_raw)
    save_silver(df_silver, "spotify_daily_silver.parquet")


def task_generate_gold():
    import polars as pl

    df_silver = pl.read_parquet(SILVER_DIR / "spotify_daily_silver.parquet")

    # GOLD 1
    df_gold1 = gold_consistent_songs(df_silver)
    save_gold(df_gold1, "gold_consistent_songs.parquet")

    # GOLD 2
    df_gold2 = gold_streams_by_country(df_silver)
    save_gold(df_gold2, "gold_streams_by_country.parquet")

    # GOLD 3
    df_gold3 = gold_daily_trends(df_silver)
    save_gold(df_gold3, "gold_daily_trends.parquet")



with DAG(
    dag_id="spotify_etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["etl", "spotify", "medallion"],
):

    extract = PythonOperator(
        task_id="extract",
        python_callable=task_extract,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=task_transform,
    )

    gold = PythonOperator(
        task_id="generate_gold",
        python_callable=task_generate_gold,
    )

    extract >> transform >> gold
